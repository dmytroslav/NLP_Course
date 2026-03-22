import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

def build_pipeline(ngram_range=(1, 1), class_weight=None, max_iter=500):

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='word', sublinear_tf=True, ngram_range=ngram_range)),
        ('clf', LogisticRegression(max_iter=max_iter, class_weight=class_weight, random_state=42))
    ])
    return pipeline

def evaluate_model(pipeline, X_test, y_test, class_names=['False', 'True']):
    
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    report = classification_report(y_test, y_pred, target_names=class_names)
    cm = confusion_matrix(y_test, y_pred)
    
    return {
        'accuracy': acc,
        'macro_f1': macro_f1,
        'report': report,
        'confusion_matrix': cm,
        'y_pred': y_pred
    }

def get_top_features(pipeline, class_names=['False', 'True'], top_n=10):
    
    vectorizer = pipeline.named_steps['tfidf']
    clf = pipeline.named_steps['clf']
    
    feature_names = vectorizer.get_feature_names_out()
    coefs = clf.coef_[0] 
    
    
    sorted_coef_indices = np.argsort(coefs)
    
    
    top_negative = [(feature_names[i], coefs[i]) for i in sorted_coef_indices[:top_n]]
    
    
    top_positive = [(feature_names[i], coefs[i]) for i in sorted_coef_indices[-top_n:]][::-1]
    
    return {
        class_names[0]: top_negative,
        class_names[1]: top_positive
    }