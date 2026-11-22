"""Page through Steam Community reviews by following the hidden form each page carries.
Usage: python3 community_paged.py APPID OUT.jsonl"""
import sys, re, json, time, urllib.parse
sys.path.insert(0, __file__.rsplit("/", 1)[0])
src = open(__file__.rsplit("/", 1)[0] + "/community_reviews.py").read().split("for filt, pages")[0]
sys_argv = sys.argv[:]
exec(src)  # defines get(), parse(), rows, seen (appid/out from argv)

def form_of(h):
    return dict(re.findall(r'name="([a-zA-Z_]+)" value="([^"]*)"', h))

for filt, pages in (("toprated", 30), ("mostrecent", 20)):
    h = get(f"https://steamcommunity.com/app/{appid}/reviews/?browsefilter={filt}&filterLanguage=all&p=1")
    print(filt, 1, parse(h, filt), file=sys.stderr)
    for p in range(2, pages + 1):
        q = form_of(h)
        if "userreviewscursor" not in q:
            break
        q.update({"appid": appid, "browsefilter": filt})
        time.sleep(1.1)
        try:
            h = get(f"https://steamcommunity.com/app/{appid}/homecontent/?" + urllib.parse.urlencode(q))
        except Exception as e:
            print("stop", filt, p, e, file=sys.stderr); break
        got = parse(h, filt)
        print(filt, p, got, file=sys.stderr)
        if got == 0:
            break

with open(out, "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
pos = sum(r["positive"] for r in rows)
print(f"reviews: {len(rows)}, positive {pos}, negative {len(rows) - pos}")
