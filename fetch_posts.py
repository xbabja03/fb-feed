import os, json, requests
from datetime import datetime

ACCESS_TOKEN = os.getenv("FB_PAGE_TOKEN")
PAGE_ID = "VAGRetrofits"  # alebo skutočné ID stránky
LIMIT = 100  # max počet príspevkov na jedno volanie

def fetch_all_posts():
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/posts"
    params = {"access_token": ACCESS_TOKEN, "fields": "id,message,created_time,full_picture,permalink_url,likes.summary(true)", "limit": LIMIT}
    posts = []
    while True:
        resp = requests.get(url, params=params).json()
        posts.extend(resp.get("data", []))
        next_page = resp.get("paging", {}).get("next")
        if not next_page: break
        url = next_page
        params = {}  # next_url má všetko
    return posts

def main():
    posts = fetch_all_posts()
    posts.sort(key=lambda x: int(x.get('likes', {}).get('summary', {}).get('total_count', 0)), reverse=True)
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump({"generated": datetime.utcnow().isoformat(), "posts": posts}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
