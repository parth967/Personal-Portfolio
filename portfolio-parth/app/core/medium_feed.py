import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict

MEDIUM_FEED_URL = "https://medium.com/feed/@pparth967"
CACHE_TTL_SECONDS = 1800
_cache: List[Dict] = []
_cache_time: float = 0


def _strip_html(html: str, max_len: int = 200) -> str:
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len] + ("..." if len(text) > max_len else "")


def _first_image_from_content(content: str) -> str:
    if not content:
        return ""
    img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.I)
    for url in img_matches:
        if url and isinstance(url, str):
            url = url.strip()
            if url and not any(x in url.lower() for x in ['stat?', 'tracking', 'analytics', 'pixel', 'beacon', '1x1', 'blank', '_/stat']):
                if url.startswith('http'):
                    if 'miro.medium.com' in url or 'cdn-images' in url or 'medium.com' in url:
                        clean_url = url.split('?')[0].split('&')[0]
                        if clean_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                            return clean_url
                        elif 'miro.medium.com' in clean_url or 'cdn-images' in clean_url:
                            return clean_url
                    return url
                elif url.startswith('//'):
                    return f"https:{url}"
    return ""


def fetch_medium_posts() -> List[Dict]:
    global _cache, _cache_time
    if _cache and (time.time() - _cache_time) < CACHE_TTL_SECONDS:
        return _cache
    posts = []
    try:
        req = urllib.request.Request(
            MEDIUM_FEED_URL,
            headers={"User-Agent": "Mozilla/5.0 (compatible; Portfolio/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
        content_ns = "http://purl.org/rss/1.0/modules/content/"
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            desc_el = item.find("description")
            content_el = item.find(f"{{{content_ns}}}encoded")
            content_raw = (content_el.text or "") if content_el is not None else ""
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.text or "").strip() if link_el is not None else ""
            desc = (desc_el.text or "").strip() if desc_el is not None else ""
            excerpt = _strip_html(desc or content_raw, 200)
            img = _first_image_from_content(content_raw or desc)
            if not img:
                for child in item:
                    if child.tag and "content" in child.tag.lower() and child.get("url"):
                        candidate = child.get("url", "")
                        if candidate and not any(x in candidate.lower() for x in ['stat?', 'tracking']):
                            img = candidate
                            break
            if not img:
                img = ""
            posts.append({
                "Title": title,
                "ShortContent": excerpt or "Read more on Medium.",
                "Url": link,
                "Image": img or "",
            })
    except Exception:
        posts = []
    _cache = posts
    _cache_time = time.time()
    return posts
