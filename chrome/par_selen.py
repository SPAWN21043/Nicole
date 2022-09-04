import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


useragent = UserAgent()


def selen_auth(salon, usluga, master, data, time_user, phone_user, password_user):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={useragent.random}')
    options.add_argument("--window-size=1024,768")
    '''options.add_argument("--disable-blink-features=AutomationControlled")'''
    '''options.headless = True'''

    url = f'https://dikidi.app/{salon}?p=4.pi-po-sm-ss-sd&o=1&m={master}&s={usluga}'

    s = Service(executable_path='/home/aleksey/Project/Nicole/chrome/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    try:
        driver.get(url=url)
        time.sleep(5)

        data_clic = driver.find_element(By.XPATH, f'//li[@data-date="{data}"]')

        webdriver.ActionChains(driver).move_to_element(data_clic).click(data_clic).perform()
        '''data_clic.click()'''
        print('data')
        time.sleep(5)

        time_click = driver.find_element(By.XPATH, f"//*[contains(text(), '{time_user}')]")
        time_click.click()
        time.sleep(5)

        '''time_click = driver.find_element(By.XPATH, f"//span[text()='{time_user}']")
        time_click.click()
        print('vremya')
        time.sleep(5)'''

        click_icon = driver.find_element(By.XPATH, '//img[@src="/assets/images/mobile/company_bg.svg"]')
        click_icon.click()
        print('avto')
        time.sleep(5)

        auth = driver.find_element(By.XPATH, '//div[@class="nr-auth-text-body"]')
        auth.click()
        print('avto')
        time.sleep(5)

        phone = driver.find_elements(By.XPATH, "//a[text()='Мобильный номер']")
        phone[1].click()
        print('mob')
        time.sleep(5)

        phone_input = driver.find_elements(By.XPATH, "//input[@name='number']")
        phone_input[1].clear()
        time.sleep(3)

        username = driver.find_elements(By.XPATH, "//input[@name='number']")
        username[1].send_keys(f"{phone_user}")
        time.sleep(5)
        pre = driver.find_elements(By.XPATH, "//input[@type='password']")
        print(len(pre))
        time.sleep(5)

        password = driver.find_element(By.XPATH, "//input[@type='password']")

        password.send_keys(f"{password_user}")
        time.sleep(5)

        button_user = driver.find_elements(By.XPATH, "//div[@class='form-group footer']")
        button_user[1].click()
        time.sleep(5)

        alert_yes = driver.find_elements(By.XPATH, "//div[text()='Неверный логин или пароль']")
        allarm = len(alert_yes)

        if allarm == 1:
            bt_s_ok = driver.find_elements(By.XPATH, "//button[text()='Ок']")

            bt_ok = driver.find_element(By.XPATH, "//button[text()='Ок']")
            bt_ok.click()

            return 'Неверный логин или пароль'

        else:

            button_auth = driver.find_element(
                By.XPATH, "//a[@class='btn btn-block btn-default btn-stylized nrs-gradient nr-continue']"
            )
            button_auth.click()
            time.sleep(3)

            return f'Вы записаны!\n' \
                   f'Дата: {data}, Время: {time_user}.'

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
