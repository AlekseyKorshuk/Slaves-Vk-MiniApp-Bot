'''
Program that updates fetters automatically in MiniApp "Рабы": https://vk.cc/c01jmF
'''

from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait


#############    All needed settings    #############################


login = "PHONEOREMAIL"
password = "PASSWORD"


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(30)

#####################################################################

profile = "https://vk.com/app7794757"
balance_path = '//*[@id="panel_main"]/div/div[3]/div[2]/div/div[1]/div/div[2]'
slaves_path = 'SlaveMobile__holder'
buy_okov_path = '//*[@id="panel_user"]/div/div[4]/div/div/button[1]/div/div'
user_name = '//*[@id="panel_user"]/div/div[3]/div[1]/div[2]'
exit_button = '//*[@id="panel_user"]/div/div[2]/div/div[1]/div'

driver.get(profile)
driver.find_element_by_xpath('//*[@id="quick_email"]').send_keys(login)
driver.find_element_by_xpath('//*[@id="quick_pass"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="quick_login_button"]').click()
time.sleep(5)


while True:
    driver.get(profile)
    time.sleep(5)
    frame = driver.find_element_by_xpath('//*[@id="app_7794757_container"]').find_element_by_tag_name('iframe')
    driver.switch_to.frame(frame)
    wait = WebDriverWait(driver, 10)
    balance = int(str(driver.find_element_by_xpath(balance_path).text).replace(" ",""))

    slaves = driver.find_elements_by_class_name(slaves_path)

    i = 0
    for i in range(len(slaves)):

        try:
            slaves[i].find_element_by_class_name('SlaveMobile__chain-holder')
        except:
            try:
                driver.execute_script("arguments[0].scrollIntoView();",
                                      slaves[i].find_element_by_class_name('SlaveMobile__avatar-holder'))
            except:
                pass

            try:
                slaves[i].click()
            except:
                slaves[i].find_element_by_class_name('SlaveMobile__avatar-holder').click()
            driver.find_element_by_xpath(user_name)
            buttons = driver.find_element_by_xpath('//*[@id="panel_user"]/div/div[4]/div/div').find_elements_by_tag_name(
                'button')
            if len(buttons) == 2:
                driver.find_element_by_xpath(buy_okov_path).click()
                print("buy")

            break

    time.sleep(300)

