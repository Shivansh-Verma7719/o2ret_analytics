#better to run this code in jupyter environment than sublime text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

# Read the Excel file
a = pd.read_excel("Apollo Pharmacy Universe of Stores with store links-2.xlsx")

# Get the product name from the user
keyword = input("Enter the product name: ")

# Set the path to the ChromeDriver executable
driver_path = r"C:\Users\Aaryan Naithani\chromedriver-win64\chromedriver.exe"

# Function to initialize the WebDriver
def init_driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)

# Function to scrape availability information for a given link
def scrape_availability(driver, link, keyword):
    availability_results = []
    try:
        driver.get(link)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[6]/div/p/span"))
        ).click()
    except TimeoutException:
        print(f"Error in link : {link}")
        return availability_results

    try:
        product_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/input"))
        )
        product_input.clear()
        product_input.send_keys(keyword)
        product_input.send_keys(Keys.ENTER)
    except TimeoutException:
        print(f"Error viewing product for pincode: {link}")
        return availability_results

    try:
        product_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='SearchMedicine_searchList__Vpj_3']/li/div/div[2]/h4"))
        )
        products = [element.text for element in product_elements]
    except TimeoutException:
        print(f"Error extracting product names: {link}")
        return availability_results

    for product in products:
        try:
            product_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/input"))
            )
            product_input.clear()
            product_input.send_keys(product)
            product_input.send_keys(Keys.ENTER)
        except TimeoutException:
            print(f"Error entering product title: {product}")
            availability_results.append((product, "n/a"))
            continue

        try:
            # Retry mechanism for clicking the product link
            retries = 3
            while retries > 0:
                try:
                    matching_product = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, f"//ul[@class='SearchMedicine_searchList__Vpj_3']/li/div/div[2]/h4[text()='{product}']"))
                    )
                    matching_product.click()
                    break
                except StaleElementReferenceException:
                    retries -= 1
                    if retries == 0:
                        raise

        except (TimeoutException, NoSuchElementException):
            try:
                first_product = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='SearchMedicine_searchList__Vpj_3']/li/div/div[2]/h4"))
                )
                first_product.click()
            except TimeoutException:
                availability_results.append((product, "n/a"))
                continue

        try:
            avail_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'StoreDetails_availBx__0XvAH'))
            )
            try:
                label_text = avail_box.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[6]/div/label').text
                availability_results.append((product, label_text))
            except NoSuchElementException:
                availability_results.append((product, "Label not found"))
        except TimeoutException:
            availability_results.append((product, "n/a"))

        try:
            search_another_medicine = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='StoreDetails_orangeLink__QcZPT']"))
            )
            search_another_medicine.click()
        except TimeoutException:
            print(f"Error clicking 'Search Another Medicine': {link}")

    return availability_results

# Main execution
if __name__ == "__main__":
    final_results = []

    for i in range(a.shape[0]):  # Use range(a.shape[0]) to loop through all links
        link = str(a.iloc[i, 0])
        store_name = str(a.iloc[i, 1])  # Assuming store name is in the second column
        driver = init_driver()
        availability_results = scrape_availability(driver, link, keyword)
        driver.quit()
        
        # Print results for the current link
        print(f"Availability information for {store_name}:")
        for product, availability in availability_results:
            print(f"{product}: {availability}")
            final_results.append({"Store": store_name, "Product": product, "Availability": availability})

    # Create a DataFrame from the final results
    df = pd.DataFrame(final_results)
    print(df)

    # Save the DataFrame to an Excel file
    df.to_excel("availability_results.xlsx", index=False)
