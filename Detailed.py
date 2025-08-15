from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Load links from your previous scrape
input_df = pd.read_csv('scraped_companies.csv')
detail_links = input_df['View More Link'].tolist()

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 12)

company_names = []
locations = []
websites = []
product_categories = []
company_profiles = []

for idx, link in enumerate(detail_links):
    driver.get(link)
    time.sleep(2.2)  # Adjust if needed

    # Company Name
    try:
        cname_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.profile-name")))
        cname = cname_elem.text.strip()
    except Exception:
        cname = ""
    
    # Location
    try:
        loc_elem = driver.find_element(By.CSS_SELECTOR, "div.profile-location")
        location = loc_elem.text.strip()
    except Exception:
        location = ""

    # Website (any <a> inside first div.profile-location)
    try:
        web_elem = driver.find_element(By.CSS_SELECTOR, "div.profile-location a")
        website = web_elem.get_attribute("href")
    except Exception:
        website = ""
    
    # Product Categories (all div.profile-location after the first)
    try:
        all_profile_locations = driver.find_elements(By.CSS_SELECTOR, "div.profile-location")
        categories = []
        for ploc in all_profile_locations[1:]:  # skip the first, as it's usually location/website
            icons = ploc.find_elements(By.CSS_SELECTOR, "i.fa-angle-double-right")
            for icon in icons:
                parent = icon.find_element(By.XPATH, "..")
                # Category name is typically after the icon, may be sibling or inner text
                # We use parent's text, minus the icon symbol
                txt = parent.text.replace("»", "").strip()
                if txt:
                    categories.append(txt)
        product_cat = ", ".join(categories)
    except Exception:
        product_cat = ""

    # Company Profile (second <p> inside div.col-sm-12)
    try:
        profile_elem = driver.find_element(By.CSS_SELECTOR, "div.col-sm-12 > p:nth-of-type(2)")
        profile = profile_elem.text.strip()
    except Exception:
        profile = ""

    company_names.append(cname)
    locations.append(location)
    websites.append(website)
    product_categories.append(product_cat)
    company_profiles.append(profile)
    
    print(f"[{idx+1}/{len(detail_links)}] {cname} done")

    # Optional: Save every 10 companies for progress safety
    if (idx+1) % 10 == 0:
        pd.DataFrame({
            'Company Name': company_names,
            'Location': locations,
            'Website': websites,
            'Product Categories': product_categories,
            'Company Profile': company_profiles,
            'Source Link': detail_links[:len(company_names)]
        }).to_csv('in_depth_company_details.csv', index=False)
        print("Checkpoint save...")

# Final Save
output_df = pd.DataFrame({
    'Company Name': company_names,
    'Location': locations,
    'Website': websites,
    'Product Categories': product_categories,
    'Company Profile': company_profiles,
    'Source Link': detail_links
})
output_df.to_csv('in_depth_company_details.csv', index=False)

driver.quit()
print("In-depth scraping completed and saved!")
