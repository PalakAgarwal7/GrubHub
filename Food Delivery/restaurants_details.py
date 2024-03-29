import csv
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def append_to_csv(data, file_name):
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        file.seek(0, 2)  # Go to the end of the file
        if file.tell() == 0:
            writer.writeheader()  # Write header if file is empty
        writer.writerows(data)

async def scrape_link(link, csv_file_name):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome( options=chrome_options)
    driver.get(link)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-testid*='category']")))
        categories = []
        category_elements = driver.find_elements(By.CSS_SELECTOR, "li[data-testid*='category']")

        for cat in category_elements:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(cat)).click()
            await asyncio.sleep(2)

            category_name = cat.text if cat.text else 'NA'
            dishes = []

            dishes_elements = driver.find_elements(By.CSS_SELECTOR, f'div[impressionid="{category_name}"')
            for ele in dishes_elements:
                dish_element = ele.text.splitlines()
                dish_name = dish_element[0] if len(dish_element) > 0 else 'NA'
                dish_price = dish_element[-1] if len(dish_element) > 1 else 'NA'
                dishes.append({'name': dish_name, 'price': dish_price})

            categories.append({
                "Category": category_name,
                "Dishes": dishes
            })

        flat_data = []
        for category in categories:
            for dish in category['Dishes']:
                flat_data.append({
                    'Restaurant Link': link,
                    'Restaurant ID' : link.split('/')[-1],
                    'Category': category['Category'],
                    'Dish Name': dish['name'],
                    'Dish Price': dish['price']

                })

        append_to_csv(flat_data, csv_file_name)
    except Exception as e:
        print(f"Error processing {link}: {e}")
    finally:
        driver.quit()

async def main():
    restaurant_link_list = []
    with open("Restaurant_grubhub_data.csv", mode="r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            restaurant_link_list.append(row["Restaurant_Link"])

    chrome_driver_path = "C:\development\chromedriver-win64\chromedriver.exe"
    csv_file_name = "Scraped_Restaurant_Data.csv"

    tasks = [scrape_link(link, csv_file_name) for link in restaurant_link_list[0:20]]
    await asyncio.gather(*tasks)

asyncio.run(main())
