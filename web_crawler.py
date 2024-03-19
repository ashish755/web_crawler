import re
import sys
import json
import psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver
from logger_config import configure_logger

logger = configure_logger(__name__)

class SeleniumParser:
    def __init__(self, save_db):
        # path of the geckodriver
        path = "./geckodriver"

        self.products = []
        for page_number in range(1,4):
            logger.info(f"Fetching data for page number: {page_number}")
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.binary_location = "./firefox"
            firefox_options.add_argument('--headless') 
            driver = webdriver.Firefox(executable_path=path, options=firefox_options)

            url = f"https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html?p={page_number}"
            driver.get(url)

            html_contents = driver.page_source
            # parse html content using beautiful soup
            soup = BeautifulSoup(html_contents, 'html.parser')

            product_list_container = soup.find('div', id='uk-product-list-container')
            product_divs = product_list_container.find_all('div', class_='uk-panel uk-position-relative')

            # extract name, price, brand, image_url and product_url of the product
            for product_div in product_divs:
                name = self.clean_text(product_div.find('h3', class_='product-name').text.strip())
                price = self.clean_text(product_div.find('span', class_='uk-price').text.strip())
                brand = self.clean_text(product_div.find(class_='uk-width-expand').text.strip())
                image_url = product_div.find('img')['src']
                product_url = product_div.find('a', class_='product-item-link')['href']

                product = {
                    'name': name,
                    'price': price,
                    'brand': brand,
                    'image_url': image_url,
                    'product_url': product_url
                }

                self.products.append(product)

        # store the data to json file
        with open("products.json", "w") as f:
            json.dump(self.products, f, indent=3)

        driver.quit()
        if save_db.lower() == "y":
            print("Database operations")
            # store data to postgres database
            self.create_table()
            self.store_in_db()
        

    def clean_text(self, text):
        """
            remove line breaks, extra space and unnecessary unicode from text
        """
        text = re.sub("\n", "", text)
        text = re.sub("\s+", " ", text)
        text = re.sub("\xa0", "", text)
        return text
    
    def create_table(self):
        self.conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres")

        self.curr = self.conn.cursor()

        logger.info("Creating table")
        # Create openai_comments table if none exists
        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS products_info(
            product_id INT PRIMARY KEY,
            name VARCHAR(255),
            brand VARCHAR(255),
            price VARCHAR(255),
            image_url VARCHAR(255),
            product_url VARCHAR(255)
        )
        """)

    def store_in_db(self):
        logger.info("Storing in database")
        for idx, product in enumerate(self.products, start=1):
            self.curr.execute(""" insert into products_info values (%s,%s,%s,%s,%s,%s)""", (
                idx,
                product["name"],
                product["brand"],
                product["price"],
                product["image_url"],
                product["product_url"],
            ))
            self.conn.commit()

if __name__ == "__main__":
    save_db = sys.argv[1]
    parser = SeleniumParser(save_db)

