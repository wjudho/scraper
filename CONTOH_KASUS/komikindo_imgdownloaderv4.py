import httpx
from selectolax.parser import HTMLParser
import os
import ssl
import random
import time
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def main(url):
    folder_title = url.split("/")[-2].split("-chapter-")[0].replace("-", " ")
    folder_title_path = os.path.join(r"D:\manga", folder_title)
    folder_chapter = url.split("/")[-2].split("-chapter-")[1]
    filepath_folder = os.path.join(folder_title_path, f"Chapter {folder_chapter}") 
    
    if not os.path.exists(filepath_folder):
        os.makedirs(filepath_folder)
    
    while True:
        try:
            r = client.get(url, headers=headers)
            html = HTMLParser(r.text)
            images = html.css("#readerarea img")
            for image in images:
                image_link = image.attrs['src']
                file_number = image_link.split("/")[-1].split(".")[0]
                filename = f"{file_number}.jpg" 
                filepath_jpg = os.path.join(filepath_folder, filename)
                
                if not os.path.exists(filepath_jpg):    
                    timeout = random.randint(1, 10)
                    r2 = client.get(image_link, headers=headers, timeout=timeout)
                    with open(filepath_jpg, 'wb') as f:
                        f.write(r2.content)
                    logging.info(f"Downloaded {filepath_jpg}")
                    
                    delay = random.randint(1, 10)
                    time.sleep(delay)
                else:
                    logging.info(f"Skipping {filename}, already exists")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(args=["--trust-certificate=mangatale.co.crt"])
                page = browser.new_page()
                page.goto(url)
                try:
                    page.locator("a.ch-next-btn").first.click()
                    next_page_url = page.url
                    url = next_page_url
                    logging.info(f"Goto next chapter: {next_page_url}")
                    
                    folder_chapter = next_page_url.split("/")[-2].split("-chapter-")[1]
                    filepath_folder = os.path.join(folder_title_path, f"Chapter {folder_chapter}")
                    if not os.path.exists(filepath_folder):
                        os.makedirs(filepath_folder)
                    
                except:
                    logging.info(f"No next page found")
                    break
                finally:    
                    browser.close()
                
        except Exception as e:
            logging.error(f"Error occured: {e}")
            break
            
if __name__ == "__main__":
    # url = "https://mangatale.co/apocalyptic-chef-awakening-chapter-01/"
    url = "https://mangatale.co/reincarnated-as-a-new-employee-chapter-01/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"}
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.options |= ssl.OP_NO_TLSv1
    ssl_context.options |= ssl.OP_NO_TLSv1_1
    ssl_context.load_verify_locations("mangatale.co.crt")
    client = httpx.Client(verify=ssl_context, timeout=20)
    main(url)