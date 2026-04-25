import os
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

base_path = os.path.dirname(os.path.dirname(__file__))

df = pickle.load(open(os.path.join(base_path, "models/data.pkl"), "rb"))
vectors = pickle.load(open(os.path.join(base_path, "models/vectors.pkl"), "rb"))

sim_matrix = cosine_similarity(vectors)

# ---------------------------
# RECOMMEND WITH IMAGE + DISCOUNT
# ---------------------------
def recommend_with_discount(product_name, discount_percent=0, top_n=5):

    if product_name not in df['product_name'].values:
        return pd.DataFrame()

    idx = df[df['product_name'] == product_name].index[0]

    scores = list(enumerate(sim_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:]

    results = []

    for i, score in scores:
        row = df.iloc[i]

        price = row.get("retail_price", 0)
        if pd.isnull(price):
            continue

        discounted = price * (1 - discount_percent / 100)

        # 🖼️ Placeholder image (Flipkart-style simulation)
        image_url = f"https://via.placeholder.com/150?text=Product"

        results.append({
            "product_name": row['product_name'],
            "original_price": price,
            "discounted_price": round(discounted, 2),
            "image": image_url,
            "similarity": score
        })

    return pd.DataFrame(results).head(top_n)