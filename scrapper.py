from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from captch_reader import solve_captcha

import os
import asyncio


def create_driver():
    options = Options()
    # To Browser in Run in headless mode
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    return driver



async def submit_case_details(url, case_type, case_number, year):
    driver = create_driver()
    driver.get(url)

    if not driver:
        raise Exception("Session expired or invalid")

    try:

        # Defining Wait Driver 
        wait = WebDriverWait(driver,10)
        # Wait for a specific element on the next page to load in order to proceed
        wait.until(
        EC.presence_of_element_located((By.ID, "captcha_image"))  # Adjust this to the first reliable element
        )


        # got Details from the form
        # print(f"Submitting case form with details: {case_type}, {case_number}, {year}, {captcha_text}")
        # # Fill form
        driver.find_element(By.ID, "case_type").send_keys(case_type)
        driver.find_element(By.ID, "search_case_no").send_keys(case_number)
        driver.find_element(By.ID, "rgyear").send_keys(year)

        # Trying Multiple Times for captcha filling
        # max_attempts = 4
        # for attempt in range(max_attempts):
        #     # GEtting the captcha Image and saving it and getting it's text
        #     captcha_image = driver.find_element(By.ID, "captcha_image")
        #     captcha_image.screenshot("static/captcha.jpg")

        #     # Getting Captcha box to sent captch text

        #     captcha_input_box = driver.find_element(By.ID,"captcha")
        #     # Based on the saved image getting the captac text from the user

        #     if os.path.exists("static/captcha.jpg"):
        #         # Giving this image path to the captch_reader to get the image text
        #         captcha_text = await solve_captcha("static/captcha.jpg")

        #         captcha_input_box.clear()
        #         captcha_input_box.send_keys(captcha_text)
                
        #         # Printing captured Captch
        #         print("Captcha Text : ",captcha_text)

        #     driver.find_element(By.NAME, "submit1").click()

        #     # Wait for results to load
        #     time.sleep(5)

        #     # Getting the status of the submission
        #     submit_status = driver.find_element(By.ID,"txtmsg").get_attribute("title")
        #     print("Submit Status :",submit_status)
        #     print("Submit Status :",type(submit_status))

        #     if submit_status is None or submit_status.strip() == "" or "Invalid" not in submit_status:
        #         print("captcha Solved Successfully!")
        #         break
        #     else:
        #         print(f"Got Invalid Captcha Atempt : {attempt+1}")
        #         submit_status = ""

        max_attempts = 5
        captcha_solved = False
        for attempt in range(max_attempts):
            # Screenshot captcha
            captcha_image = driver.find_element(By.ID, "captcha_image")
            captcha_image.screenshot("static/captcha.jpg")

            captcha_input_box = driver.find_element(By.ID, "captcha")
            captcha_text = await solve_captcha("static/captcha.jpg")
            captcha_input_box.clear()
            captcha_input_box.send_keys(captcha_text)

            print("Captcha Text:", captcha_text)
            driver.find_element(By.NAME, "submit1").click()

            try:
                # Check if result table is present
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#showList1 a")))

                # got Details from the form
                print(f"Submitting case form with details: {case_type}, {case_number}, {year}")

                ## Now, Since we have submitted details i want to click on the view button for more details 
                ## And then, pass the driver to another funtion to extract all the details about the case
                driver.find_element(By.CSS_SELECTOR,"#showList1 a").click()
                time.sleep(5)


                # After Getting to the case details page 
                # Saving this page to get the required Details 
                # Getting the Inner HTML from the page
                case_page = driver.find_element(By.ID,"secondpage").get_attribute("innerHTML")

                # Saving This Details Page For further processing
                if not os.path.exists("scrapped_page"):
                    os.mkdir("scrapped_page")


                with open("scrapped_page/case_details.html","w") as file:
                    file.write(case_page)

                print("CAPTCHA solved and result page loaded!")
                captcha_solved = True
                break
            except:
                # Try to get any error message
                try:
                    submit_status = driver.find_element(By.ID, "txtmsg").get_attribute("title")
                    print("Submit Status:", submit_status)
                except:
                    submit_status = None

                print(f"Got Invalid Captcha Attempt: {attempt + 1}")

        # If captch is not solved 
        if not captcha_solved:
            print("There was problem while solving the captcha sorry for inconvience")
    except Exception as e:
        print("Error : ",e)
    finally:
        # driver.quit()
        print("Driver Session Closed")


if __name__ == "__main__":
    url = "https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no.php?state_cd=16&dist_cd=1&court_code=1&stateNm=Calcutta"  # Replace with the URL you want to scrape
    # scrape_data(url)
    asyncio.run(submit_case_details(url, "APOT - TEMP APO(32)", "26", "2024")) 