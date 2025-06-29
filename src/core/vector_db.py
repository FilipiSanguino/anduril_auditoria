import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from google.cloud import storage
import pickle

# Configurações
# Nome do bucket usado para armazenar o indice FAISS
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "anduril-auditoria")
INDEX_FILE_PATH = "vector_db/audit_docs.index"
METADATA_FILE_PATH = "vector_db/audit_docs_meta.pkl"

# Carrega o modelo de embedding (pode levar um tempo no primeiro uso)
print("Carregando modelo de embedding...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Modelo carregado.")

def get_vector_db_from_gcs():
    """Baixa e carrega o índice FAISS e os metadados do GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    
    try:
        # Baixa o índice
        blob_index = bucket.blob(INDEX_FILE_PATH)
        index_data = blob_index.download_as_bytes()
        index = faiss.read_index(faiss.PyCallbackIOReader(index_data.read))

        # Baixa os metadados
        blob_meta = bucket.blob(METADATA_FILE_PATH)
        meta_data = pickle.loads(blob_meta.download_as_string())
        
        return index, meta_data
    except Exception as e:
        print(f"Índice não encontrado ou erro ao carregar: {e}. Criando um novo.")
        dimension = embedding_model.get_sentence_embedding_dimension()
        index = faiss.IndexFlatL2(dimension)
        return index, []

def save_vector_db_to_gcs(index, metadata):
    """Salva o índice FAISS e os metadados no GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # Salva o índice
    writer = faiss.PyCallbackIOWriter(lambda data: None)
    faiss.write_index(index, writer)
    blob_index = bucket.blob(INDEX_FILE_PATH)
    blob_index.upload_from_string(writer.data)

    # Salva os metadados
    blob_meta = bucket.blob(METADATA_FILE_PATH)
    blob_meta.upload_from_string(pickle.dumps(metadata))
    print("Índice e metadados salvos no GCS.")

def add_document(text_chunk: str, source: str, role: str):
    """Adiciona um chunk de texto ao banco de dados vetorial."""
    index, metadata = get_vector_db_from_gcs()
    
    embedding = embedding_model.encode([text_chunk]).astype('float32')
    index.add(embedding)
    metadata.append({"text": text_chunk, "source": source, "role": role})
    
    save_vector_db_to_gcs(index, metadata)

def search_documents(query: str, top_k: int = 5, required_role: str = "auditoria_interna") -> list:
    """Busca por documentos relevantes no banco de dados vetorial."""
    index, metadata = get_vector_db_from_gcs()
    if index.ntotal == 0:
        return [{"text": "O banco de dados vetorial está vazio.", "source": "system"}]

    query_embedding = embedding_model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i in indices[0]:
        # Filtro de acesso simples
        if metadata[i]['role'] == required_role or metadata[i]['role'] == 'public':
            results.append(metadata[i])
            
    return results

