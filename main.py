from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


brave_options = Options()
brave_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
# can change to chrome , i am using brave so the path is of brave

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=brave_options)

try:
  
    base_url = 'https://www.indeed.com/jobs?q=part+time&l=Remote&vjk=c7c162cfda2f3215'
   
    driver.get(base_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'job_seen_beacon'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

   
    job_cards = soup.find_all('div', class_='job_seen_beacon')


    job_listings = []

    for job in job_cards:
        title_elem = job.find('h2', class_='jobTitle')
        company_elem = job.find('span', class_="css-63koeb eu4oa1w0")
        location_elem = job.find('div', class_='company_location')
        summary_elem = job.find('div', class_='css-9446fg eu4oa1w0')
        link_elem = job.find('a')
        extra_elem = job.find('div', class_='heading6')

        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
        company = company_elem.get_text(strip=True) if company_elem else 'N/A'
        location = location_elem.get_text(strip=True) if location_elem else 'N/A'
        summary = summary_elem.get_text(strip=True) if summary_elem else 'N/A'
        link = 'https://www.indeed.com' + link_elem['href'] if link_elem else 'N/A'
        extra = extra_elem.get_text(strip=True) if extra_elem else 'N/A'

       
        print(f'Job Title: {title}')
        print(f'Company: {company if company != "N/A" else "Company data not found!"}')
        print(f'Location: {location if location != "N/A" else "Location data not found!"}')
        print(f'Summary: {summary if summary != "N/A" else "Summary data not found!"}')
        print(f'Link: {link}\n')
        print(f'extra: {extra}\n')

    
        job_listings.append([title, company, location, summary, link, extra])

    
    df = pd.DataFrame(job_listings, columns=['Job Title', 'Company', 'Location', 'Summary', 'Link', 'Extra'])
    df.to_excel('job_listings.xlsx', index=False)

except Exception as e:
    print(f'An error occurred: {e}')
finally:

    driver.quit()
