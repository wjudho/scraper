from playwright.sync_api import sync_playwright
import os

# save pages as html
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    # goto page 13 as starting point (bcs the oldest chapter is in pages 13)
    page.goto("https://www.tokopedia.com/search?navsource=&ob=5&pmax=1800000&pmin=1100000&srp_component_id=04.06.00.00&srp_page_id=&srp_page_title=&st=&q=android")

    html_articles = []
    # Get-the-Page
    articles = page.locator('html')
    html_articles.append(articles.inner_html())

    # specify folder to save file
    with open("stack.html", "w+", encoding="utf-8") as f:
        full_html_articles = ''.join(html_articles)
        f.write(full_html_articles)
    browser.close()
