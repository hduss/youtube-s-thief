import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def main():
    driver_exe = 'chromedriver'
    options = Options()
    # Disable display chrome browser
    #options.add_argument("--headless")
    driver = webdriver.Chrome(driver_exe, options=options)
    driver.get("https://www.youtube.com/channel/UCS08XVYyOCxYvZNtovqdaAQ/playlists")

    # loginButton = driver.find_element(By.CLASS_NAME, 'WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb')

    try:
        # Click on login button
        loginButton = driver.find_element(By.CLASS_NAME, "uqeIBc")
        loginButton.click()
        print('click OK')

        # Fill email form
        element = driver.find_element(By.ID, "identifierId")
        element.send_keys("tdelmas26@gmail.com")

        print('Fill email OK')

        # CLick on next
        element = driver.find_element(By.ID, "identifierNext")
        element.click()

        print('click 2 OK')







    except:
        print('Erreur de select')
    # print(loginButton)
    # content = driver.page_source.encode('utf-8').strip()

    # soup = BeautifulSoup(content, 'lxml')
    # print(content)

    time.sleep(5)


main()
