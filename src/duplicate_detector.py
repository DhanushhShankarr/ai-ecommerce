import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity

base_path = os.path.dirname(os.path.dirname(__file__))

df = pickle.load(open(os.path.join(base_path, "models/data.pkl"), "rb"))
vectors = pickle.load(open(os.path.join(base_path, "models/vectors.pkl"), "rb"))

sim_matrix = cosine_similarity(vectors)

def find_duplicates_for_product(product_name, threshold=0.9, top_n=5):

    if product_name not in df['product_name'].values:
        return []

    idx = df[df['product_name'] == product_name].index[0]

    scores = list(enumerate(sim_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    duplicates = []

    for i, score in scores[1:]:
        if score >= threshold:
            duplicates.append({
                "product": df.iloc[i]['product_name'],
                "similarity": float(score)
            })

    return duplicates[:top_n]