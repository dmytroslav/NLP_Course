import os
import json
import re

class FactCheckAgent:
    def __init__(self, client, model="llama-3.1-8b-instant", log_file="data/tool_logs_lab12.jsonl"):
        self.client = client
        self.model = model
        self.log_file = log_file
        
        # Оновлений промпт з чіткою логікою для офіційних джерел
        self.system_prompt = """Ти — аналітик інформаційної безпеки (FactCheck Agent).
Твоє завдання — проаналізувати новину та винести фінальний вердикт: [FAKE] або [TRUE].

ЛОГІКА ПРИЙНЯТТЯ РІШЕНЬ:
- Якщо джерело "Офіційне, надійне" (наприклад, ГШ ЗСУ, Міністерство оборони, Офіційно) -> ВЕРДИКТ: [TRUE], навіть якщо точних даних у базі фактів немає.
- Якщо джерело "російська пропаганда", "анонімний телеграм" або факт прямо спростовано -> ВЕРДИКТ: [FAKE].

ВАЖЛИВІ ПРАВИЛА:
1. ВИКЛИКАЙ ІНСТРУМЕНТИ ТІЛЬКИ ЧЕРЕЗ API TOOL CALLING.
2. КАТЕГОРИЧНО ЗАБОРОНЕНО писати у відповіді сирі теги типу <function=...>.
3. Завжди завершуй свою відповідь чітко: ВЕРДИКТ: [FAKE] або ВЕРДИКТ: [TRUE]."""
        
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

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools_schema,
                tool_choice="auto",
                parallel_tool_calls=False,  # ВАЖЛИВО: Вимикаємо паралельні виклики для стабільності Groq
                temperature=0.0
            )
            
            response_message = response.choices[0].message
            tool_calls_log = []

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
                
            if final_answer:
                final_answer = re.sub(r'<function=.*?</function>', '', final_answer, flags=re.DOTALL).strip()
                
                # Запобіжник, щоб гарантувати правильний формат маркування
                if "[FAKE]" not in final_answer and "[TRUE]" not in final_answer:
                    if "не можу підтвердити" in final_answer.lower() or "фейк" in final_answer.lower():
                        final_answer += "\n\nВЕРДИКТ: [FAKE]"
                    else:
                        final_answer += "\n\nВЕРДИКТ: [TRUE]"
            else:
                final_answer = "Відповідь не згенерована.\n\nВЕРДИКТ: [FAKE]"

            self.log_interaction(text, tool_calls_log, final_answer)
            return final_answer
            
        except Exception as e:
            return f"Error executing agent: {e}"