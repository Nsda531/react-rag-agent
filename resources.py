from embedding import build_vectorstore

chunks, model, collection = build_vectorstore()
RESOURCES = {
    "model": model,
    "chunks": chunks,
    "collection": collection,
}
