# Лабораторна робота 6: TF-IDF + Logistic Regression Baseline

## 1. Напрям роботи
Напрям: **A** (Класифікація текстів / Fake News Detection).

## 2. Підзадача
Бінарна класифікація текстів на основі ознаки `label` (True / False). Мета: побудувати базову ML-модель для виявлення патернів у текстах і встановлення метрик-орієнтирів (baselines).

## 3. Baseline-варіанти для порівняння
* **Baseline 1:** `TfidfVectorizer(ngram_range=(1,1))` + `LogisticRegression(class_weight=None)`. Базовий підхід на уніграмах без врахування дисбалансу.
* **Baseline 2:** `TfidfVectorizer(ngram_range=(1,2))` + `LogisticRegression(class_weight='balanced')`. Використання біграм та балансування ваг класів для боротьби з дисбалансом (76.7% vs 23.3%), виявленим у ЛР5.

## 4. Основні цифри (будуть оновлені після запуску Colab)
* **Baseline 1 (Test):** Accuracy = TBA, Macro-F1 = TBA
* **Baseline 2 (Test):** Accuracy = TBA, Macro-F1 = TBA
* **Краща модель:** TBA

## 5. Error Analysis (коротко)
TBA (буде заповнено після ручного розбору помилок: які типи текстів модель класифікує неправильно і чому).