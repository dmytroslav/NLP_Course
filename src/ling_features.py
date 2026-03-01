import spacy

def extract_ling_features(text: str, nlp_model) -> dict:
    """
    Повертає словник з лемами та POS-тегами для тексту.
    """
    if not isinstance(text, str) or not text.strip():
        return {"lemma_text": "", "pos_seq": ""}

    doc = nlp_model(text)

    lemmas = [token.lemma_ for token in doc]
    pos_tags = [token.pos_ for token in doc]

    return {
        "lemma_text": " ".join(lemmas),
        "pos_seq": " ".join(pos_tags)
    }