import asyncio
import csv
import json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for background execution
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the target Tokopedia search page
        await page.goto("https://www.tokopedia.com/search?q=macbook+pro+m3&source=universe&st=product&srp_component_id=02.07.02.01")

        # Wait for initial page load with a timeout (adjust as needed)
        try:
            await page.wait_for_selector('div#zeus-root', timeout=5000)  # Replace with a more specific selector if necessary
        except playwright._impl._api_types.TimeoutError:
            print("Timeout error waiting for page to load. Consider increasing timeout or using a more specific selector.")

        # Extract product data using appropriate selectors (replace with actual selectors from Tokopedia)
        product_titles = await page.query_selector_all('div.prd_link-product-name')  # Replace with product title selector
        product_prices = await page.query_selector_all('div.prd_link-product-price')  # Replace with product price selector
        product_links = await page.query_selector_all('a.pcv3__info-content')  # Replace with product link selector

        # Process and store extracted data
        product_data = []
        for i in range(len(product_titles)):
            title = await product_titles[i].text_content()
            price = await product_prices[i].text_content()
            link = await product_links[i].get_attribute('href')
            product_data.append({
                "title": title,
                "price": price,
                "link": link
            })
        
        print(product_data)

        # Save data ethically and responsibly
        try:
            save_to_csv(product_data, "scraped_products.csv")
            save_to_json(product_data, "scraped_products.json")
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")

        await browser.close()

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

asyncio.run(main())