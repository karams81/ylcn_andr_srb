from playwright.sync_api import sync_playwright
import re, os

active_domain = "https://birazcikspor25.xyz/"
proxy_prefix = "https://proxy.freecdn.workers.dev/?url="

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"{proxy_prefix}{active_domain}", timeout=15000)

    # Sayfadaki tüm m3u8 linklerini çek
    content = page.content()
    links = re.findall(r'(https?://[^\s"\']+\.m3u8)', content)

    if not links:
        raise SystemExit("❌ Sayfada hiç m3u8 linki bulunamadı.")

    print(f"✅ {len(links)} adet m3u8 linki bulundu.")

    # Toplu M3U8 dosyası
    lines = ["#EXTM3U"]
    for i, link in enumerate(links, 1):
        lines.append(f"#EXTINF:-1, Kanal {i}")
        lines.append(link)

    with open("androiptv.m3u8", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Ayrı kanallar
    out_dir = "channels"
    os.makedirs(out_dir, exist_ok=True)
    for i, link in enumerate(links, 1):
        file_name = f"Kanal_{i}.m3u8"
        content = ["#EXTM3U", link]
        with open(os.path.join(out_dir, file_name), "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    print(f"✅ {len(links)} kanal '{out_dir}' dizinine yazıldı.")
    browser.close()
