import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report

def run_linear_svc(X_train, y_train, X_test, y_test, analyzer='word', ngram_range=(1, 2), class_weight='balanced'):
    """
    Тренує та оцінює модель LinearSVC.
    """
    print(f"--- Training LinearSVC (analyzer={analyzer}, ngram_range={ngram_range}, class_weight={class_weight}) ---")
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer=analyzer, ngram_range=ngram_range, sublinear_tf=True)),
        ('clf', LinearSVC(C=1.0, class_weight=class_weight, random_state=42, dual=False))
    ])
    
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    print(f"Accuracy: {acc:.4f}")
    print(f"Macro-F1: {macro_f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return pipeline, acc, macro_f1