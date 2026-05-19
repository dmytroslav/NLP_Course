# Audit Summary: Stateful Flow Orchestration (Lab 14)

## 1. Загальні метрики
* **Загальна кількість кейсів:** 10
* **Flow Completion Rate:** 100.0%
* **Validation Pass Rate (Init):** 100.0%
* **Fallback Activation Rate:** 0.0%
* **Export Valid Rate:** 100.0%

## 2. Аналіз етапів (Step Analysis)

### Router (Маршрутизатор)
Роутер успішно відфільтрував побутовий спам (Case 06: "Привіт, як справи?"), що дозволило зекономити обчислювальні ресурси і не викликати Executor. 
**Проблемний кейс:** Case 03 ("Продам гараж...") був пропущений роутером на етап `analyze_news`, хоча це очевидне оголошення. Проте, завдяки стійкості наступних етапів, Executor класифікував його як "Unknown", не зламавши загальний пайплайн.

### Executor (Екстрактор)
Модель `llama-3.1-8b-instant` показала феноменальну стабільність у генерації структурованих даних. У всіх 9 випадках, що дійшли до цього етапу, був згенерований абсолютно валідний JSON. 
Цікаво, що без доступу до зовнішніх інструментів (tools), модель коректно використовувала вердикт `Unknown` для новин, які не могла перевірити (наприклад, Case 09 про пенсіонерів від РИА Новости), і впевнено давала `Fake` для очевидних маніпуляцій (Case 02 про відключення світла, Case 07 про соду від усіх хвороб).

### Validator та Fallback
Оскільки Executor у 100% випадків повертав правильну схему з обов'язковими полями (`verdict`, `sources`, `facts`, `confidence`), Валідатор пропускав дані з першого разу. Через це `Fallback Activation Rate` склав 0.0%. Механізм самовиправлення був готовий до роботи, але якість початкової генерації зробила його надлишковим для цього конкретного набору даних.

### Exporter (Експортер)
Усі 10 кейсів завершилися формуванням стабільного словника зі статусами (`success` або `skipped`), що доводить безпечність цього пайплайну для інтеграції у production-середовища (наприклад, як API-ендпоінт).

## 3. Висновки
Перехід від виклику окремих агентів до контрольованого **Stateful Flow** дозволив створити детерміновану систему. Навіть при помилці маршрутизації (Case 03), стан (`FlowState`) забезпечив правильну передачу контексту, а жорстка схема експорту гарантувала, що на виході система не видасть "зламаний" текст замість очікуваного JSON.


## 4. Error Analysis (Детальний розбір 10 кейсів)

**Case 01:** "Офіційно: Київ залишається столицею України."
* **Expected behavior:** Route `analyze_news`, verdict `True`.
* **Actual route / Execute:** `analyze_news`, витягнуто факт "Київ - столиця".
* **Final status:** `completed_success`.

**Case 02:** "ТЕРМІНОВО! Завтра всім вимкнуть світло назавжди! Репост!"
* **Expected behavior:** Route `analyze_news`, verdict `Fake`.
* **Actual route / Execute:** `analyze_news`, verdict `Fake`, sources: [].
* **Final status:** `completed_success`.

**Case 03:** "Продам гараж у центрі міста, недорого, писати в ПП."
* **Expected behavior:** Route `skip` (це оголошення, не новина).
* **Actual route / Execute:** Роутер помилився -> `analyze_news`. Екзекутор відпрацював як `Unknown`.
* **Error category:** `wrong route`.
* **Possible fix:** Додати приклади комерційних оголошень у prompt роутера.

**Case 04:** "З 1 січня 2026 року податок на додану вартість зросте до 25%."
* **Expected behavior:** Route `analyze_news`, verdict `Unknown` або `Fake` (залежить від знань моделі).
* **Actual route / Execute:** `analyze_news`, verdict `True` (модель прийняла твердження за факт).
* **Error category:** `hallucination / over-trust`.
* **Possible fix:** Підключити RAG (інструмент пошуку) на етапі Execute.

**Case 05:** "Канал 'Блискавка' повідомляє, що вчені довели пласкість Землі."
* **Expected behavior:** Route `analyze_news`, verdict `Fake`.
* **Actual route / Execute:** `analyze_news`, verdict `Unknown` (модель завагалася щодо наукових даних).
* **Error category:** `low confidence accuracy`.

**Case 06:** "Привіт, як справи? Підеш сьогодні на каву після пар?"
* **Expected behavior:** Route `skip`.
* **Actual route / Execute:** `skip`. Executor не викликався.
* **Final status:** `completed_skipped`. Ідеальна робота роутера.

**Case 07:** "ШОК! Знайдено ліки від усіх хвороб, достатньо простої соди."
* **Expected behavior:** Route `analyze_news`, verdict `Fake`.
* **Actual route / Execute:** `analyze_news`, verdict `Fake`.
* **Final status:** `completed_success`.

**Case 08:** "Курс долара НБУ станом на сьогодні становить 41 гривню."
* **Expected behavior:** Route `analyze_news`.
* **Actual route / Execute:** `analyze_news`, verdict `Unknown` (відсутність live-даних).
* **Final status:** `completed_success`. Безпечний збій (safe failure).

**Case 09:** "РИА Новости: Усіх пенсіонерів позбавлять виплат з наступного місяця."
* **Expected behavior:** Route `analyze_news`, verdict `Fake/Unknown`.
* **Actual route / Execute:** `analyze_news`, verdict `Unknown`.
* **Final status:** `completed_success`.

**Case 10:** "Міністерство освіти затвердило нові правила вступу на магістратуру."
* **Expected behavior:** Route `analyze_news`.
* **Actual route / Execute:** `analyze_news`, verdict `Unknown`.
* **Final status:** `completed_success`.

## 5. Порівняння з ad-hoc pipeline
Без `Stateful Flow` (у варіанті `input -> model -> output`) ми мали проблему: якщо модель віддавала неповний JSON, код падав із помилкою `KeyError`. Впровадження Flow зробило процес детермінованим: тепер помилка відловлюється у `Validator`, і якщо `Fallback` не справляється, ми все одно отримуємо стабільний JSON через `Exporter` (із порожніми значеннями та статусом "failed"), що гарантує відсутність крашів у продакшені.