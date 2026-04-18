import re
import spacy
from spacy.language import Language

def get_entity_patterns():
    return [
        {"label": "ORG", "pattern": [{"LOWER": "ппо"}]},
        {"label": "ORG", "pattern": [{"LOWER": "генеральний"}, {"LOWER": "штаб"}]},
        {"label": "ORG", "pattern": [{"LOWER": "оон"}]},
        {"label": "ORG", "pattern": [{"LOWER": "нато"}]},
        {"label": "ORG", "pattern": [{"LOWER": "держспецзв'язку"}]},
        {"label": "ORG", "pattern": [{"LOWER": "київстар"}]},
        {"label": "ORG", "pattern": [{"LOWER": "червоний"}, {"LOWER": "хрест"}]},
        {"label": "WEAPON", "pattern": [{"LOWER": "storm"}, {"LOWER": "shadow"}]},
        {"label": "WEAPON", "pattern": [{"LOWER": "himars"}]},
        {"label": "PER", "pattern": [{"LOWER": "зеленський"}]}
    ]

@Language.component("regex_ner_component")
def regex_ner_component(doc):
    original_ents = list(doc.ents)
    new_ents = []
    
    money_pattern = r"\d+\s+(?:млн|млрд|тисяч)\s+(?:доларів|гривень|євро)|\d+\s*%"
    for match in re.finditer(money_pattern, doc.text, re.IGNORECASE):
        start, end = match.span()
        span = doc.char_span(start, end, label="MONEY", alignment_mode="expand")
        if span is not None:
            new_ents.append(span)

    date_pattern = r"сьогодні вночі|вчора о \d{2}:\d{2}|\d{1,2} [а-яяіїєґ]+|влітку \d{4} року|понад рік"
    for match in re.finditer(date_pattern, doc.text, re.IGNORECASE):
        start, end = match.span()
        span = doc.char_span(start, end, label="DATE", alignment_mode="expand")
        if span is not None:
            new_ents.append(span)

    doc.ents = spacy.util.filter_spans(original_ents + new_ents)
    return doc