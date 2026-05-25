# Fake News Detection in Ukrainian Media 🇺🇦

## Про проєкт
Цей проєкт вирішує задачу класифікації україномовних новин на правдиві (True) та маніпулятивні/фейкові (Fake), а також здійснює автоматичне виділення ключових сутностей (Information Extraction) для глибшого розуміння контексту пропаганди. 

Проєкт побудований на концепції **Dual Pipeline**:
1. **Classification (Ядро):** Класифікатор на базі TF-IDF (символьні n-грами) та LinearSVC.
2. **Information Extraction (IE):** Гібридний NER-модуль на базі spaCy (EntityRuler + Regex) для витягнення організацій, локацій та осіб.

## Результати (Metrics)
* **Accuracy:** 0.9236
* **Macro-F1:** 0.8903
* **Entity Recall (IE Pipeline):** 0.93

## Структура репозиторію
* `notebooks/final_project.ipynb` — головний енд-ту-енд ноутбук із повним пайплайном обробки тексту. Запускається через "Run All".
* `docs/final_project_report.md` — детальний звіт про архітектуру, порівняння метрик та аналіз помилок.
* `data/sample.csv` — фрагмент датасету для локального тестування.
* `requirements.txt` — список залежностей.

## Інструкція із запуску (Colab / Local)
1. Склонуйте цей репозиторій:
   `git clone (https://github.com/dmytroslav/NLP_Course.git)`
2. Встановіть залежності:
   `pip install -r requirements.txt`
3. Завантажте українську мовну модель для spaCy:
   `python -m spacy download uk_core_news_sm`
4. Відкрийте файл `notebooks/final_project.ipynb` у Jupyter Notebook, VS Code або Google Colab та виконайте всі комірки. У кінці ноутбука доступне інтерактивне віджет-вікно для тестування власних новин.
