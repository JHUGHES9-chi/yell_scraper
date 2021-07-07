from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


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

    url_driver = webdriver.Chrome()
    url_driver.get(url)
    time.sleep(2.5)
    done = 0

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
    if(appended):
        biz_list.append(this_biz)




    

    


yell_url = 'https://www.yell.com/'
postcode = 'rh164tg'
bussiness = 'Computer Busines'

driver = webdriver.Chrome()
driver.get(yell_url)
completed = 0
while(completed < 1):
    try:
        #input business details

        business_search = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div/section/div/div/div/form/fieldset/div[1]/div[1]/div/div/div/input')
        business_search.send_keys(bussiness)

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
            if(saveBuss(url)):
                print("Downloaded ---")
            else:
                raise Exception("Err downloading captcha hit")
        
    except:
        print("complete captcha plz")
        time.sleep(5)

