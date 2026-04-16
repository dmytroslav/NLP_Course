!pip install gensim pandas numpy

import os
import pandas as pd
import numpy as np
from gensim.models import Word2Vec, FastText


os.chdir('/content')
!rm -rf NLP_Course
REPO_URL = "https://github.com/dmytroslav/NLP_Course.git"
!git clone $REPO_URL

# Завантажуємо датасет
data_path = '/content/NLP_Course/data/processed_v2.csv'
print(f"Завантаження даних з {data_path}...")
df = pd.read_csv(data_path)
display(df.head(2))

text_column = 'text' 

df = df.dropna(subset=[text_column])
df[text_column] = df[text_column].astype(str)

df['tokens'] = df[text_column].apply(lambda x: x.split())

df = df[df['tokens'].map(len) >= 3]

sentences = df['tokens'].tolist()

num_docs = len(sentences)
num_tokens = sum(len(doc) for doc in sentences)

print("\n" + "="*40)
print(f"Використане поле: {text_column}")
print(f"Документів у тренувальному корпусі: {num_docs}")
print(f"Загальна кількість токенів: {num_tokens}")
print("="*40 + "\n")

print("Приклад токенізації (перший документ):")
print(sentences[0][:15], "...\n")

import gensim
from gensim.models import Word2Vec, FastText

print("Доочищення токенів (видалення пунктуації та нижній регістр)...")
df['clean_tokens'] = df['text'].apply(lambda x: gensim.utils.simple_preprocess(x, deacc=False))

df = df[df['clean_tokens'].map(len) >= 3]
sentences = df['clean_tokens'].tolist()

print(f"Приклад чистої токенізації: {sentences[0][:10]}...\n")

VECTOR_SIZE = 100
WINDOW = 5
MIN_COUNT = 3
SG = 1 

print("Тренування Word2Vec...")
w2v_model = Word2Vec(
    sentences=sentences, 
    vector_size=VECTOR_SIZE, 
    window=WINDOW, 
    min_count=MIN_COUNT, 
    sg=SG,
    workers=4 
)
print("Word2Vec натреновано!\n")

print("Тренування FastText...")
ft_model = FastText(
    sentences=sentences, 
    vector_size=VECTOR_SIZE, 
    window=WINDOW, 
    min_count=MIN_COUNT, 
    sg=SG,
    workers=4
)
print("FastText натреновано!")