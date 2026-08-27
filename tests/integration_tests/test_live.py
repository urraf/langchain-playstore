import pytest
from langchain_playstore import (
    PlayStoreAppRetriever,
    PlayStoreReviewsRetriever
)

def test_app_retriever():
    retriever = PlayStoreAppRetriever()
    docs = retriever.invoke("com.whatsapp")
    
    assert len(docs) == 1
    assert docs[0].metadata["source"] == "playstore_app_details"
    assert "WhatsApp" in docs[0].metadata["title"] or "WhatsApp" in docs[0].page_content
    assert docs[0].metadata["app_id"] == "com.whatsapp"

def test_reviews_retriever():
    retriever = PlayStoreReviewsRetriever(max_results=5)
    docs = retriever.invoke("https://play.google.com/store/apps/details?id=com.whatsapp")
    
    assert len(docs) > 0
    assert docs[0].metadata["source"] == "playstore_reviews"
    assert docs[0].metadata["app_id"] == "com.whatsapp"
    assert "score" in docs[0].metadata
