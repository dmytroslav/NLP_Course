# 🇺🇦 Fake News & Propaganda Detection (Two-Tier Architecture)

## Про проєкт
Цей проєкт вирішує задачу автоматичного виявлення маніпуляцій та фейків в українському інфопросторі. На відміну від стандартних рішень, система використовує **Two-Tier Architecture**, поєднуючи швидкість класичного Machine Learning та глибину сучасних Agentic Workflows.

### Архітектура системи
* **Tier 1 (Fast Filter & Extraction):** * *Метод:* TF-IDF (char n-grams) + LinearSVC.
  * *NER Модуль:* Гібридний пайплайн на spaCy (EntityRuler + Regex) для витягнення організацій та локацій.
  * *Мета:* Миттєва обробка тисяч новин, відсіювання клікбейту, витягнення ключових сутностей.
* **Tier 2 (Deep Semantic Fact-Checking):**
  * *Метод:* Stateful LLM Flow (через Groq API, модель `llama-3.1-8b-instant`).
  * *Мета:* Глибокий аналіз семантично складних фейків (написаних офіційною мовою), валідація JSON-схеми, використання repair loop у разі збоїв формату та видача текстового обґрунтування (`reasoning`).

## Результати (Metrics)
* **Tier 1 (SVM Baseline):** Accuracy = 0.9236, Macro-F1 = 0.8903.
* **Tier 1 (IE Pipeline):** Entity Recall = 0.93.
* **Tier 2 (Flow Orchestration):** Valid JSON Rate = 100% (завдяки repair loop).

## Інструкція із запуску (Colab / Local)
1. Склонуйте репозиторій та встановіть залежності (`pip install -r requirements.txt`).
2. Завантажте мовну модель: `python -m spacy download uk_core_news_sm`.
3. Відкрийте `notebooks/final_project.ipynb` і натисніть **Run All**.
4. **Запуск Tier 2:** Код безпечно попросить ввести ваш Groq API-ключ через вбудований віджет. Ключ не зберігається в коді.
5. У кінці ноутбука доступна **інтерактивна демо-панель** (UI-віджет) для перевірки власних текстів через обидва рівні системи.
