from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL,CHROMA_DB_PATH,COLLECTION_NAME
import chromadb
import os
import glob

def build_vectorstore():
    text = ""
    for filepath in glob.glob("data/*.pdf"):
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text()
    for filepath in glob.glob("data/*.txt"):
        with open(filepath, "r", encoding = "utf-8") as f:
            text += f.read()
    print("知识库加载完成")
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    chunks=splitter.split_text(text)
    print("chunk已生成")
    model=SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(
        path = CHROMA_DB_PATH
    )
    collection_name = COLLECTION_NAME

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