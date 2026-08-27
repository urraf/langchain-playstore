"""LangChain retrievers for Google Play Store data.

This module provides two retrievers for fetching Play Store data
as LangChain Document objects:

- PlayStoreAppRetriever: Fetch detailed information about an app.
- PlayStoreReviewsRetriever: Fetch user reviews for an app.
"""

from __future__ import annotations

from typing import Any
import json

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field, PrivateAttr

from langchain_playstore._client import PlayStoreClient


class PlayStoreAppRetriever(BaseRetriever):
    """Fetch detailed information about a Google Play Store app."""
    
    lang: str = Field(
        default="en",
        description="Language code for the Play Store (e.g., 'en', 'es')."
    )
    country: str = Field(
        default="us",
        description="Country code for the Play Store (e.g., 'us', 'uk')."
    )
    
    _client: PlayStoreClient = PrivateAttr()
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize the Play Store API client."""
        super().model_post_init(__context)
        self._client = PlayStoreClient(lang=self.lang, country=self.country)
        
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        """Fetch app details and return as a single Document."""
        app_id = self._client.extract_app_id(query)
        details = self._client.get_app_details(app_id=app_id)
        
        content = f"App Name: {details.get('title')}\n"
        content += f"Developer: {details.get('developer')}\n"
        
        description = details.get('description', '')
        if description:
            content += f"\nDescription:\n{description}\n"
            
        metadata = {
            "source": "playstore_app_details",
            "app_id": details.get("appId", app_id),
            "title": details.get("title", ""),
            "developer": details.get("developer", ""),
            "url": details.get("url", ""),
            "score": details.get("score", 0.0),
            "ratings": details.get("ratings", 0),
            "reviews": details.get("reviews", 0),
            "price": details.get("price", 0.0),
            "currency": details.get("currency", ""),
            "free": details.get("free", True),
            "genre": details.get("genre", ""),
            "installs": details.get("installs", ""),
            "released": details.get("released", ""),
            "updated": details.get("updated", 0),
            "version": details.get("version", ""),
            "contentRating": details.get("contentRating", ""),
        }
        
        return [Document(page_content=content.strip(), metadata=metadata)]


class PlayStoreReviewsRetriever(BaseRetriever):
    """Fetch user reviews for a Google Play Store app."""
    
    lang: str = Field(
        default="en",
        description="Language code for the Play Store (e.g., 'en', 'es')."
    )
    country: str = Field(
        default="us",
        description="Country code for the Play Store (e.g., 'us', 'uk')."
    )
    max_results: int = Field(
        default=50,
        description="Maximum number of reviews to return."
    )
    sort: str = Field(
        default="helpfulness",
        description="Sort order. Options: 'newest', 'rating', 'helpfulness'."
    )
    
    _client: PlayStoreClient = PrivateAttr()
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize the Play Store API client."""
        super().model_post_init(__context)
        self._client = PlayStoreClient(lang=self.lang, country=self.country)
        
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        """Fetch app reviews and return as Documents."""
        app_id = self._client.extract_app_id(query)
        reviews_data = self._client.get_app_reviews(
            app_id=app_id,
            max_results=self.max_results,
            sort=self.sort,
        )
        
        documents: list[Document] = []
        for review in reviews_data:
            content = review.get("content", "")
            
            metadata = {
                "source": "playstore_reviews",
                "app_id": app_id,
                "review_id": review.get("reviewId", ""),
                "author": review.get("userName", ""),
                "score": review.get("score", 0),
                "thumbs_up": review.get("thumbsUpCount", 0),
                "version": review.get("reviewCreatedVersion", ""),
                "at": review.get("at", None),
                "reply_content": review.get("replyContent", ""),
                "replied_at": review.get("repliedAt", None),
            }
            
            # Convert datetime objects to string for metadata serialization
            if metadata["at"]:
                metadata["at"] = str(metadata["at"])
            if metadata["replied_at"]:
                metadata["replied_at"] = str(metadata["replied_at"])
                
            documents.append(Document(page_content=content, metadata=metadata))
            
        return documents
