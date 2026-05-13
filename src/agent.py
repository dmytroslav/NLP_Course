import os
import json
import re
import uuid
from src.tool_logger import ToolLogger

class FactCheckAgent:
    def __init__(self, client, model="llama-3.1-8b-instant", log_file="data/tool_logs_lab12.jsonl"):
        self.client = client
        self.model = model
        self.logger = ToolLogger(log_file)
        
        self.system_prompt = """Ти — суворий аналітик інформаційної безпеки.
Твоє завдання — перевірити новину за допомогою інструментів і винести вердикт.

ПРАВИЛА:
1. Офіційне, надійне джерело (ГШ ЗСУ, Міноборони) -> ВЕРДИКТ: [TRUE].
2. Російська пропаганда ("риа новости") -> ВЕРДИКТ: [FAKE].
3. Ненадійне джерело ("анонімний телеграм", "труха") -> ВЕРДИКТ: [FAKE].
4. Якщо немає надійного джерела і немає офіційних даних -> ВЕРДИКТ: [FAKE].

Завершуй відповідь рядком:
ВЕРДИКТ: [TRUE] або ВЕРДИКТ: [FAKE]"""
        
        from src.tools import tools_schema, available_tools
        self.tools_schema = tools_schema
        self.available_tools = available_tools

    def run(self, text: str, task_id: str = None) -> str:
        if not task_id:
            task_id = f"case_{uuid.uuid4().hex[:6]}"
            
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": text}
        ]
        final_answer = "ВЕРДИКТ: [FAKE]"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools_schema,
                tool_choice="auto",
                parallel_tool_calls=False,
                temperature=0.0
            )
            
            response_message = response.choices[0].message

            if response_message.tool_calls:
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    func_name = tool_call.function.name
                    func_args_str = tool_call.function.arguments
                    success = True
                    error_msg = None
                    
                    if func_name in self.available_tools:
                        try:
                            func_args = json.loads(func_args_str)
                            func_result = self.available_tools[func_name](**func_args)
                        except Exception as e:
                            func_result = {"error": "Invalid params"}
                            success = False
                            error_msg = str(e)
                    else:
                        func_result = {"error": "Tool not found"}
                        success = False
                        error_msg = "Tool missing"
                        
                    # Логування у правильному форматі
                    self.logger.log_call(
                        task_id=task_id,
                        tool_name=func_name,
                        tool_input=func_args_str,
                        tool_output=func_result,
                        success=success,
                        error=error_msg
                    )
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": str(func_result)
                    })
                
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.0
                )
                final_answer = final_response.choices[0].message.content
            else:
                final_answer = response_message.content
                
        except Exception as e:
            final_answer = f"API Error: {str(e)}\n\nВЕРДИКТ: [FAKE]"

        if final_answer:
            final_answer = re.sub(r'<function=.*?</function>', '', final_answer, flags=re.DOTALL).strip()
            if "[FAKE]" not in final_answer and "[TRUE]" not in final_answer:
                final_answer += "\n\nВЕРДИКТ: [FAKE]"
                
        return final_answer