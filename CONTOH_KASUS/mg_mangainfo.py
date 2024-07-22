import httpx
from selectolax.parser import HTMLParser
import os
from urllib.parse import urljoin
import csv

client = httpx.Client(timeout=30.0)

manga_info = []
os.chdir(r'D:\manga')

# Get Page URL
for page_number in range(1, 201):
    url = "https://www.mgeko.cc/browse-comics/?results={}&filter=views"
    url_page = url.format(page_number)
    # print(url_page)

    # Fetch The Page URL
    try:
        response = client.get(url_page)
        response.raise_for_status()
    except httpx.RequestError as exc:
        print(f"An error occured while requesting {exc.request.url!r}: while requesting {exc.request.url!r}: {exc}")
    except httpx.HTTPStatusError as exc:   
        print(f"Error Response {exc.response.status_code} while requesting {exc.request.url!r}: {exc} ")
    else:      
        parser = HTMLParser(response.text)
        manga_links = [urljoin(url_page, a.attributes['href']) for a in parser.css("li.novel-item > a")]
        print(f"Found {len(manga_links)} manga Links on page {page_number}.")
        # print(manga_links)
        
        # Get Manga Info
        for manga_link in manga_links:
            try:
                response = client.get(manga_link)
                response.raise_for_status()
            except httpx.RequestError as exc:
                print(f"An error occured while requesting {exc.request.url!r}: {exc}")
            else:
                parser = HTMLParser(response.text)
                manga_title = parser.css("div.main-head > h1")[0].text().strip().replace('â€™', "'").replace('â€“', '-').replace('Iâ€¦', 'I...').replace('â€œ', '"').replace('â€œ', '"').replace('â€•', '-').replace('â€¢', '*').replace('â€˜', "'")
                manga_chapters = parser.css("span:nth-child(1) > strong")[0].text().strip('book ')
                manga_views = parser.css("span:nth-child(2) > strong")[0].text().strip('supervised_user_circle ') 
                manga_bookmarked = parser.css("span:nth-child(3) > strong")[0].text().strip('bookmark ')
                manga_last_updated = parser.css("div.updinfo > strong")[0].text().replace('\xa0', ' ')
                manga_summary = parser.css("#info > p.description")[0].text().strip().replace('\n\n', ': ').replace('\n', ' ')
                manga_info.append((manga_title, manga_chapters, manga_views, manga_bookmarked, manga_last_updated, manga_summary))
                print(f"Processed page: {page_number} manga: {manga_title}.")
        
# Save to CSV
with open('mgeko.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["Title", "Chapter", "Views", "Bookmarked", "Last Updated", "Summary"])
    writer.writerows(manga_info)
print("Data saved to mgeko.csv.")