import httpx
from selectolax.parser import HTMLParser
import os
from dataclasses import dataclass
from urllib.parse import urljoin
import logging
import time
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rotating user agent
USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0"
]

headers = {"User-Agent": random.choice(USER_AGENT)}
BASE_URL = "https://www.mgeko.cc"

@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict

MAX_ATTEMPTS = 3
TIMEOUT = 3

def retry(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> None:
        for attempt in range(MAX_ATTEMPTS):
            try:
                return func(*args, **kwargs)
            except httpx.RequestError as e:
                logger.error(f"Failed to {func.__name__}: {e}. Retrying...")
                time.sleep(TIMEOUT) # wait before retrying
        logger.error(f"Failed to {func.__name__} after {MAX_ATTEMPTS} attempts.")
    return wrapper

def create_image_directory(image_dir: str) -> None:
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

def log_time_taken(start_time: float) -> str:
    seconds_taken = int(time.time() - start_time)
    minutes_taken = seconds_taken // 60
    return f"{minutes_taken} minutes and {seconds_taken % 60} seconds"
    
@retry
def download_image(img_url: str, image_dir: str, url: str, page_number: int) -> None:
    start_time = time.time()
    try:
        img_response = httpx.get(img_url, headers=headers)
        img_response.raise_for_status()
        img_alt = img_url.split("/")[-1].split(".")[0]
        chapter_number = url.split("/")[-2].split("-chapter-")[1].split("-")[0]
        page_dir = os.path.join(image_dir, f"Chapter {chapter_number}")
        create_image_directory(page_dir)
        filename = f"{img_alt}.jpg"
        with open(os.path.join(page_dir, filename), "wb") as f:
            f.write(img_response.content)
            logger.info(f"Image '{filename}' \033[1mChapter {chapter_number}\033[0m Downloaded. Time Taken: {log_time_taken(start_time)}")
    except httpx.RequestError as e:
        logger.error(f"Failed to download image '{img_alt}.jpg': {e}")

@retry
def get_img(client: httpx.Client, url: str, image_dir: str, page_number: int) -> None:
    start_time = time.time()
    try:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        html = HTMLParser(resp.text)
        imgs = html.css("#chapter-reader img")
        img_urls = [i.attrs["src"] for i in imgs]
        for img_url in img_urls:
            download_image(img_url, image_dir, url, page_number)
        logger.info(f"Images fetched from page {page_number}. Time Taken: {log_time_taken(start_time)}")
        # logger.info(f"Images fetched from page {page_number}. Time taken: {time.time() - start_time:.2f} seconds or {(time.time() - start_time) / 60:.2f} minutes")
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch images: {e}")

def get_next_page_url(html: HTMLParser) -> dict:
    next_page = html.css_first("#save > a.nextchap")
    if next_page:
        return {"href": next_page.attributes["href"]}
    return {"href": False}

@retry
def get_pages(client: httpx.Client, url: str, image_dir: str, base_url: str, page_number: int = 1) -> None:
    start_time = time.time()
    try:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        html = HTMLParser(response.text)
        get_img(client, url, image_dir, page_number)
        next_page_url = get_next_page_url(html)
        if next_page_url["href"]:
            next_page_url = urljoin(base_url, next_page_url["href"])
            logger.info(f"Next page: {next_page_url}. Time Taken: {log_time_taken(start_time)}")
            get_pages(client, next_page_url, image_dir, base_url, page_number + 1)
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch page: {e}")

def main() -> None:
    url = "https://www.mgeko.cc/reader/en/embodiment-of-the-assassin-in-the-murim-world-chapter-2-eng-li/"
    # Current Working Directory
    os.chdir("D:/manga")
    # Folder will be rename according to url
    chapter_name = url.split("/")[-2].split("-chapter-")[0].replace("-", " ")
    image_dir = chapter_name
    # from previous define function to create main folder if doesn't exist
    create_image_directory(image_dir)
    client = httpx.Client()
    start_time = time.time()
    get_pages(client, url, image_dir, BASE_URL)
    logger.info(f"Total time taken to download \033[1m{chapter_name}\033[0m: {log_time_taken(start_time)}")

if __name__ == "__main__":
    main()