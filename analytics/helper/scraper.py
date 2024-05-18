from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time
import csv

def blinkit():
    driver_path = r"C:\Users\shiva\chromedriver_win32\chromedriver.exe"

    # Create ChromeOptions object
    options = Options()
    query = input("Enter the product you want to search: ")

    # Set desired capabilities
    options.add_argument("--start-maximized")  # Maximize the browser window on startup

    # Create Chrome WebDriver with specified options
    driver = webdriver.Chrome(options=options)

    # Navigate to the desired website
    driver.get(f'https://blinkit.com/s/?q={query}')

    # Find the location input field
    location_input_xpath = '/html/body/div[1]/div/div/div[1]/header/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/input'
    location_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, location_input_xpath)))

    if location_input:
        print("Location input found successfully.")

    # Clear the location input field
    location_input.clear()

    # Type "110001" directly into the location input field
    location_input.send_keys("110")
    time.sleep(1)
    location_input.send_keys("001")
    time.sleep(1)


    # Wait for the autocomplete options to appear
    autocomplete_options_xpath = '//div[@class="LocationSearchList__LocationLabel-sc-93rfr7-2 ixiZXd"]'
    autocomplete_options = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, autocomplete_options_xpath)))

    if autocomplete_options:
        print("Autocomplete options found successfully.")

    # Iterate through the autocomplete options and select "New Delhi, Delhi 110001, India"
    for option in autocomplete_options:
        if option.text == "New Delhi, Delhi 110001, India":
            try:
                # Scroll to the element using JavaScript
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                
                # Click on the element using JavaScript
                driver.execute_script("arguments[0].click();", option)
                break
            except Exception as e:
                print("Exception occurred while clicking:", str(e))


    product_names = []
    delivery_times = []
    prices_to_consumer = []
    actual_prices = []
    discounts = []

    for i in range(2, 21):
        try:
            
            xpath = f'//*[@id="app"]/div/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[2]/a[{i}]'
            card = driver.find_element(By.XPATH, xpath)
            
            # Extract product name
            product_name_element = card.find_element(By.XPATH, f'{xpath}/div/div[3]/div[2]/div[1]/div[1]')
            product_name = product_name_element.text
            product_names.append(product_name)

            # # Extract product quantity
            # product_quantity_element = card.find_element(By.XPATH, f'{xpath}/div/div[3]/div[2]/div[1]/div[2]/div/div[1]')
            # product_quantity = product_quantity_element.text
            # product_quantities.append(product_quantity)
            
            # Extract delivery time
            delivery_time_element = card.find_element(By.XPATH, f'{xpath}/div/div[3]/div[1]/div[1]/div/div[2]')
            delivery_time = delivery_time_element.text
            delivery_times.append(delivery_time)
            
            # Extract price to consumer
            price_to_consumer_element = card.find_element(By.XPATH, f'{xpath}/div/div[3]/div[2]/div[2]/div[1]/div[1]')
            price_to_consumer = price_to_consumer_element.text
            prices_to_consumer.append(price_to_consumer)
            
            # Extract actual price
            actual_price_element = card.find_element(By.XPATH, f'{xpath}/div/div[3]/div[2]/div[2]/div[1]/div[2]')
            actual_price = actual_price_element.text
            actual_prices.append(actual_price)
            
            # Extract discount
            discount_element = card.find_element(By.XPATH, f'{xpath}/div/div[1]/div')
            discount = discount_element.text
            discounts.append(discount)
        except NoSuchElementException as e:
            print(f"Error occurred while scraping product {i}: {e}")
            pass

    # for i in range(len(product_names)):
    #     print("Product Name:", product_names[i])
    #     # print("Product Quantity:", product_quantities[i])
    #     print("Delivery Time:", delivery_times[i])
    #     print("Price to Consumer:", prices_to_consumer[i])
    #     print("Actual Price:", actual_prices[i])
    #     print("Discount:", discounts[i])
    #     print("---------------------------------------")

    data_rows = list(zip(product_names, delivery_times, prices_to_consumer, actual_prices, discounts))

    csv_file_path = 'product_data.csv'

    headers = ["product_names", "delivery_times", "prices_to_consumer", "actual_prices", "discounts"]

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(headers)
        
        for row in data_rows:
            writer.writerow(row)


