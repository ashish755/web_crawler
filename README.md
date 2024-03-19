# web_crawler

## postgres database setup
    - host="localhost",
    - database="postgres",
    - user="postgres",
    - password="postgres"


## Script
- The script web_crawler.py takes one argument: y - yes , n - no.
    python web_crawler.py n  ## parse through the web page, gets the product info and saves in json file
    python web_crawler.py y  ## parse through the web page, gets the product info and saves in json file as well as postgres database

## Additional files
- The geckodriver and firefox files are also uploaded.

- The docker container setup is also done but there are some error related to selenium.

## Output
- The output is saved in products.json file