# 📊 BigQuery Release Notes Dashboard

A sleek, dark-themed web dashboard that fetches and displays the latest **Google BigQuery release notes** in real time — with live search, category filtering, and auto-refreshing from the official Google Cloud Atom feed.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- **Live feed** — Pulls directly from the official [BigQuery release notes Atom feed](https://docs.cloud.google.com/feeds/bigquery-release-notes.xml)
- **Smart caching** — In-memory cache with a 5-minute TTL; graceful fallback to stale cache on network errors
- **Instant search** — Filter releases by keyword with highlighted match results
- **Category filters** — Auto-classifies each release as Feature, Fix, Preview, Deprecation, Breaking Change, or Other
- **Expandable cards** — Collapsible HTML-rendered content with a "Read more / Show less" toggle
- **Skeleton loader** — Animated placeholders shown while data loads
- **Status indicator** — Live / Cached / Error dot with last-updated timestamp
- **One-click refresh** — Force a fresh fetch bypassing the cache
- **Responsive layout** — Works on desktop and mobile

---

## 🖥️ Screenshot

> The dashboard on first load, showing the skeleton loader transitioning into release cards.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mhrshgh/mehrnaz-bq-release-notes.git
cd mehrnaz-bq-release-notes

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install flask
```

### Running the App

```bash
python app.py
```

Then open your browser at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## 📁 Project Structure

```
mehrnaz-bq-release-notes/
├── app.py                  # Flask backend — feed fetcher, cache, API routes
├── templates/
│   └── index.html          # Single-page dashboard UI (HTML + CSS + JS)
└── .gitignore
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the dashboard HTML |
| `GET` | `/api/releases` | Returns cached or freshly fetched release notes as JSON |
| `GET` | `/api/releases?refresh=true` | Forces a live fetch, bypassing the cache |

### Example response

```json
{
  "status": "success",
  "source": "network",
  "last_updated": 1750000000.0,
  "releases": [
    {
      "title": "BigQuery now supports ...",
      "id": "https://cloud.google.com/...",
      "updated": "2026-06-10T00:00:00+00:00",
      "link": "https://cloud.google.com/bigquery/docs/release-notes#june_10_2026",
      "content": "<p>HTML content here</p>"
    }
  ]
}
```

---

## ⚙️ Configuration

Two constants at the top of `app.py` can be adjusted:

| Constant | Default | Description |
|----------|---------|-------------|
| `FEED_URL` | Google Cloud BigQuery feed URL | The Atom feed to fetch from |
| `CACHE_DURATION` | `300` (5 min) | Seconds before the cache is considered stale |

---

## 🛠️ Built With

- **[Flask](https://flask.palletsprojects.com/)** — Python web framework
- **[Google Cloud Atom Feed](https://docs.cloud.google.com/feeds/bigquery-release-notes.xml)** — Data source
- **Vanilla HTML / CSS / JavaScript** — No frontend dependencies
- **[Inter](https://fonts.google.com/specimen/Inter)** — Google Fonts typeface

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
