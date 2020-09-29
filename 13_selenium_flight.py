from selenium import webdriver # 크롬 버전에 맞는 chromedriver.exe 가 반드시 있어야 함!
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

url = "https://flight.naver.com/flights/"
browser.get(url) # url로 이동

# 가는날 선택 클릭
browser.find_element_by_link_text("가는날 선택").click()

# 이번달 28, 29일 선택
# browser.find_elements_by_link_text("28")[0].click() # [0] -> 이번달
# browser.find_elements_by_link_text("29")[0].click() # [1] -> 이번달

# 다음달 28, 29일 선택
# browser.find_elements_by_link_text("28")[1].click() # [1] -> 다음달
# browser.find_elements_by_link_text("29")[1].click() # [1] -> 다음달

# # 이번달 28일, 다음달 29일 선택
browser.find_elements_by_link_text("28")[0].click() # [0] -> 다음달
browser.find_elements_by_link_text("29")[1].click() # [1] -> 다음달

# 제주도 선택
browser.find_element_by_xpath("//*[@id='recommendationList']/ul/li[1]").click()

# 항공권 검색 클릭
browser.find_element_by_link_text("항공권 검색").click()

try:
    elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[2]/div/div[4]/ul/li[1]")))
    # 성공했을 때 동작 수행
    print(elem.text) # 첫번째 결과 출력
finally:
    browser.quit()
