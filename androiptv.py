import os
import re
from playwright.sync_api import sync_playwright

# 1️⃣ Aktif domain bulma
active_domain = None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for i in range(25, 100):
        url = f"https://birazcikspor{i}.xyz/"
        try:
            response = page.goto(url, timeout=10000)
            if response and response.status == 200:
                print(f"✅ Aktif domain bulundu: {url}")
                active_domain = url
                break
        except Exception as e:
            print(f"{url} → Hata: {e}")
            continue

    if not active_domain:
        raise SystemExit("❌ Aktif domain bulunamadı.")

    # 2️⃣ Kanal ID bulma (JS render edilmiş HTML üzerinden)
    content = page.content()
    m = re.search(r'<iframe[^>]+src="event\.html\?id=([^"]+)"', content)
    if not m:
        raise SystemExit("❌ Kanal ID bulunamadı (Playwright ile).")
    
    first_id = m.group(1)
    print("✅ Kanal ID bulundu:", first_id)
    
    browser.close()

# 3️⃣ Base URL çek (requests ile yeterli)
import requests

event_source = requests.get(active_domain + "event.html?id=" + first_id, timeout=10).text
b = re.search(r'var\s+baseurls\s*=\s*\[\s*"([^"]+)"', event_source)
if not b:
    raise SystemExit("❌ Base URL bulunamadı.")
base_url = b.group(1)

# 4️⃣ Kanal listesi
channels = [
     ("beIN Sport 1 HD","androstreamlivebs1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("beIN Sport 2 HD","androstreamlivebs2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("beIN Sport 3 HD","androstreamlivebs3","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("beIN Sport 4 HD","androstreamlivebs4","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("beIN Sport 5 HD","androstreamlivebs5","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("beIN Sport Max 1 HD","androstreamlivebsm1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("beIN Sport Max 2 HD","androstreamlivebsm2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("S Sport 1 HD","androstreamlivess1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("S Sport 2 HD","androstreamlivess2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tivibu Sport HD","androstreamlivets","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tivibu Sport 1 HD","androstreamlivets1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tivibu Sport 2 HD","androstreamlivets2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tivibu Sport 3 HD","androstreamlivets3","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tivibu Sport 4 HD","androstreamlivets4","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Smart Sport 1 HD","androstreamlivesm1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Smart Sport 2 HD","androstreamlivesm2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Euro Sport 1 HD","androstreamlivees1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Euro Sport 2 HD","androstreamlivees2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii HD","androstreamlivetb","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 1 HD","androstreamlivetb1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 2 HD","androstreamlivetb2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 3 HD","androstreamlivetb3","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 4 HD","androstreamlivetb4","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 5 HD","androstreamlivetb5","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 6 HD","androstreamlivetb6","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 7 HD","androstreamlivetb7","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Tabii 8 HD","androstreamlivetb8","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen HD","androstreamliveexn","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 1 HD","androstreamliveexn1","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 2 HD","androstreamliveexn2","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 3 HD","androstreamliveexn3","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 4 HD","androstreamliveexn4","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 5 HD","androstreamliveexn5","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 6 HD","androstreamliveexn6","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 7 HD","androstreamliveexn7","https://i.hizliresim.com/8xzjgqv.jpg"),
    ("Exxen 8 HD","androstreamliveexn8","https://i.hizliresim.com/8xzjgqv.jpg"),
]

# 5️⃣ Toplu M3U8 dosyası
lines = ["#EXTM3U"]
for name, cid, logo in channels:
    lines.append(f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{name}" tvg-logo="{logo}" group-title="DeaTHLesS",TR:{name}')
    full_url = f"{base_url}{cid}.m3u8"
    lines.append(full_url)

with open("androiptv.m3u8", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("✅ androiptv.m3u8 faylı yaradıldı.")

# 6️⃣ Ayrı ayrı .m3u8 dosyaları
out_dir = "channels"
os.makedirs(out_dir, exist_ok=True)

for name, cid, logo in channels:
    file_name = name.replace(" ", "_").replace("/", "_") + ".m3u8"
    full_url = f"{base_url}{cid}.m3u8"

    content = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        '#EXT-X-STREAM-INF:BANDWIDTH=5500000,AVERAGE-BANDWIDTH=8976000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2",FRAME-RATE=25',
        full_url
    ]

    with open(os.path.join(out_dir, file_name), "w", encoding="utf-8") as f:
        f.write("\n".join(content))

print(f"✅ {len(channels)} kanal '{out_dir}' qovluğuna yazıldı.")
