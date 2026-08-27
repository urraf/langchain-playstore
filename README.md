# 🚀 langchain-playstore

[![PyPI version](https://badge.fury.io/py/langchain-playstore.svg)](https://badge.fury.io/py/langchain-playstore)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**LangChain retrievers for the Google Play Store** — fetch app details and retrieve user reviews as LangChain `Document` objects. **No API keys required**.

Perfect for building RAG applications that can analyze app store feedback, monitor sentiment, or scrape competitor features.

## ✨ Features

| Retriever | What it does | API Key Required? |
|---|---|---|
| `PlayStoreAppRetriever` | Fetch full metadata/details of an app | ❌ No! |
| `PlayStoreReviewsRetriever` | Fetch user reviews for an app | ❌ No! |

## 📦 Installation

```bash
pip install langchain-playstore
```

## 🚀 Quick Start

### Fetch App Details

```python
from langchain_playstore import PlayStoreAppRetriever

retriever = PlayStoreAppRetriever(
    lang="en",      # Default is "en"
    country="us"    # Default is "us"
)

# You can pass the app package ID or a full Play Store URL
docs = retriever.invoke("com.google.android.youtube")

app_metadata = docs[0].metadata
print(f"Name: {app_metadata['title']}")
print(f"Developer: {app_metadata['developer']}")
print(f"Score: {app_metadata['score']} / 5.0")
print(f"Installs: {app_metadata['installs']}")
```

### Fetch App Reviews

```python
from langchain_playstore import PlayStoreReviewsRetriever

retriever = PlayStoreReviewsRetriever(
    lang="en",
    country="us",
    max_results=5,
    sort="helpfulness", # "helpfulness", "newest", "rating"
)

docs = retriever.invoke("https://play.google.com/store/apps/details?id=com.whatsapp")

for doc in docs:
    print(f"⭐ {doc.metadata['score']} / 5")
    print(f"💬 {doc.page_content}")
    print(f"👍 {doc.metadata['thumbs_up']} upvotes\n")
```

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
