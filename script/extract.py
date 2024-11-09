from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from webdriver_manager.chrome import ChromeDriverManager  
from google.oauth2.service_account import Credentials
import pandas as pd
import pandas_gbq
from datetime import datetime  
import time  

def scrape_page(driver):  

    rows = driver.find_elements(By.CSS_SELECTOR, "table.table-sales tbody tr")  
    
    games_data = []  

    for row in rows:  
        cols = row.find_elements(By.TAG_NAME, "td")  
        if len(cols) >= 8:  
            try:  
                # Extract the title removing the <span>
                title_element = cols[2].find_element(By.TAG_NAME, 'a')  
                title = title_element.get_attribute('textContent').split("\n")[0].strip()  

                rating_text = cols[5].text.strip().replace('%', '')  
                rating = float(rating_text)

                game_info = {  
                    "Title": title,  
                    "Discount": cols[3].text.strip(),  
                    "Current Price": cols[4].text.strip(),  
                    "Rating": rating,  
                    "Release Date": cols[6].text.strip(),  
                    "Sale End Date": datetime.fromtimestamp(int(cols[7].get_attribute('data-sort'))),  
                    "Sale Start Date": datetime.fromtimestamp(int(cols[8].get_attribute('data-sort'))),  
                    "Link": cols[1].find_element(By.TAG_NAME, 'a').get_attribute('href')  
                }  
                games_data.append(game_info)  
            except Exception as e:  
                print(f"Error processing row: {e}")  

    return games_data  

def scrape_steam_sales():   
    options = webdriver.ChromeOptions()  
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')  
    options.add_argument('--no-sandbox')  
    options.add_argument('--window-size=1920,1080')  
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')  
  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  
    url = "https://steamdb.info/sales/"  
    driver.get(url)  

    # Wait until the table is loaded
    wait = WebDriverWait(driver, 20)  
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-sales")))  

    all_games_data = []  
    page_number = 1 

    # Loop to collect data from all pages
    while True:  
        print(f"Extracting data from page: {page_number}...")  
        page_data = scrape_page(driver)  
        all_games_data.extend(page_data)  
        
        try:  
            next_button = driver.find_element(By.CSS_SELECTOR, 'button.dt-paging-button.next')

            if 'disabled' in next_button.get_attribute('class'):  
                break  
            next_button.click()  
            page_number += 1
            time.sleep(2)  
        except:  
            print("Button not found")  
            break  

    driver.quit()  

    df = pd.DataFrame(all_games_data) 
    
    return df

def upload_to_bigquery(df, table_id, credentials, if_exists='replace'):

    credentials = Credentials.from_service_account_file(credentials)
    
    project_id = credentials.project_id

    print("Loading dataframe to BigQuery...")
    pandas_gbq.to_gbq(df, table_id, project_id, if_exists=if_exists, credentials=credentials)

if __name__ == "__main__":  
    df = scrape_steam_sales()
    upload_to_bigquery(df, 'steamdb.sales', 'credentials.json')