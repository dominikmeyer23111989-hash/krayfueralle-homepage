import os
import requests
import feedparser

# Konfiguration aus GitHub Secrets laden
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
RSS_FEED_URL = "https://rss.app/feeds/Ov1YRUfI0cPlLS2C.xml"

def sync_feed():
    print("Lese RSS-Feed aus...")
    feed = feedparser.parse(RSS_FEED_URL)
    
    if not feed.entries:
        print("Keine Einträge im Feed gefunden.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" # Verhindert doppelte Einträge, falls ein Unique Key existiert
    }

    # Die neuesten Beiträge durchgehen (z. B. die letzten 5)
    for entry in feed.entries[:5]:
        title = entry.get("title", "Facebook Beitrag")
        link = entry.get("link", "")
        published = entry.get("published", "")
        description = entry.get("description", "")
        
        # Bild-URL aus dem Feed extrahieren (falls vorhanden)
        image_url = None
        if "media_content" in entry and entry.media_content:
            image_url = entry.media_content[0].get("url")
        elif "enclosures" in entry and entry.enclosures:
            image_url = entry.enclosures[0].get("href")

        payload = {
            "titel": title[:100], # Kürzen falls zu lang
            "inhalt": description,
            "bild_url": image_url,
            "autor": "KrayFürAlle (Facebook-Bot)",
            "created_at": published if published else None
        }

        # An Supabase senden (Tabelle: 'aktuelles')
        url = f"{SUPABASE_URL}/rest/v1/aktuelles"
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"Erfolgreich synchronisiert: {title}")
        else:
            print(f"Fehler bei {title}: {response.text}")

if __name__ == "__main__":
    sync_feed()
