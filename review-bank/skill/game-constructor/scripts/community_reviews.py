"""Collect public Steam Community reviews for an app (HTML pages), 1 request per second.
Usage: python3 community_reviews.py APPID OUT.jsonl"""
import sys, re, json, time, html, urllib.request, urllib.parse

appid, out = sys.argv[1], sys.argv[2]
seen, rows = set(), []

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def parse(h, src):
    n = 0
    for card in re.split(r'class="apphub_Card modalContentLink', h)[1:]:
        title = re.search(r'<div class="title">([^<]*)</div>', card)
        hours = re.search(r'<div class="hours">([^<]*)</div>', card)
        body = re.search(r'apphub_CardTextContent">\s*(?:<div class="date_posted">.*?</div>)?(.*?)</div>', card, re.S)
        link = re.search(r'data-modal-content-url="(https://steamcommunity\.com/(?:id|profiles)/[^"]+/recommended/\d+/?)"', card)
        if not (title and body):
            continue
        text = html.unescape(re.sub(r"<br\s*/?>", "\n", body.group(1)))
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"^\s*Posted:[^\n]*\n", "", text.strip()).strip()
        key = (link.group(1) if link else text[:80])
        if key in seen:
            continue
        seen.add(key); n += 1
        hrs = re.search(r"([\d.,]+)\s*hrs", hours.group(1)) if hours else None
        rows.append({"positive": title.group(1).strip() == "Recommended", "hours": float(hrs.group(1).replace(",", "")) if hrs else None,
                     "text": text, "url": link.group(1) if link else None, "source": src})
    return n

for filt, pages in (("toprated", 25), ("mostrecent", 15)):
    for p in range(1, pages + 1):
        q = {"userreviewsoffset": (p - 1) * 10, "p": p, "workshopitemspage": p, "readytouseitemspage": p, "mtxitemspage": p,
             "itemspage": p, "screenshotspage": p, "videospage": p, "artpage": p, "allguidepage": p, "webguidepage": p,
             "integratedguidepage": p, "discussionspage": p, "numperpage": 10, "browsefilter": filt, "appid": appid,
             "appHubSubSection": 10, "l": "english", "filterLanguage": "all", "searchText": "", "maxInappropriateScore": 50, "forceanon": 1}
        try:
            h = get(f"https://steamcommunity.com/app/{appid}/homecontent/?" + urllib.parse.urlencode(q))
        except Exception as e:
            print("stop", filt, p, e); break
        got = parse(h, filt)
        print(filt, p, got, file=sys.stderr)
        if got == 0 and p > 1:
            break
        time.sleep(1.1)

with open(out, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
pos = sum(r["positive"] for r in rows)
print(f"reviews: {len(rows)}, positive {pos}, negative {len(rows) - pos}")
