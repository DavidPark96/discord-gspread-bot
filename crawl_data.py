import requests
from bs4 import BeautifulSoup
import datetime
from urllib import parse #url decode
def get_data(url):
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }
    if "naver" in url:
        response = requests.get(url, headers=header)
        if response.history: #모바일의 경우 리다이렉트
            print("Request was redirected")
            url = parse.unquote(response.url) #url 디코딩
            url = url.replace('https://link.naver.com/bridge?url=','') #이걸 삭제해야 원래 주소가 나옴.
            response = requests.get(url, headers=header)
        else:
            print("Request was not redirected")

        soup = BeautifulSoup(response.text, 'html.parser')

        date = soup.select_one(".media_end_head_info_datestamp_time") #날짜 원문 '2022.10.14. 오전 7:00'
        date_str = date.text.split()[0] #'2022.10.14.'
        date_obj = datetime.datetime.strptime(date_str, '%Y.%m.%d.') #날짜 '2022-10-14'
        date = date_obj.strftime("%Y-%m-%d")

        title = soup.select_one(".media_end_head_headline").text #제목
        offer = soup.select_one(".media_end_linked_more_point").text #언론사
        classification = "네이버 뉴스"
        return str(date), str(title), str(offer), classification

    elif "youtu" in url: #모바일은 youtu.be
        response = requests.get(url, headers=header)
        if response.history: #모바일의 경우 리다이렉트
            print("Request was redirected")
            response = requests.get(response.url, headers=header)
        else:
            print("Request was not redirected")

        soup = BeautifulSoup(response.text, 'html.parser')

        date = str(soup.find("meta", itemprop="datePublished")).split('"')[1] #.text가 안되서 split을 사용함. (원인 찾아보기.) #datePublished, uploadDate 택1
        title = str(soup.find("meta",property="og:title")).split('"')[1]
        offer = str(soup.find("link", itemprop="name")).split('"')[1] #채널 이름
        classification = "유튜브"
        return str(date), str(title), str(offer), classification
    
    else:
        print("유튜브, 네이버 링크가 아님.")