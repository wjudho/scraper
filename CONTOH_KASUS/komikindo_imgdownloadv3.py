import httpx
from selectolax.parser import HTMLParser
import os
import ssl
import random
import time


url = "https://mangatale.co/apocalyptic-chef-awakening-chapter-04/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"}

# Set up SSL/TLS certificates using certifi
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations("mangatale.co.crt")
client = httpx.Client(verify=ssl_context)


def main():
    folder_title = url.split("/")[-2].split("-chapter-")[0].replace("-", " ")
    folder_title_path = os.path.join(r"D:\manga", folder_title)
    folder_chapter = url.split("/")[-2].split("-chapter-")[1]
    filepath_folder = os.path.join(folder_title_path, f"Chapter {folder_chapter}") 
    
    if not os.path.exists(filepath_folder):
        os.makedirs(filepath_folder)
    
    r = client.get(url, headers=headers)
    html = HTMLParser(r.text)
    images = html.css("#readerarea img")
    for image in images:
        image_link = image.attrs['src']
        file_number = image_link.split("/")[-1].split(".")[0]
        filename = f"{file_number}.jpg" 
        filepath_jpg = os.path.join(filepath_folder, filename)
        
        if not os.path.exists(filepath_jpg):    
            timeout = random.randint(5, 30)
            r2 = client.get(image_link, headers=headers, timeout=timeout)
            with open(filepath_jpg, 'wb') as f:
                f.write(r2.content)
            print(f"Downloaded {filename}")
            
            delay = random.randint(1, 10)
            time.sleep(delay)
            print(f"Waiting for {delay} seconds....")
        else:
            print(f"Skipping {filename}, already exists")
        
        
if __name__ == "__main__":
    main()