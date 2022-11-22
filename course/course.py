import requests
from random import randint
from time import sleep
from os.path import exists, abspath, isfile
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup as _bs
from base64 import b64encode
import json

URL = "https://portalfun.yzu.edu.tw/cosSelect/index.aspx?D=G"
#URL = "https://portal.yzu.edu.tw/cosSelect/index.aspx?D=G"
USERAGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
headers = {"User-Agent": USERAGENT}
data = {}



def bs(document):
    return _bs(document, "lxml")


def getLecCredit(url):
    url = urljoin(URL, url)
    r = requests.get(url, headers=headers)
    soup = bs(r.text)
    return {
        'num': soup.find_all(attrs={"class": "record"})[1].string.strip(),
        'link': b64encode(url.encode()).decode()
    }


def getLecHour(text):
    if ',' in text:
        hour = []
        text = text.split('-')
        for i in text:
            timesplit = i.split('        ,')
            hour.append({
                'room': timesplit[0],
                'time': timesplit[1] 
            })
        return hour
    else:
        return text.split('-')

def fuckDotNet(r):
    global data
    soup = bs(r.text)
    target = ["__EVENTTARGET", "__EVENTARGUMENT", "__LASTFOCUS", "__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]
    for i in target:
        elm = soup.find(id=i)
        if (not elm):
            raise Exception("DOTNET FORM BROKEN")
        else:
            data[i] = elm['value']


def getDeptList():
    r = requests.get(URL, headers=headers)
    soup = bs(r.text)
    with open("deptlist", "w") as deptlist:
        for i in soup.find(id="DDL_Dept").find_all("option"):
            deptlist.write(f"{i.string.strip()} {i['value']}\n")


def parseDept():
    deptId = []
    with open("deptlist", "r") as deptlist:
        for i in deptlist.readlines():
            deptId.append(i.split(' ')[1].strip())
    return deptId


def getCosChart(dept, document):
    soup = bs(document)
    hilines = list(soup.find_all(attrs={"class": "hi_line"}))
    record = list(soup.find_all(attrs={"class": "record2"}))
    lectures = []
    for i in hilines[::2]:
        tds = i.find_all("td")
        lectures.append({
            "id": tds[1].a.text,
            "dept": tds[2].text,
            "credit": getLecCredit(tds[3].a['href']),
            "type": tds[4].text,
            "time": getLecHour(tds[5].get_text(strip=True, separator='-')),
            "prof": tds[6].text,
        })
    for i in record[::2]:
        tds = i.find_all("td")
        lectures.append({
            "id": tds[1].a.text,
            "dept": tds[2].text,
            "credit": getLecCredit(tds[3].a['href']),
            "type": tds[4].text,
            "time": getLecHour(tds[5].get_text(strip=True, separator='-')),
            "prof": tds[6].text,
        })
    with open('leclist', 'a+') as f:
        for i in lectures:
            f.write(f"{json.dumps(i, ensure_ascii=False)}\n")
            
        



def getContent(req, url, headers, data):
    # dept = parseDept()
    dept = [304] # enter department in this list

    for i in dept:
        print(f"[+] {i}")
        data["__EVENTTARGET"] = "DDL_Dept"
        data['Q'] = "RadioButton1"
        data['DDL_YM'] = "109,2  "
        data['DDL_Dept'] = i
        data['DDL_Degree'] = "1"
        fuckDotNet(req.post(url, headers=headers, data=data))
        sleep(randint(1, 5) * 0.1)
        data['Q'] = "RadioButton1"
        data['DDL_YM'] = "109,2  "
        data['DDL_Dept'] = i
        data['DDL_Degree'] = "0"
        data['Button1'] = "%E7%A2%BA%E5%AE%9A"
        r = req.post(url, headers=headers, data=data)
        fuckDotNet(r)
        getCosChart(i, r.text)

if __name__ == '__main__':
    main = requests.Session()

    fuckDotNet(main.get(URL, headers=headers))
    deplistPath = abspath("deptlist")
    if (not exists(deplistPath) or not isfile(deplistPath)):
        getDeptList()

    getContent(main, URL, headers, data)
