'''
This is a program designed to auto fill YZU easy test by using selenium webdriver.
The score is not guaranteed use this program at your own risk!
You can freely modify the code as you wish.
'''
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser #for login information config file
import os
from random import randrange #rand for answer

def clickalert():
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    sleep(0.5)



#config setup
configFilename = 'accounts.ini'
if not os.path.isfile(configFilename):
    with open(configFilename, 'a') as f:
        f.writelines(["[Default]\n", "Account= your account\n", "Password= your password\n", "Course= your course"])
        print('input your username and password in accounts.ini')
        exit()
# get account info fomr ini config file
config = configparser.ConfigParser()
config.read(configFilename)
Account = config['Default']['Account']
Password = config['Default']['Password']
Course = config['Default']['Course']




driver = webdriver.Chrome("./chromedriver.exe")
driver.get("http://140.138.36.177/")
driver.find_element_by_name("cust_id").send_keys(Account)
driver.find_element_by_name("cust_pass").send_keys(Password)
driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/form/fieldset/input").click()
sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/a[1]").click()
sleep(1)
choice = Select(driver.find_element_by_name("choice")) # choose class here
choice.select_by_value(Course)#Course number here
sleep(1)
driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/p[1]/a/img").click()
sleep(1)
#driver.switch_to_alert().accept()

window_before = driver.window_handles[0]#store the old window handle
driver.find_element_by_xpath("/html/body/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr/td/a[1]").click() # choose the test you want to take here

#driver.switch_to_alert().dismiss()

window_after = driver.window_handles[1]#store the new window handle
driver.switch_to_window(window_after)
sleep(1)
for test in range(1,11):
    driver.find_elements_by_name(f"q{test}")[randrange(4)].click()
    sleep(0.1)
    if(test != 10):
        driver.find_element_by_xpath(f"/html/body/table[3]/tbody/tr/td[2]/form/table[{test}]/tbody/tr[5]/td/center/img").click()
        sleep(0.1)

driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/table[10]/tbody/tr[5]/td/center/input").click()
sleep(0.5)
clickalert()

for test in range(1,31):
    driver.find_elements_by_name(f"q{test}")[randrange(3)].click()

driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/a[30]/center/input").click()
clickalert()

for test in range(1,31):
    driver.find_elements_by_name(f"q{test}")[randrange(4)].click()

driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/a[30]/center/input").click()
clickalert()

for test in range(1,31):
    driver.find_elements_by_name(f"q{test}")[randrange(4)].click()

driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/a[30]/center/input").click()
clickalert()

for test in range(1,41):
    driver.find_elements_by_name(f"q{test}")[randrange(4)].click()

driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/a[40]/center/input").click()
clickalert()

for test in range(1,13):
    driver.find_elements_by_name(f"q{test}")[randrange(4)].click()

driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[2]/form/a[12]/center/input").click()
clickalert()

for test in range(1,49):
    randnum = randrange(4)
    print(f"q{test} : {randnum}")
    driver.find_elements_by_name(f"q{test}")[randnum].click()

