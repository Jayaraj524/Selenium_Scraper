Iphex Exhibitor Scraper: Company and Details Extraction

This tool collects company data from the IPHEX exhibitor website and gathers in-depth details for
each company, saving everything into easy-to-use Excel/CSV files. Anyone can use this, even
without a coding background, by following the steps below.

How It Works
The project is divided into two parts:
1. Basic Scraper: Collects a list of companies, their stall numbers, and a link to their detailed profile.


2. In-depth Scraper: Visits each company profile link and extracts detailed information such as
company name, location, website, product categories, and profile.

Prerequisites
You need:
- A Windows PC (or Mac/Linux if you adapt instructions)
- Python 3.8 or above installed (python.org)
- Google Chrome installed
- ChromeDriver that matches your Chrome version (download from
chromedriver.chromium.org/downloads and place the file in the same folder as your scripts)
- The files Basic_Scraper.py and In_depth_Scraper.py (provided with this project)
- The requirements.txt file (provided with this project)

1. Install Required Python Libraries
Open Command Prompt (type cmd in the Windows search bar and hit Enter), then type the following
command in the folder where your scripts are:
 pip install -r requirements.txt
(This will install Selenium, pandas, and any other required libraries.)
2. Run the Basic Scraper
1. Open Command Prompt and navigate to the project folder.
 For example:
 cd D:\YourFolderName
2. Run the basic scraper:
 python Basic_Scraper.py
3. The program will open Chrome, collect all company links, and save the results to a file named
scraped_companies.csv.
 Wait until you see the message saying scraping is completed and data stored successfully.


3. Run the In-depth Scraper
1. Once the basic scraper is finished, you will have a file called scraped_companies.csv in your
folder.
2. Run the in-depth scraper:
 python In_depth_Scraper.py
3. The scraper will read all links from your scraped_companies.csv, visit each link, and extract
detailed information for each company.
4. Results are saved automatically every 10 companies, and again at the end, into
in_depth_company_details.csv.


4. Output Files
- scraped_companies.csv: Contains the basic company list and profile links.
- in_depth_company_details.csv: Contains all detailed information for each company: Company
Name, Location, Website, Product Categories, Company Profile, and the Source Link.
 You can open these files with Microsoft Excel or Google Sheets.
5. Tips and Troubleshooting
- Make sure you have a stable internet connection.
- If the script does not open Chrome or shows an error about ChromeDriver, download the correct
ChromeDriver version from chromedriver.chromium.org/downloads and place it in your script folder.
- If you accidentally close Chrome during scraping, just restart the script; it saves progress every 10
companies.
- The process can take some time depending on your internet speed and the number of companies.
6. Contact
For any issues or help, reach out to the team member who set up this project, or consult your
in-house data or IT team.
This README is designed to be clear and simple for anyone in your team.
