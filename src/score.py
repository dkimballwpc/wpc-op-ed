from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

WPC_TOPICS = {
    "budget_and_taxes": {
        "keywords": ["budget", "tax", "taxes", "spending", "government reform", "revenue", "fiscal"],
        "description": "WPC research on budget, taxes, and government spending"
    },
    "education": {
        "keywords": ["education", "school", "schools", "students", "teachers", "learning", "curriculum"],
        "description": "WPC research on education policy and schools"
    },
    "environment": {
        "keywords": ["environment", "energy", "climate", "data center", "carbon", "emissions", "pollution"],
        "description": "WPC research on environment and energy policy"
    },
    "health_care": {
        "keywords": ["health care", "healthcare", "insurance", "medical", "hospital", "coverage"],
        "description": "WPC research on health care policy"
    },
    "small_business": {
        "keywords": ["small business", "business", "regulation", "entrepreneur", "startup", "commerce"],
        "description": "WPC research on small business and regulation"
    },
    "transportation": {
        "keywords": ["transportation", "roads", "traffic", "transit", "highway", "transport"],
        "description": "WPC research on transportation and infrastructure"
    },
    "worker_rights": {
        "keywords": ["worker", "labor", "union", "employment", "wage", "workforce"],
        "description": "WPC research on worker rights and labor policy"
    },
    "tech_telecom": {
        "keywords": ["technology", "tech", "telecom", "broadband", "internet", "digital"],
        "description": "WPC research on technology and telecom policy"
    }
}

def cluster_by_topic(news_items):
    """Group similar news items into topics"""
    if not news_items:
        return []
    
    texts = [f"{x['title']} {x['summary']}" for x in news_items]
    
    vec = TfidfVectorizer(stop_words="english", max_features=1000)
    X = vec.fit_transform(texts)
    
    feature_names = vec.get_feature_names_out()
    topic_words = []
    for i, row in enumerate(X):
        if row.nnz > 0:
            indices = row.indices
            data = row.data
            top_idx = indices[data.argmax()]
            topic_words.append(feature_names[top_idx])
    
    clusters = defaultdict(list)
    for item, kw in zip(news_items, topic_words):
        clusters[kw].append(item)
    
    topics = []
    for keyword, items in clusters.items():
        if len(items) >= 1:
            wa_count = sum(1 for x in items if x.get("source_type") == "washington")
            national_count = len(items) - wa_count
            topics.append({
                "keyword": keyword,
                "items": items,
                "wa_count": wa_count,
                "national_count": national_count,
                "total": len(items)
            })
    
    return sorted(topics, key=lambda x: x["total"], reverse=True)[:10]

def match_to_wpc_topics(clusters):
    """Match clusters to WPC research areas"""
    ranked = []
    
    for cluster in clusters:
        cluster_text = " ".join([f"{x['title']} {x['summary']}" for x in cluster["items"]]).lower()
        
        best_match = None
        best_score = 0
        
        for topic_key, topic_info in WPC_TOPICS.items():
            score = sum(1 for kw in topic_info["keywords"] if kw in cluster_text)
            if score > best_score:
                best_score = score
                best_match = topic_key
        
        if best_match:
            ranked.append({
                **cluster,
                "wpc_topic": best_match,
                "wpc_description": WPC_TOPICS[best_match]["description"],
                "wpc_keywords": WPC_TOPICS[best_match]["keywords"],
                "match_strength": best_score
            })
    
    return sorted(ranked, key=lambda x: (x["match_strength"], x["total"]), reverse=True)[:8]

def generate_explanation(topic):
    """Generate a short explanation of relevance"""
    wa = topic["wa_count"]
    nat = topic["national_count"]
    topic_name = topic["wpc_topic"].replace("_", " ").title()
    
    parts = []
    
    if wa > 0 and nat > 0:
        parts.append(f"Washington coverage: {wa} story/stories")
        parts.append(f"National coverage: {nat} story/stories")
        parts.append(f"This trend is appearing in both Washington and national news.")
    elif wa > 0:
        parts.append(f"Washington coverage: {wa} story/stories")
        parts.append(f"This is primarily a Washington state trend.")
    elif nat > 0:
        parts.append(f"National coverage: {nat} story/stories")
        parts.append(f"This is a national trend with potential Washington relevance.")
    
    parts.append(f"Matches WPC research area: {topic_name}")
    parts.append(f"Relevance: {topic['wpc_description']}")
    
    return " ".join(parts)
