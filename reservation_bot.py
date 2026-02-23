# 셀레니움 기본 템블릿
import json
import time

import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

reservation_complete = False


def check():
    global reservation_complete
    # 크롬 드라이버 생성
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    # 이미지 로딩 비활성화로 속도 향상
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    try:
        day = time.gmtime().tm_mday + 15
        driver = webdriver.Chrome(options=options)

        # url 접속
        ticket_data = "2026-03-02"
        target_time = "11:55"
        driver.get(f'https://www.xn--2e0b040a4xj.com/reservation?branch=4&theme=22&date={ticket_data}#list')
        # driver.get(f'https://www.xn--2e0b040a4xj.com/reservation?branch=4&theme=13&date=2026-02-23#list')
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.active1.eveReservationButton")

        for btn in buttons:
            hidden_element = btn.find_element(By.CSS_SELECTOR, "div.eveHiddenData")
            hidden_data = driver.execute_script("return arguments[0].textContent;", hidden_element)
            data = json.loads(hidden_data)
            if data['time'] == target_time:
                print(f"찾았다! 테마: {data['theme']}, 시간: {data['time']}")
                btn.click()
                time.sleep(1)
                break

        name_input = driver.find_element(By.CSS_SELECTOR, "input[name='name']")
        name_input.send_keys("이동호")

        phone_input = driver.find_element(By.CSS_SELECTOR, "input[name='phone']")
        phone_input.send_keys("010-4819-6169")

        select_element = driver.find_element(By.ID, "evePeople")
        select = Select(select_element)
        select.select_by_value("2")

        payment_label = driver.find_element(By.CSS_SELECTOR, "label.el-rc.bs-bb")
        driver.execute_script("arguments[0].click();", payment_label)

        agree_label = driver.find_element(By.CSS_SELECTOR, "label.el-rc.fw7")
        driver.execute_script("arguments[0].click();", agree_label)

    except Exception as err:
        print(err)
    finally:
        print("예약완료")
        # driver.quit()


if __name__ == "__main__":
    check()
    # schedule.every().day.at("15:00").do(check)
    # schedule.every(1).seconds.do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)
