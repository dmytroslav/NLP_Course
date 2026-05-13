import os

class FactCheckAgent:
    def __init__(self, client, model="llama3-8b-8192", log_file="data/tool_logs_lab12.jsonl"):
        self.client = client
        self.model = model
        self.log_file = log_file
        self.system_prompt = """Ти - FactCheck Agent.
        Завжди використовуй інструменти для перевірки джерела та фактів перед винесенням вердикту (FAKE чи TRUE)."""
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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools_schema,
            tool_choice="auto",
            temperature=0.1
        )
        
        response_message = response.choices[0].message
        tool_calls_log = []

        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                func_result = self.available_tools[func_name](**func_args)
                
                tool_calls_log.append({
                    "tool": func_name,
                    "args": func_args,
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
                temperature=0.1
            )
            final_answer = final_response.choices[0].message.content
        else:
            final_answer = response_message.content

        self.log_interaction(text, tool_calls_log, final_answer)
        return final_answer