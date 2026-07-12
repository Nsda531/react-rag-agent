from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import os

def build_vectorstore():
    reader=PdfReader("data/午餐科学搭配与食谱大全.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    print("知识库加载完成")
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    chunks=splitter.split_text(text)
    print("chunk已生成")
    model=SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(
        path = os.path.join("data", "chroma_db")
    )
    collection_name = "lunch_knowledge"

    try:
        collection = client.get_collection(collection_name)
        print("ChromaDB 已有数据，直接加载")
    except Exception:
        collection = client.create_collection(collection_name)
        print("首次建库，正在向量化并入ChromaDB")
        embeddings = model.encode(chunks)   #生成向量   
        collection.add(
            embeddings = embeddings.tolist(),
            documents = chunks,
            ids = [f"chunk_{i}" for i in range(len(chunks))]
        )
        print("ChromaDB 索引已建立并持久化")
    return chunks, model, collection