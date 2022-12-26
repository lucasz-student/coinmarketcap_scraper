from selenium import webdriver
import csv
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])


# Get driver and website
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
driver.get("https://coinmarketcap.com/historical/")

# Close Popup
try:
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/button[2]").click()
except:
    print("no popup")

time.sleep(1.5)

# list of times & actual data, will be comprehended and written into csv file
data_list = []

# loops through all the days
for i in range(13):

    # finds anchor links to days
    days = driver.find_elements_by_xpath("//div[text() = '2021']/following::a")

    # clicks on days
    driver.execute_script("arguments[0].click();", days[i])

    # obtains date year and month, creating a list
    date_month_year = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[1]/h1"
    )

    # date month year list
    list1 = date_month_year.text.split(" ")[3:6]

    # creates list of the required data
    data_descriptors = ["rank", "name", "perc1hour", "price", "volume"]

    # appends list to list of data
    data_list.append(list1)
    data_list.append(data_descriptors)

    # scrolls to bottom of page incrementally to render javascript
    y = 1000
    for timer in range(0, 9):
        driver.execute_script(f'window.scrollTo(0, "{str(y)}")')
        y += 1000
        time.sleep(1)

    # finds each row of data
    rows = driver.find_elements_by_class_name("cmc-table-row")

    # aquires data and appends to data list
    for row in rows:
        list_of_5 = []
        row = row.text.split("\n")
        list_of_5.append(row[0])
        list_of_5.append(row[1])
        list_of_5.append(row[7])
        list_of_5.append(row[4])
        list_of_5.append(row[6])
        data_list.append(list_of_5)

    # returns to original site
    driver.execute_script("window.history.go(-1)")
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[text() = '2021']/following::a"))
    )

    # comprehends list
    comprehended_list = [i for n, i in enumerate(data_list) if i not in data_list[:n]]

    # writes the data into a file at the end
    with open("t1.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(comprehended_list)
        file.close()

    print(f"Date Done {i}")

# closes driver at the end
driver.quit()
