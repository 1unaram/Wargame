from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# selenium setting
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)


# Webhacking.kr Login
loginURL = 'https://webhacking.kr/login.php'
driver.get(loginURL)

sleep(3)

uid = input('Input ID : ')
upass = input('Input PASS : ')

driver.find_element(
    By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/form/table/tbody/tr[1]/td[2]/input').send_keys(uid)
driver.find_element(
    By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/form/table/tbody/tr[2]/td[2]/input').send_keys(upass)
driver.find_element(
    By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/form/input').click()


# Move to challenge page
URL = 'https://webhacking.kr/challenge/code-4/'
driver.get(URL)


# Input
driver.find_element(
    By.XPATH, '/html/body/form/table/tbody/tr[1]/td[2]/input').send_keys('HI')
driver.find_element(
    By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/input').send_keys('HI')

captcha = driver.find_element(By.XPATH,
                              '/html/body/form/table/tbody/tr[3]/td[2]/input[2]').get_attribute('value')
driver.find_element(By.XPATH,
                    '/html/body/form/table/tbody/tr[3]/td[2]/input[1]').send_keys(captcha)
driver.find_element(By.XPATH,
                    '/html/body/form/table/tbody/tr[4]/td[1]/input').click()

print("SOLVED!")
