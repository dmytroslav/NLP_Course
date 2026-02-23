import re
import spacy

# Завантажуємо модель один раз при імпорті
try:
    nlp = spacy.load("uk_core_news_sm")
except OSError:
    print("Model not found. Please run: python -m spacy download uk_core_news_sm")
    nlp = None

def normalize_text(text: str) -> str:
    """
    Нормалізація: апострофи, лапки, тире, зайві пробіли.
    """
    if not isinstance(text, str):
        return str(text)

    # 1. Уніфікація апострофів (всі види -> ')
    text = re.sub(r"[’ʼ`]", "'", text)

    # 2. Уніфікація лапок («...» -> "...", “...” -> "...")
    text = re.sub(r"[«»“”]", '"', text)

    # 3. Уніфікація тире (–, — -> -)
    text = re.sub(r"[–—]", "-", text)

    # 4. Прибирання зайвих пробілів (більше одного -> один)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def mask_pii(text: str) -> str:
    """
    Маскування персональних даних: URL, Email, Phone.
    """
    # URL
    text = re.sub(r'https?://\S+|www\.\S+', '<URL>', text)
    # Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '<EMAIL>', text)
    # Phone (простий варіант для укр номерів)
    text = re.sub(r'\+?380\d{9}', '<PHONE>', text)
    
    return text

def clean_text(text: str) -> str:
    """
    Базова очистка від HTML та сміття.
    """
    # HTML теги
    text = re.sub(r'<[^>]+>', '', text)
    # Залишаємо маски, але прибираємо спецсимволи, якщо треба (тут мінімально)
    return text

def sentence_split(text: str) -> list:
    """
    Розбиття на речення за допомогою Spacy.
    Стійке до скорочень (м., вул., ім.) та ініціалів.
    """
    if not nlp:
        return [text]
    
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

def preprocess_pipeline(text: str) -> dict:
    """
    Головна функція, яка викликає всі попередні.
    Повертає словник з різними етапами обробки.
    """
    # 1. Нормалізація
    normalized = normalize_text(text)
    # 2. Маскування
    masked = mask_pii(normalized)
    # 3. Очистка
    cleaned = clean_text(masked)
    # 4. Спліт
    sentences = sentence_split(cleaned)
    
    return {
        "raw": text,
        "normalized": normalized,
        "cleaned": cleaned, # фінальний текст (string)
        "sentences": sentences # список речень (list)
    }