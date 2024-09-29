from dotenv import load_dotenv
from scraping import setup_driver, collect_hrefs, scrape_page
from file_operations import save_content_locally
from upload_to_pinata import upload_to_pinata
import os
import argparse

def main(search_term, limit):
    load_dotenv()
    pinata_jwt = os.getenv('PINATA_JWT')
    url = f'https://ask.usda.gov/s/global-search/{search_term}?tabset-fd9ce=2'
    output_dir = f"usdac_data_scrap_{search_term}"
    driver_path = "D:\chromedriver-win64\chromedriver-win64\chromedriver.exe" # update this before running

    driver = setup_driver(driver_path)

    try:
        hrefs = collect_hrefs(driver, url, limit=limit)
        print(f"Collected {len(hrefs)} hrefs")

        all_contents = []
        for count, href in enumerate(hrefs, start=1):
            page_content = scrape_page(driver, href)
            all_contents.append({"href": href, "content": page_content})
            print(f"Scraped link {count}: {href}")

        save_content_locally(all_contents, output_dir, search_term)

    finally:
        driver.quit()

    upload_to_pinata(output_dir, pinata_jwt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape USDA website and upload to Pinata')
    parser.add_argument('search_term', type=str, help='Search term for USDA website')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Limit of links to scrape (default: 10)')
    
    args = parser.parse_args()
    
    main(args.search_term, args.limit)