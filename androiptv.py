from playwright.sync_api import sync_playwright
import os

active_domain = "https://birazcikspor25.xyz/"
proxy_prefix = "https://proxy.freecdn.workers.dev/?url="

m3u8_links = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Network trafiğini dinle
    def handle_response(response):
        url = response.url
        if url.endswith(".m3u8"):
            m3u8_links.add(url)
            print("✅ Bulunan m3u8:", url)

    page.on("response", handle_response)

    # Sayfayı proxy üzerinden aç
    page.goto(f"{proxy_prefix}{active_domain}", timeout=20000)

    # Birkaç saniye bekle ki tüm JS çalışsın ve linkler gelsin
    page.wait_for_timeout(8000)

    if not m3u8_links:
        raise SystemExit("❌ Sayfada hiç m3u8 linki bulunamadı.")

    # Toplu M3U8 dosyası
    lines = ["#EXTM3U"]
    for i, link in enumerate(m3u8_links, 1):
        lines.append(f"#EXTINF:-1, Kanal {i}")
        lines.append(link)

    with open("androiptv.m3u8", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Ayrı kanal M3U8
    out_dir = "channels"
    os.makedirs(out_dir, exist_ok=True)
    for i, link in enumerate(m3u8_links, 1):
        file_name = f"Kanal_{i}.m3u8"
        with open(os.path.join(out_dir, file_name), "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + link)

    print(f"✅ {len(m3u8_links)} kanal '{out_dir}' dizinine yazıldı.")

    browser.close()
