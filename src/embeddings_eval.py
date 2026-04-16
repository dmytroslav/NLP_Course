def compare_neighbors(word, topn=5):
    print(f"\n{'='*40}")
    print(f" Аналіз слова: '{word}'")
    print(f"{'='*40}")
    
    # Word2Vec
    print(f" Word2Vec:")
    try:
        w2v_res = w2v_model.wv.most_similar(word, topn=topn)
        for w, score in w2v_res:
            print(f"   {w} ({score:.3f})")
    except KeyError:
        print(f" Відсутнє у словнику (OOV - Out Of Vocabulary)")
        
    # FastText
    print(f"\n FastText:")
    try:
        ft_res = ft_model.wv.most_similar(word, topn=topn)
        for w, score in ft_res:
            print(f"   {w} ({score:.3f})")
    except KeyError:
        print(f"   Відсутнє у словнику (OOV)")

words_to_test = [
    "україна",     # 1. Загальне часте
    "ракетний",    # 2. Доменне (часте)
    "тривога",     # 3. Доменне
    "зсу",         # 4. Абревіатура / специфічне
    "ппо",         # 5. Абревіатура
    "блекаут",     # 6. Неологізм / запозичення
    "русня",       # 7. Сленг / noisy text
    "бахмут",      # 8. Власна назва (географія)
    "допомога",    # 9. Загальне слово (політика/економіка)
    "повідомляють" # 10. Шаблонна лексика (з ЛР8)
]

for w in words_to_test:
    compare_neighbors(w)