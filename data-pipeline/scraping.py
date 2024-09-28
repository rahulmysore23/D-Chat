from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Function to set up the WebDriver
def setup_driver(driver_path, headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run headless (no browser window)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    return driver

# Function to collect hrefs from the page until a specified limit is reached
def collect_hrefs(driver, url, limit=1000):
    driver.get(url)

    # Wait for the initial content to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "listContent")))

    # Find the element with the class 'listContent'
    list_content = driver.find_element(By.CLASS_NAME, 'listContent')

    # Initialize a list to store hrefs
    hrefs = []

    # Function to collect hrefs from <li> elements
    def collect_links():
        nonlocal hrefs
        list_items = list_content.find_elements(By.TAG_NAME, 'li')
        for item in list_items:
            try:
                # Find the <a> tag within the <li>
                a_tag = item.find_element(By.TAG_NAME, 'a')
                # Get the href attribute and add it to the list
                href = a_tag.get_attribute('href')
                if href and href not in hrefs:
                    hrefs.append(href)
            except Exception as e:
                print(f"Error in collecting href: {e}")

    # Collect initial hrefs
    collect_links()

    # Click "Load More" button until we have at least 'limit' hrefs
    while len(hrefs) < limit:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "loadmore")))
            load_more_button.click()
            # Collect hrefs after loading more items
            time.sleep(3)  # Adding delay to allow more items to load
            collect_links()
        except Exception as e:
            print("No more items to load or an error occurred:", e)
            break

    # Return the collected hrefs (limited to 'limit' hrefs)
    return hrefs[:limit]

# Function to scrape content (H2 tags and paragraph content) from each href
def scrape_page(driver, href):
    # Initialize a dictionary to store the H2 and content
    page_content = {"h2": [], "paragraph": ""}

    try:
        driver.get(href)
        
        # Wait for the <h2> headings to load
        h2_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h2")))
        for h2 in h2_elements:
            page_content["h2"].append(h2.text)  # Store the text of each <h2> tag

        # Wait for the paragraph content to load
        paragraph = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "slds-rich-text-editor__output")))
        page_content["paragraph"] = paragraph.text  # Store the text content

    except Exception as e:
        print(f"Could not retrieve content from {href}: {e}")

    # Return the scraped content
    return page_content
