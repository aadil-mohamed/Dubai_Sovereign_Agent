import os
import logging
from supabase import create_client, Client
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class PropIQVectorStore:
    """
    Production-grade Vector Store connection for PropIQ Legal Agent.
    Handles embedding generation and Supabase pgvector transactions.
    """
    def __init__(self):
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("CRITICAL: Supabase credentials missing from environment variables.")
            
        # Initialize Supabase Client
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # 384-dimension embedding model matching your Supabase VECTOR(384) schema
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.table_name = "propiq_documents"

    def get_store(self) -> SupabaseVectorStore:
        return SupabaseVectorStore(
            client=self.supabase,
            embedding=self.embeddings,
            table_name=self.table_name,
            query_name="match_documents"
        )
        
    def add_legal_documents(self, texts: list[str], metadatas: list[dict] = None):
        """Hashes and uploads legal document chunks to Supabase."""
        try:
            store = self.get_store()
            ids = store.add_texts(texts, metadatas=metadatas)
            logger.info(f"Successfully vectorized and stored {len(ids)} document chunks.")
            return ids
        except Exception as e:
            logger.error(f"Failed to store documents in Supabase: {str(e)}")
            raise

    def retrieve_precedents(self, query: str, top_k: int = 4):
        """Performs cosine similarity search against the vector database."""
        try:
            store = self.get_store()
            results = store.similarity_search(query, k=top_k)
            return results
        except Exception as e:
            logger.error(f"Vector retrieval failed for query '{query}': {str(e)}")
            return []

# Singleton instance for the agent to import
vector_db = PropIQVectorStore()