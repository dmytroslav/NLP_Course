import spacy
from src.ner_rules import get_entity_patterns, regex_ner_component

def get_baseline_pipeline(model_name="uk_core_news_sm"):
    return spacy.load(model_name)

def get_hybrid_pipeline(model_name="uk_core_news_sm"):
    nlp = spacy.load(model_name)
    
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    ruler.add_patterns(get_entity_patterns())
    
    if "regex_ner_component" not in nlp.pipe_names:
        nlp.add_pipe("regex_ner_component", after="ner")
        
    return nlp

def extract_entities(nlp_model, text):
    doc = nlp_model(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]