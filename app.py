from flask import Flask, render_template, jsonify, request
import urllib.request
import xml.etree.ElementTree as ET
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"
CACHE_DURATION = 300  # 5 minutes in seconds

# Simple in-memory cache
feed_cache = {
    "data": None,
    "last_fetched": 0
}

def parse_release_feed():
    logger.info("Fetching and parsing BigQuery release notes XML feed...")
    try:
        req = urllib.request.Request(
            FEED_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"
        
        entries = []
        for entry_el in root.findall(f"{ns}entry"):
            title_el = entry_el.find(f"{ns}title")
            id_el = entry_el.find(f"{ns}id")
            updated_el = entry_el.find(f"{ns}updated")
            content_el = entry_el.find(f"{ns}content")
            
            link_href = ""
            # Look for link tags
            links = entry_el.findall(f"{ns}link")
            for link in links:
                rel = link.attrib.get("rel", "alternate")
                if rel == "alternate" or not rel:
                    link_href = link.attrib.get("href", "")
                    break
            if not link_href and links:
                link_href = links[0].attrib.get("href", "")
            
            entries.append({
                "title": title_el.text if title_el is not None else "",
                "id": id_el.text if id_el is not None else "",
                "updated": updated_el.text if updated_el is not None else "",
                "link": link_href,
                "content": content_el.text if content_el is not None else ""
            })
            
        return entries, None
    except Exception as e:
        logger.error(f"Error fetching/parsing feed: {str(e)}")
        return None, str(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/releases")
def get_releases():
    force_refresh = request.args.get("refresh", "false").lower() == "true"
    current_time = time.time()
    
    # Check cache
    if not force_refresh and feed_cache["data"] is not None and (current_time - feed_cache["last_fetched"]) < CACHE_DURATION:
        logger.info("Returning cached release notes.")
        return jsonify({
            "status": "success",
            "source": "cache",
            "last_updated": feed_cache["last_fetched"],
            "releases": feed_cache["data"]
        })
    
    # Fetch new data
    releases, error = parse_release_feed()
    if error:
        # If fetch fails but we have cached data, fall back to cache
        if feed_cache["data"] is not None:
            logger.warning("Fetch failed, falling back to cached data.")
            return jsonify({
                "status": "warning",
                "source": "cache_fallback",
                "error": error,
                "last_updated": feed_cache["last_fetched"],
                "releases": feed_cache["data"]
            })
        return jsonify({
            "status": "error",
            "message": "Failed to fetch release notes from Google Cloud.",
            "error": error
        }), 500
        
    # Update cache
    feed_cache["data"] = releases
    feed_cache["last_fetched"] = current_time
    
    return jsonify({
        "status": "success",
        "source": "network",
        "last_updated": current_time,
        "releases": releases
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
