import httpx
from selectolax.parser import HTMLParser
import random
import time
import ssl
import os
import logging

# URL to scrape
url = "https://mangatale.co/apocalyptic-chef-awakening-chapter-02/"
user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up SSL/TLS certificates using certifi
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations("mangatale.co.crt")
client = httpx.Client(verify=ssl_context)

def log_time_taken(start_time:float):
    seconds_taken = int(time.time() - start_time)
    minutes_taken = seconds_taken // 60
    return f"{minutes_taken} minutes and {seconds_taken % 60} seconds"

def create_folder(folder_title):
    folder_title_path = os.path.join("D:\manga", folder_title)
    if not os.path.exists(folder_title_path):
        os.makedirs(folder_title_path)
        logger.info(f"Folder created: {folder_title_path}")
    return folder_title_path

def download_image(folder_title: str, image_link: str):
    start_time = time.time()
    folder_chapter = url.split("/")[-2].split("-chapter-")[1]
    file_number = image_link.split("/")[-1].split(".")[0]
    filename = f"{file_number}.jpg" 
    filepath_folder = os.path.join(folder_title, f"Chapter {folder_chapter}") 
    filepath_jpg = os.path.join(filepath_folder, filename)
    
    create_folder(filepath_folder)
    if not os.path.exists(filepath_jpg):            
        try:
            image_link_response = client.get(image_link, headers=user_agent)
            with open(filepath_jpg, 'wb') as f:
                f.write(image_link_response.content)
            logger.info(f"downloaded: \033[1mChapter {folder_chapter}/{file_number}\033[0m {log_time_taken(start_time)}")
        except httpx.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}") 
    else:
        logger.info(f"File already exists: {filename}")

def goto_next_chapter(html: HTMLParser):
    next_page = html.css_first("a.ch-next-btn")
    if next_page:
        return next_page.attributes["href"]
    
def main():
    try:
        os.chdir("D:/manga")
        response = client.get(url, headers=user_agent)
        folder_title = url.split("/")[-2].split("-chapter-")[0].replace("-", " ")
        html = HTMLParser(response.text)
        images = html.css("#readerarea img")
        for image in images:
            image_link = image.attrs['src']
            download_image(folder_title, image_link)
            delay = random.uniform(10, 30)
            logger.info(f"Waiting for {delay} seconds...")
            time.sleep(delay)
    except httpx.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except Exception as http_err: 
        logger.error(f"An error occurred: {http_err}")
    finally:    
        client.close()

if __name__ == "__main__":
    main()