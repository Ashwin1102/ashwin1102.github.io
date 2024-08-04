from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

page_url = "https://www.myntra.com/men-jeans"

driver = webdriver.Chrome()

driver.get(page_url)

pagination = driver.find_element(By.CLASS_NAME, "pagination-paginationMeta").text
last_page = int(pagination.split(" ")[3])
data = {
    "name" : [],
    "brand" : [],
    "distress" : [],
    "waist_rise" : [],
    "length" :  [],
    "fit" : [],
    "number_of_pockets" : [],
    "occasion" : [],
    "reversible" : [],
    "stretch" : [],
    "price" : [],
    "rating" : [],
    "number_of_ratings" : []

}
product_urls = []

c = 0

for i in range(600):  # Adjust this as needed
    try:
        products = driver.find_elements(By.CLASS_NAME, "product-base")
        product_urls += [element.find_element(By.TAG_NAME, "a").get_attribute("href") for element in products]
        next_button = driver.find_element(By.CLASS_NAME, "pagination-next")
        driver.execute_script("arguments[0].click();", next_button)
    except StaleElementReferenceException:
        continue


print("product_urls ", len(product_urls))

for url in product_urls:
    try:
        c += 1
        print(c)
        driver.get(url)

        driver.find_element(By.CLASS_NAME, "index-showMoreText").click()

        specifications = driver.find_elements(By.CLASS_NAME, "index-row")
        price = driver.find_element(By.CLASS_NAME, "pdp-price").find_element(By.TAG_NAME, "strong").text
        brand = driver.find_element(By.CLASS_NAME, "pdp-title").text
        name = driver.find_element(By.CLASS_NAME, "pdp-name").text
        
        try:
            rating_element = driver.find_element(By.CSS_SELECTOR, "[class^='index-overallRating']").find_elements(By.TAG_NAME, "div")
            rating = rating_element[1].text
        except NoSuchElementException:
            rating = None

        try:
            number_of_ratings = driver.find_element(By.CLASS_NAME, "index-ratingsCount").text
        except NoSuchElementException:
            rating = None

        data["price"].append(price)
        data["rating"].append(rating)
        data["number_of_ratings"].append(number_of_ratings)
        data["brand"].append(brand)
        data["name"].append(name)
            
        spec_dict = {
            "Distress": None,
            "Waist Rise": None,
            "Length": None,
            "Fit": None,
            "Number of Pockets": None,
            "Occasion": None,
            "Reversible": None,
            "Stretch": None
        }

        for specification in specifications:
            key = specification.find_element(By.CLASS_NAME, "index-rowKey").text
            value = specification.find_element(By.CLASS_NAME, "index-rowValue").text
            if key in spec_dict:
                spec_dict[key] = value

        data["distress"].append(spec_dict["Distress"])
        data["waist_rise"].append(spec_dict["Waist Rise"])
        data["length"].append(spec_dict["Length"])
        data["fit"].append(spec_dict["Fit"])
        data["number_of_pockets"].append(spec_dict["Number of Pockets"])
        data["occasion"].append(spec_dict["Occasion"])
        data["reversible"].append(spec_dict["Reversible"])
        data["stretch"].append(spec_dict["Stretch"])
    
    except Exception as e:
        print(f"Exception occurred while processing product URL {url}: {e}")
        continue

df = pd.DataFrame(data)
csv_file_path = 'jeans_data.csv'
df.to_csv(csv_file_path, index=False)