# Lab 3: Lemma/POS Baseline

**1. [cite_start]Який напрям:** A (Класифікація текстів: Fake vs True) [cite: 235]
**2. [cite_start]Який інструмент для lemma/POS:** spaCy (модель `uk_core_news_sm`) [cite: 311]
**3. [cite_start]Який baseline ви зробили:** TF-IDF Vectorizer + Logistic Regression (з балансуванням класів)[cite: 236, 312].
**4. [cite_start]Основні цифри "до/після":** [cite: 313]
- *Processed Text:* Accuracy = 0.8882, Macro-F1 = 0.8442
- *Lemmatized Text:* Accuracy = 0.8803, Macro-F1 = 0.8347
**5. Ваш висновок:** Використовувати леми для основної задачі бінарної класифікації фейків недоцільно, оскільки вони знищують важливі стилістичні та емоційні маркери тексту (що підтверджується падінням метрик). [cite_start]Леми не беремо для ML-моделі, але можемо використати POS-теги в майбутньому як додаткові фічі[cite: 314].