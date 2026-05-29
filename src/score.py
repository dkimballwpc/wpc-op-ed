from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_topics(news_items, wpc_texts):
    if not news_items or not wpc_texts:
        return []

    news_texts = [f"{x.get('title','')} {x.get('summary','')}" for x in news_items]
    all_texts = news_texts + wpc_texts

    vec = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
    X = vec.fit_transform(all_texts)

    sims = cosine_similarity(X[:len(news_items)], X[len(news_items):]).max(axis=1)
    ranked = []
    for item, s in zip(news_items, sims):
        ranked.append({**item, "fit_score": float(s)})

    return sorted(ranked, key=lambda x: x["fit_score"], reverse=True)[:15]
