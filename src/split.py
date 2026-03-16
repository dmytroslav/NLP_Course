import pandas as pd
from sklearn.model_selection import train_test_split
import json
import os
from datetime import datetime

def make_splits(df: pd.DataFrame, strategy: str = 'random', seed: int = 42, 
                test_size: float = 0.1, val_size: float = 0.1, stratify_col: str = None) -> dict:
   
    # Спочатку відділяємо test
    train_val_df, test_df = train_test_split(
        df, 
        test_size=test_size, 
        random_state=seed,
        stratify=df[stratify_col] if strategy == 'stratified' and stratify_col else None
    )
    
    
    val_ratio = val_size / (1.0 - test_size)
    
    train_df, val_df = train_test_split(
        train_val_df, 
        test_size=val_ratio, 
        random_state=seed,
        stratify=train_val_df[stratify_col] if strategy == 'stratified' and stratify_col else None
    )
    
    splits = {
        'train': train_df,
        'val': val_df,
        'test': test_df,
        'metadata': {
            'strategy': strategy,
            'seed': seed,
            'stratify_col': stratify_col,
            'sizes': {
                'train': len(train_df),
                'val': len(val_df),
                'test': len(test_df)
            },
            'proportions': f"{int((1-test_size-val_size)*100)}/{int(val_size*100)}/{int(test_size*100)}"
        }
    }
    
    return splits

def save_splits(splits: dict, out_dir: str):
    
    os.makedirs(out_dir, exist_ok=True)
    
    # Зберігаємо ID [cite: 30-32]
    for split_name in ['train', 'val', 'test']:
        ids = splits[split_name].index.astype(str).tolist()
        file_path = os.path.join(out_dir, f'splits_{split_name}_ids.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ids))
            
    
    manifest = splits['metadata']
    manifest['generated_at'] = datetime.now().isoformat()
    
    
    docs_dir = os.path.join(os.path.dirname(out_dir), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    manifest_path = os.path.join(docs_dir, 'splits_manifest_lab5.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
        
    print(f"Спліти збережено у {out_dir}")
    print(f"Маніфест збережено у {manifest_path}")