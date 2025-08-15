from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

driver = webdriver.Chrome()
driver.maximize_window()

url = 'https://iphex-india.com/exhibitor/exhibitors'
driver.get(url)
time.sleep(3)  # Wait for page load

wait = WebDriverWait(driver, 15)

company_names = []
stall_numbers = []
view_more_links = []

def save_to_csv():
    df = pd.DataFrame({
        'Company Name': company_names,
        'Stall Number': stall_numbers,
        'View More Link': view_more_links
    })
    df.to_csv('scraped_companies.csv', index=False)
    print("Intermediate save to CSV.")

header_keywords = ["exhibitor", "stall name"]

rows = driver.find_elements(By.CSS_SELECTOR, 'tr.gridrow')  # Only company rows

for i, row in enumerate(rows):
    try:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) < 2:
            continue

        name_text = cells[0].text.strip().lower()
        if (
            not name_text
            or name_text == "view more"
            or name_text.startswith(".....")
            or any(h in name_text for h in header_keywords)
        ):
            continue

        # Get company name and stall number
        try:
            name_elem = cells[0].find_element(By.TAG_NAME, 'span')
            company_name = name_elem.text.strip()
        except Exception:
            company_name = cells[0].text.strip()
        stall_number = cells[1].text.strip() if len(cells) > 1 else ""

        # Scroll row into view and click (using JS for reliability)
        driver.execute_script("arguments[0].scrollIntoView(true);", row)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", row)

        # Retry logic for robust extraction
        link_found = False
        retries = 0
        view_more_link = ""

        while not link_found and retries < 3:
            try:
                details_row = row.find_element(By.XPATH, 'following-sibling::tr[1]')
                # Wait until the details row is visible
                wait.until(lambda d: details_row.value_of_css_property('display') != 'none')
                # Now wait for the 'View More' link inside details_row
                view_more_elem = WebDriverWait(details_row, 6).until(
                    lambda dr: dr.find_element(By.LINK_TEXT, 'View More')
                )
                view_more_link = view_more_elem.get_attribute('href')
                link_found = True
            except Exception:
                retries += 1
                time.sleep(1)  # Give more time before retrying

        if not link_found:
            print(f"Could not get View More for: {company_name}")

        company_names.append(company_name)
        stall_numbers.append(stall_number)
        view_more_links.append(view_more_link)
        print(f"Done with company {len(company_names)}: {company_name} | {view_more_link}")

        time.sleep(0.5)  # Slightly increased for reliability

        # Every 10 companies, save progress and scroll
        if (len(company_names)) % 10 == 0:
            save_to_csv()
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(0.8)

    except Exception as e:
        print(f"Error on row {i+1}: {e}")

# Final save
save_to_csv()
driver.quit()
print("All scraping completed and data stored successfully!")
