from functools import update_wrapper
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
from base64 import b64decode
import os
import pyautogui
from dbconnect import database

captcha_killer_url = 'https://brandfolder.com/workbench/extract-text-from-image'
myDB = database()


def CaptchaKiller(adriver):

    we = adriver.find_element_by_xpath("//img[@alt='Captcha']").get_attribute('src')
    #print(we)
    with open("imageToSave.png", "wb") as fh:
        im = Image.open(BytesIO(b64decode(we.split(',')[1])))
        im.save("image.png")    


    decode_driver = webdriver.Chrome()

    decode_driver.get(captcha_killer_url)
    time.sleep(3)
    uploader = decode_driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/div/div/input')
    
    uploader.send_keys("C://Users/thatp/GIt/yell_scraper/image.png")
    time.sleep(5)

    decoded = decode_driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/textarea').text
    decode_driver.close()
    decoded = decoded.strip(' ')
    return(decoded)

    

class captchaError(Exception):
    pass

biz_list = []



def saveBuss(url):

    appended = False
    this_biz = {
        "Name": "",
        "Contact Number": 0,
        "Address" : "",
        "website" : ""
    }
    while not (appended):
        url_driver = webdriver.Chrome()
        url_driver.get(url)
        time.sleep(2.5)
        done = 0
        #Captcha killer
        try:
            text_box = url_driver.find_element_by_xpath('/html/body/form/input[1]')
            solve = CaptchaKiller(url_driver)
            text_box.send_keys(solve)
            print(solve)


            upload_button = url_driver.find_element_by_xpath('/html/body/form/input[2]')
            upload_button.click()

            time.sleep(3)
        except Exception as e:
            print(str(e))



        try:
            names = url_driver.find_elements_by_class_name('businessCard--businessName')
            this_biz['Name'] = names[0].text
            appended = True
        except:
            print("Error getting name, this is very unusual.")
        
        #Get phone number

        try:
            phone_numbers = url_driver.find_elements_by_class_name('business--telephoneNumber')
            this_biz['Contact Number'] = phone_numbers[0].text
            appended = True

        except:
            print("Error getting phone number, maybe not available")

        #Get address of business
        addy = ''
        try:
            postcode = url_driver.find_elements_by_class_name("address")
            for item in postcode:
                addy = addy + item.text
            this_biz["Address"] = addy
            appended = True

        except:
            print("Error getting address")

        #Get website
        try:
            websites = url_driver.find_elements_by_class_name('businessCard--callToAction')
            this_biz['website'] = (websites[0].get_attribute('href'))
            appended = True
        except:
            print("Error getting website url")
            
        print(this_biz)
        url_driver.close()
        if(this_biz['Name'] != ""):
            commit_sql = ("""INSERT INTO it (Name, address, phone_number, website) VALUES ('{}','{}','{}','{}');""").format(this_biz['Name'], this_biz["Address"], this_biz["Contact Number"], this_biz["website"])
            print(commit_sql)
            myDB.commit_db(commit_sql)
            biz_list.append(this_biz)
            return True




    

old_search_terms = ['Computer design', 'Computer Engineering', 'Digital solutions', 'Computer solutions', 'Digital Engineering', 'bespoke electronics', 'Computer aided design', 'CAD']
search_terms = ['Computer security', 'cctv installers', 'Opticians', 'sign makers', 'surveyors']


yell_url = 'https://www.yell.com/'
postcode = 'Croydon'

for business in search_terms:
    driver = webdriver.Chrome()
    driver.get(yell_url)
    completed = 0

    while(completed < 1):
        try:
            #input business details

            business_search = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div/section/div/div/div/form/fieldset/div[1]/div[1]/div/div/div/input')
            business_search.send_keys(business)

            postcode_search = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div/section/div/div/div/form/fieldset/div[1]/div[2]/div/div/div/input')
            postcode_search.send_keys(postcode)

            #Search for businesses
            search_button = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div/section/div/div/div/form/fieldset/div[1]/div[3]/button')
            search_button.click()

            time.sleep(0.4)

            links = driver.find_elements_by_class_name("businessCapsule--title")
            completed = 10
            for item in links:
                time.sleep(0.2)
                url = (item.get_attribute('href'))
                saveBuss(url)
                print("Downloaded ---")

            
        except:
            text_box = driver.find_element_by_xpath('/html/body/form/input[1]')
            solve = CaptchaKiller(driver)
            text_box.send_keys(solve)
            print(solve)


            upload_button = driver.find_element_by_xpath('/html/body/form/input[2]')
            upload_button.click()

            time.sleep(3)
            
print(len(biz_list))