def evaluate_simple(dataset, pred_key):
    total_expected = 0
    total_found = 0
    correct = 0
    
    for item in dataset:
        exp = [e['text'] for e in item['expected']]
        pred = [e['text'] for e in item[pred_key]]
        
        total_expected += len(exp)
        total_found += len(pred)
        
        for p in pred:
            if p in exp:
                correct += 1
                
    precision = round(correct / total_found, 2) if total_found > 0 else 0
    recall = round(correct / total_expected, 2) if total_expected > 0 else 0
                
    return {
        "expected": total_expected,
        "found": total_found,
        "correct": correct,
        "missed": total_expected - correct,
        "precision": precision,
        "recall": recall
    }