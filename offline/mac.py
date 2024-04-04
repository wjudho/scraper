# from playwright.sync_api import sync_playwright
# from selectolax.parser import HTMLParser

# def parse_item(html_page):
#     results = []
#     html = HTMLParser(html_page)
#     items = html.css(".css-llwpbs")
#     for item in items:
#         product = {
#             "title": item.css_first(".prd_link-product-name css-3um8ox")
#             }
#         results.append(product)
#     return results

# def main():
#     url = "https://www.tokopedia.com/search?q=macbook+pro+m3&source=universe&st=product&navsource=home&srp_component_id=02.02.02.04"
#     with sync_playwright() as pw:
#         browser = pw.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto(url, wait_until="networkidle")

# def save_page():
#     with open('mac.html', 'w') as e:
#         e.write(parse_item)

# if __name__ == "__main__":
#     main()

import email
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
with open("mac.mhtml") as fp:
    message = email.message_from_file(fp, 'lxml')
    for part in message.walk():
        if (part.get_content_type() == "text/html"):
            soup = BeautifulSoup(part.get_payload(decode=False))
            for table in soup.body.find_all("table", recursive=False):
                extractor = Extractor(table)
                extractor.parse()
                print(extractor.return_list())