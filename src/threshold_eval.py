import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, precision_score, recall_score, f1_score

def evaluate_thresholds(y_true, y_scores, thresholds_to_test=[0.0]):
    """
    Будує PR-криву та оцінює задані пороги рішення.
    (Для LinearSVC дефолтний поріг = 0.0)
    """
    precision, recall, pr_thresholds = precision_recall_curve(y_true, y_scores)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, marker='.', label='LinearSVC PR curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    plt.grid()
    plt.show()
    
    print("--- Threshold Evaluation ---")
    for thresh in thresholds_to_test:
        y_pred_custom = (y_scores >= thresh).astype(int)
        # Assuming True is 1 and False is 0. Adapting for boolean inputs:
        if y_true.dtype == 'bool':
            y_pred_custom = y_pred_custom.astype(bool)
            
        p = precision_score(y_true, y_pred_custom, pos_label=False) # Фокус на minority class (False)
        r = recall_score(y_true, y_pred_custom, pos_label=False)
        f1 = f1_score(y_true, y_pred_custom, pos_label=False)
        
        print(f"Threshold: {thresh:>5} | Minor Class (False) -> Precision: {p:.4f}, Recall: {r:.4f}, F1: {f1:.4f}")