"""LangChain Google Play Store integration.

Retrievers for fetching app details and user reviews from the Google Play Store.

Install:
    pip install langchain-playstore

Usage:
    from langchain_playstore import PlayStoreAppRetriever, PlayStoreReviewsRetriever

    # Fetch app details
    app_retriever = PlayStoreAppRetriever()
    docs = app_retriever.invoke("com.google.android.youtube")

    # Fetch app reviews
    reviews_retriever = PlayStoreReviewsRetriever(max_results=50, sort="helpfulness")
    docs = reviews_retriever.invoke("com.google.android.youtube")
"""

from langchain_playstore.retrievers import (
    PlayStoreAppRetriever,
    PlayStoreReviewsRetriever,
)

__all__ = [
    "PlayStoreAppRetriever",
    "PlayStoreReviewsRetriever",
]

__version__ = "0.1.0"
