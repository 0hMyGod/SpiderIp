import requests
import random
from bs4 import BeautifulSoup
import pymysql
class Spider_Ips():
    url = 'http://www.xicidaili.com/wn/'
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]
    MAX_RETRIES = 20
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    def list_ip(self):
        req = self.session.get(self.url, headers=random.choice(self.headers))
        response = BeautifulSoup(req.text, 'html.parser')
        res_obj = response.findAll('table')
        tab = res_obj[0]
        db = pymysql.connect("localhost", "root", "", "test")
        for item in tab.findAll('tr'):
            tds = item.findAll('td')    
            if tds:
                # 打开数据库连接
                
                cursor = db.cursor()
                sql = 'insert into iplist(ip,ip_port) values ("%s", "%s") ' % (tds[1].text, tds[2].text)
                print(sql)
                try:
                    cursor.execute(sql)
                    db.commit()
                    print('success')
                except:
                    db.rollback()
                #with open('HTTPS.txt', 'a', encoding='utf-8') as f:
                   # print(tds[1].text+':'+tds[2].text)
                    #f.write(tds[1].text+':'+tds[2].text+'\n')   
        db.close()                 

    def __init__(self):
        self.list_ip()


s_ip = Spider_Ips()

