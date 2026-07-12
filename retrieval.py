def search(query,model,collection,k=3):
    query_vec = model.encode([query]).tolist()
    result = collection.query(
        query_embeddings = query_vec,
        n_results = k
    )
    return result["documents"][0]