from dotenv import load_dotenv
from scraping import setup_driver, collect_hrefs, scrape_page
from file_operations import save_content_locally
from upload_to_pinata import upload_to_pinata
import os

def main():
    # Load environment variables
    load_dotenv()
    pinata_jwt = os.getenv('PINATA_JWT')
    #driver_path = #Chrome driver path
    url = 'https://ask.usda.gov/s/global-search/food?tabset-fd9ce=2'
    output_dir = "usdac_data_scrap"

    # Set up WebDriver
    driver = setup_driver(driver_path)

    try:
        # Collect HREFs
        hrefs = collect_hrefs(driver, url, limit=10)
        print(f"Collected {len(hrefs)} hrefs")

        # Scrape content
        all_contents = []
        for count, href in enumerate(hrefs, start=1):
            page_content = scrape_page(driver, href)
            all_contents.append({"href": href, "content": page_content})
            print(f"Scraped link {count}: {href}")

        # Save content locally
        save_content_locally(all_contents, output_dir)

    finally:
        # Quit driver
        driver.quit()

    # Upload to Pinata
    upload_to_pinata(output_dir, pinata_jwt)

if __name__ == "__main__":
    main()
