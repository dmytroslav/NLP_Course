import os
import json
import re

class FactCheckAgent:
    def __init__(self, client, model="llama-3.1-8b-instant", log_file="data/tool_logs_lab12.jsonl"):
        self.client = client
        self.model = model
        self.log_file = log_file
        
        # Мінімалістичний промпт без згадок про "теги". Чітка логіка.
        self.system_prompt = """Ти — суворий аналітик інформаційної безпеки.
Твоє завдання — перевірити новину за допомогою доступних інструментів і винести вердикт.

ПРАВИЛА ПРИЙНЯТТЯ РІШЕНЬ (ПРЕЗУМПЦІЯ ФЕЙКУ):
1. Якщо джерело "Офіційне, надійне" (ГШ ЗСУ, Міноборони, Офіційно) -> ВЕРДИКТ: [TRUE].
2. Якщо джерело російська пропаганда ("риа новости") -> ВЕРДИКТ: [FAKE].
3. Якщо джерело ненадійне або маніпулятивне ("анонімний телеграм", "труха", "влада приховує") -> ВЕРДИКТ: [FAKE].
4. Якщо немає надійного джерела і немає офіційних даних -> ВЕРДИКТ: [FAKE].

Твоя відповідь має містити короткий висновок і ОБОВ'ЯЗКОВО закінчуватися рядком:
ВЕРДИКТ: [TRUE] або ВЕРДИКТ: [FAKE]"""
        
        from src.tools import tools_schema, available_tools
        self.tools_schema = tools_schema
        self.available_tools = available_tools

    def log_interaction(self, task, tool_calls, final_answer):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        log_entry = {
            "task": task,
            "tool_calls": tool_calls,
            "final_answer": final_answer
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def run(self, text: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": text}
        ]

        tool_calls_log = []
        final_answer = "ВЕРДИКТ: [FAKE]" # Дефолтне значення на випадок збою

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
                    
                    if func_name in self.available_tools:
                        try:
                            func_args = json.loads(tool_call.function.arguments)
                            func_result = self.available_tools[func_name](**func_args)
                        except Exception:
                            func_result = "Помилка параметрів інструменту."
                    else:
                        func_result = f"Інструмент {func_name} не знайдено."
                        
                    tool_calls_log.append({
                        "tool": func_name,
                        "args": tool_call.function.arguments,
                        "result": func_result
                    })
                    
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
            # Запобіжник від крашу API Groq (якщо модель знову зламає теги)
            err_msg = str(e)
            if "tool_use_failed" in err_msg:
                final_answer = "Модель виконала виклик інструменту з порушенням синтаксису API.\n\nВЕРДИКТ: [FAKE]"
            else:
                final_answer = f"API Error: {err_msg}\n\nВЕРДИКТ: [FAKE]"

        # Фінальне очищення
        if final_answer:
            final_answer = re.sub(r'<function=.*?</function>', '', final_answer, flags=re.DOTALL).strip()
            if "[FAKE]" not in final_answer and "[TRUE]" not in final_answer:
                final_answer += "\n\nВЕРДИКТ: [FAKE]"
                
        self.log_interaction(text, tool_calls_log, final_answer)
        return final_answer