def vishal_mm(query):
    driver_path = r"C:\Users\shiva\chromedriver_win32\chromedriver.exe"

    # Create ChromeOptions object
    options = Options()

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    # Navigate to the desired website
    driver.get(f'https://www.vishalmegamart.com/en-in/search?q={query}&search-button=&lang=en_IN')

    time.sleep(3)
    try:
        button1_xpath = '/html/body/div[1]/header/nav/div[2]/div[1]/div/div[2]/div/button'
        button1 = driver.find_element(By.XPATH, button1_xpath)
        driver.execute_script("arguments[0].click();", button1)

        button2_xpath = '/html/body/div[1]/header/nav/div[2]/div[1]/div/div[2]/div/div[2]/button[1]'
        button2 = driver.find_element(By.XPATH, button2_xpath)
        driver.execute_script("arguments[0].click();", button2)

        location_input_xpath = '//*[@id="ipt-store-finder-addressbook"]'
        location_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, location_input_xpath)))
    except Exception as e:
        print("Exception occurred while executing the code:", e)
        return

    if location_input:
        print("Location input found successfully.")

    # Clear the location input field
    location_input.clear()

    # Type "110001" directly into the location input field
    location_input.send_keys("110")
    time.sleep(1)
    location_input.send_keys("001")
    time.sleep(1)
    location_input.send_keys(Keys.ARROW_DOWN)
    location_input.send_keys(Keys.RETURN)


    # # Wait for the autocomplete options to appear
    # autocomplete_options_xpath = '//div[@class="LocationSearchList__LocationLabel-sc-93rfr7-2 ixiZXd"]'
    # autocomplete_options = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, autocomplete_options_xpath)))

    # if autocomplete_options:
    #     print("Autocomplete options found successfully.")

    # # Iterate through the autocomplete options and select "New Delhi, Delhi 110001, India"
    # for option in autocomplete_options:
    #     if option.text == "New Delhi, Delhi 110001, India":
    #         try:
    #             # Scroll to the element using JavaScript
    #             driver.execute_script("arguments[0].scrollIntoView(true);", option)
                
    #             # Click on the element using JavaScript
    #             driver.execute_script("arguments[0].click();", option)
    #             break
    #         except Exception as e:
    #             print("Exception occurred while clicking:", str(e))
    
    button_xpath = '//*[@id="changeAddressPopup"]/div[1]/div/div/div[2]/button'
    button = driver.find_element(By.XPATH, button_xpath)
    driver.execute_script("arguments[0].click();", button)
    print("Location selected successfully.")
    time.sleep(2)
    driver.execute_script("window.scrollBy(0,500)", "")

    product_names = []
    # prices_to_consumer = []
    # actual_prices = []
    # discounts = []
    flag = True
    for i in range(1, 11):
        try:
            
            xpath = f'//*[@id="product-search-results"]/div[2]/div[2]/div[2]/div[{i}]/div'
            card = driver.find_element(By.XPATH, xpath)

            # Extract product name
            product_name_element = card.find_element(By.XPATH, f'{xpath}/div/div[2]/div[2]/h2')
            product_name = product_name_element.text
            product_details = card.find_element(By.XPATH, f'{xpath}/div/div[2]/div[2]/a').text
            product_names.append(product_name + " " + product_details)

            # # Extract product quantity
            # product_quantity_element = card.find_element(By.XPATH, f'{xpath}/div/div[3]/div[2]/div[1]/div[2]/div/div[1]')
            # product_quantity = product_quantity_element.text
            # product_quantities.append(product_quantity)
            
            # # Extract price to consumer
            # price_to_consumer_element = card.find_element(By.XPATH, f'{xpath}/div/div[2]/div[3]/span[2]/span[1]')
            # price_to_consumer = price_to_consumer_element.text
            # prices_to_consumer.append(price_to_consumer)
            
            # # Extract actual price
            # actual_price_element = card.find_element(By.XPATH, f'{xpath}/div/div[2]/div[3]/span[1]/span')
            # actual_price = actual_price_element.text
            # actual_prices.append(actual_price)
            
            # # Extract discount
            # discount_element = card.find_element(By.XPATH, f'{xpath}/div/div[2]/div[3]/span[2]/span[2]')
            # discount = discount_element.text
            # discounts.append(discount)
            if i > 7 and flag:
                driver.execute_script("window.scrollBy(0,400)", "")
                flag = False
                time.sleep(2)

        except NoSuchElementException as e:
            print(f"Error occurred while scraping product {i}: {e}")
            pass

    for i in range(len(product_names)):
        print("Product Name:", product_names[i])
        # print("Product Quantity:", product_quantities[i])
        # print("Price to Consumer:", prices_to_consumer[i])
        # print("Actual Price:", actual_prices[i])
        # print("Discount:", discounts[i])
        print("---------------------------------------")

    # data_rows = list(zip(product_names))

    # csv_file_path = 'product_data.csv'

    # headers = ["product_names"]

    # with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
        
    #     writer.writerow(headers)
        
    #     for row in data_rows:
    #         writer.writerow(row)

if __name__ == "__main__":
    blinkit()