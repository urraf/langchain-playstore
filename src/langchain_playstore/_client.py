"""Google Play Store client wrapper.

Provides a clean interface for interacting with the Google Play Store
using the unofficial google-play-scraper package. No API keys required.
"""

from __future__ import annotations

from typing import Any
import re
from google_play_scraper import app, reviews, Sort

class PlayStoreClient:
    """Wrapper around google-play-scraper."""
    
    # Regex to extract app ID (package name) from a Play Store URL
    PLAY_URL_PATTERN = re.compile(r"id=([a-zA-Z0-9._]+)")
    
    def __init__(self, lang: str = "en", country: str = "us") -> None:
        self.lang = lang
        self.country = country

    def get_app_details(self, app_id: str) -> dict[str, Any]:
        """Fetch details for a specific app.
        
        Args:
            app_id: The Android package name (e.g., 'com.google.android.youtube').
            
        Returns:
            Dictionary containing app details.
        """
        try:
            result = app(
                app_id,
                lang=self.lang,
                country=self.country
            )
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Play Store app details for '{app_id}': {e}") from e

    def get_app_reviews(
        self,
        app_id: str,
        max_results: int = 100,
        sort: str = "newest"
    ) -> list[dict[str, Any]]:
        """Fetch user reviews for a specific app.
        
        Args:
            app_id: The Android package name.
            max_results: Maximum number of reviews to return.
            sort: 'newest', 'rating', or 'helpfulness'.
            
        Returns:
            List of review dictionaries.
        """
        if sort == "newest":
            sort_enum = Sort.NEWEST
        elif sort == "rating":
            sort_enum = Sort.RATING
        elif sort == "helpfulness":
            sort_enum = Sort.MOST_RELEVANT
        else:
            raise ValueError(f"Invalid sort option: '{sort}'. Use 'newest', 'rating', or 'helpfulness'.")
            
        try:
            result, _ = reviews(
                app_id,
                lang=self.lang,
                country=self.country,
                sort=sort_enum,
                count=max_results
            )
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Play Store reviews for '{app_id}': {e}") from e

    @classmethod
    def extract_app_id(cls, url_or_id: str) -> str:
        """Extract app ID from a play.google.com URL or raw ID."""
        url_or_id = str(url_or_id).strip()
        
        match = cls.PLAY_URL_PATTERN.search(url_or_id)
        if match:
            return match.group(1)
            
        # If it looks like a package name (e.g., com.example.app)
        if "." in url_or_id and not url_or_id.startswith("http"):
            return url_or_id
            
        raise ValueError(f"Could not extract a Google Play Store app ID from: '{url_or_id}'")
