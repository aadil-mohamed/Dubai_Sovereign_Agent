import logging
from langchain_core.tools import tool
from vector_store import vector_db

logger = logging.getLogger(__name__)

@tool
def legal_rag_tool(query: str) -> str:
    """
    Searches the PropIQ Sovereign Database for Dubai real estate laws, 
    regulations, and legal precedents.
    """
    logger.info(f"Executing Legal RAG Search for: {query}")
    try:
        results = vector_db.retrieve_precedents(query, top_k=4)
        if not results:
            return "No relevant legal precedents found in the database."
        
        formatted_results = []
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown Regulation')
            formatted_results.append(f"--- Document {i} ({source}) ---\n{doc.page_content}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        logger.error(f"RAG Tool Error: {e}")
        return f"CRITICAL: Error accessing legal vector database: {str(e)}"
def query_legal(query: str) -> str:
    """Wrapper to comply with deployment function naming standards."""
    return legal_rag_tool.invoke(query)    