import requests
import re
from bs4 import BeautifulSoup

def create_soup(url):

    headers = headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrape_weather():

    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%95%88%EC%82%B0+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=U36amlp0J1sssPcpnPCsssssta0-229390"
    soup = create_soup(url)

    # 현재 날씨 종합 정보 (ex : 흐림, 어제보다 3˚C 낮아요)
    info = soup.find("p", attrs={"class" : "cast_txt"}).get_text()
    # 현재 온도, 최저 온도, 최고 온도
    temperature = soup.find("span", attrs={"class" : "todaytemp"}).get_text()
    min_temp = soup.find("span", attrs={"class" : "min"}).get_text()
    max_temp = soup.find("span", attrs={"class" : "max"}).get_text()
    # 오전 강수확률, 오후 강수확률
    morning_rain_rate = soup.find("span", attrs={"class" : "point_time morning"}).get_text()
    afternoon_rain_rate = soup.find("span", attrs={"class": "point_time afternoon"}).get_text()
    # 미세먼지, 초미세먼지
    dust = soup.find("dl", attrs={"class" : "indicator"})
    fine_dust = dust.find_all("dd")[0].get_text()
    ultra_fine_dust = dust.find_all("dd")[1].get_text()

    print("[오늘의 날씨]")
    print(info)
    print("현재 {}˚C (최저 {}C / 최고 {}C)".format(temperature, min_temp, max_temp))
    print("오전 :", morning_rain_rate.strip(), "오후 :", afternoon_rain_rate.strip())
    print()
    print("미세먼지", fine_dust)
    print("초미세먼지", ultra_fine_dust)
    print()


def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class" : "hdline_article_list"}).find_all("li", limit=3) # 3개만 가져오기
    for idx, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print("{}. {}".format(idx+1, title))
        print("(링크 : {})".format(link))
    print()



def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)

    news_list = soup.find("ul", attrs={"class" : "type06_headline"}).find_all("li", limit=3) # 3개만 가져오기
    for idx, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1
        title = news.find_all("a")[a_idx].get_text().strip()
        link = news.find("a")["href"]
        print("{}. {}".format(idx+1, title))
        print("(링크 : {})".format(link))
    print()

def scrape_daily_eng():

    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_gnb_eng_I_others_english&logger_kw=haceng_submain_gnb_eng_I_others_english"
    soup = create_soup(url)

    contexts = soup.find_all("div", attrs= {"id" :re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for context in contexts[len(contexts)//2:]: # 8문장이 있다고 가정할 때, index 기준 4~7까지 잘라오기
        print(context.get_text().strip())
    print()
    print("(한글 지문)")
    for context in contexts[:4]:
        print(context.get_text().strip())

if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news() # 헤드라인 뉴스 가져오기
    scrape_it_news() # IT 뉴스 정보 가져오기
    scrape_daily_eng() # 오늘의 영어 회화 가져오기