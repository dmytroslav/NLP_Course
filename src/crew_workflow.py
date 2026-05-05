import json

class FakeNewsCrewWorkflow:
    def __init__(self, triager, extractor, reviewer, fallback_agent):
        self.triager = triager
        self.extractor = extractor
        self.reviewer = reviewer
        self.fallback_agent = fallback_agent

    def process_case(self, case_id: str, input_text: str) -> dict:
        """
        Головний метод workflow, який запускає агентів по черзі 
        і формує словник для логування згідно з вимогами ЛР13.
        """
        # Базовий словник для логу (crew_logs_lab13.jsonl)
        log_entry = {
            "case_id": case_id,
            "input": input_text,
            "triager_output": None,
            "extractor_output": None,
            "reviewer_output": None,
            "fallback_triggered": False,
            "fallback_output": None,
            "final_output": None,
            "status": "processing"
        }

        try:
            # 1. Етап Triage (Маршрутизація)
            triager_out = self.triager.run(input_text)
            log_entry["triager_output"] = triager_out

            # 2. Етап Extraction (Екстракція)
            extractor_out = self.extractor.run(
                text=input_text,
                route=triager_out.get("route", "standard_news"),
                notes=triager_out.get("notes", "")
            )
            log_entry["extractor_output"] = extractor_out

            # 3. Етап Review (Перевірка)
            reviewer_out = self.reviewer.run(
                text=input_text,
                extracted_data=extractor_out
            )
            log_entry["reviewer_output"] = reviewer_out

            # 4. Логіка делегування та Fallback
            verdict = reviewer_out.get("verdict")

            if verdict == "accept":
                log_entry["final_output"] = extractor_out
                log_entry["status"] = "accepted_first_try"

            elif verdict == "repair_needed":
                log_entry["fallback_triggered"] = True
                
                # Запускаємо Fallback агента для виправлення
                fallback_out = self.fallback_agent.run(
                    text=input_text,
                    extracted_data=extractor_out,
                    issues=reviewer_out.get("issues", [])
                )
                log_entry["fallback_output"] = fallback_out
                
                # Після repair приймаємо результат, але статус вказує на те, що був ремонт
                log_entry["final_output"] = fallback_out
                log_entry["status"] = "accepted_after_repair"

            elif verdict == "manual_review":
                # Якщо Reviewer вирішив, що система не впорається, передаємо людині
                log_entry["final_output"] = extractor_out
                log_entry["status"] = "manual_review_required"

        except Exception as e:
            # Safe failure: якщо впала сама LLM або парсинг
            log_entry["status"] = "failed_execution"
            log_entry["final_output"] = {"error": str(e)}

        return log_entry