import os
import requests
import feedparser

# Secrets aus den Umgebungsvariablen laden
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

# Deine NEUE RSS-Feed-URL
FEED_URL = "https://rss.app/feeds/I0SLdMp2Hine8Hkx.xml"

print("=== START FACEBOOK SYNC ===")

# 1. Secrets-Check
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ FEHLER: SUPABASE_URL oder SUPABASE_SERVICE_ROLE_KEY fehlt in den Secrets!")
    exit(1)
else:
    print("✅ Secrets erfolgreich geladen.")

# 2. Feed auslesen
print(f"Hole Daten von RSS-Feed: {FEED_URL}")
feed = feedparser.parse(FEED_URL)

print(f"Gefundene Feed-Einträge: {len(feed.entries)}")

if len(feed.entries) == 0:
    print("⚠️ WARNUNG: Der RSS-Feed liefert 0 Einträge! Prüfe die RSS-URL.")
    exit(0)

# 3. Posts aufbereiten
posts = []
for entry in feed.entries[:5]:  # Die neuesten 5 Posts
    titel = entry.get("title", "Neuer Beitrag")
    inhalt = entry.get("summary", entry.get("description", ""))
    
    bild_url = None
    if "enclosures" in entry and len(entry.enclosures) > 0:
        bild_url = entry.enclosures[0].get("href")
    elif "media_content" in entry and len(entry.media_content) > 0:
        bild_url = entry.media_content[0].get("url")

    posts.append({
        "titel": titel[:150],
        "inhalt": inhalt,
        "autor": "Facebook",
        "bild_url": bild_url
    })

# 4. An Supabase senden
endpoint = f"{SUPABASE_URL}/rest/v1/aktuelles"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

print(f"Sende {len(posts)} Posts an Supabase REST API ({endpoint})...")
response = requests.post(endpoint, headers=headers, json=posts)

if response.status_code in [200, 201]:
    print("🎉 SUCCESS: Posts erfolgreich in Supabase gespeichert!")
else:
    print(f"❌ SUPABASE FEHLER (Status {response.status_code}):")
    print(response.text)

print("=== END SYNC ===")
