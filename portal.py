#Quick and easy way to open YZU Portal?
import configparser
from selenium import webdriver
import os
from time import sleep



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

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx") 
driver.find_element_by_name("Txt_UserID").send_keys(Account)
driver.find_element_by_name("Txt_Password").send_keys(Password)
sleep(0.5)
driver.find_element_by_name("ibnSubmit").click()

