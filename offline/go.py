from playwright.sync_api import sync_playwright


def save_mhtml(path: str, text: str):
    with open(path, mode='w', encoding='UTF-8', newline='\n') as file:
        file.write(text)

def save_page(url: str, path: str):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=0)

        client = page.context.new_cdp_session(page)
        mhtml = client.send("Page.captureSnapshot")['data']
        save_mhtml(path, mhtml)
        browser.close()

if __name__ == '__main__':
    save_page('https://www.cnbcindonesia.com/', 'cnbc2.mhtml')