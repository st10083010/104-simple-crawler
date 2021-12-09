# 104 作業 完成

import requests, json ,csv
from bs4 import BeautifulSoup

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"
headers = {"User-Agent": userAgent}


url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=11&keyword=python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000&order=14&asc=0&page=2&mode=s&jobsource=2018indexpoc&langFlag=0'


res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')



jobUrlList = soup.select('h2[class="b-tit"]')
index = 0
for jobURL in jobUrlList:
    if jobURL.a == None:
        pass
    else:
        index += 1
        jobURL2 = "https:" + jobURL.a['href']
        jobs = jobURL.a.text
        print("編號: ", index )
        print("職缺名稱: ", jobs)
        print("工作連結: " + jobURL2)


        referer = jobURL2.split('/')[-1].split('?')[0]
        referer2 = 'https://www.104.com.tw/job/ajax/content/{}'.format(referer) # 帶著這筆資料對網頁發出請求
        headers2 = {"User-Agent": userAgent, "Referer": referer2}
        workRes = requests.get(url=referer2, headers=headers2)

        jsonData = json.loads(workRes.text)
        comName = jsonData['data']['header']['custName'] # 公司名稱
        workDetails = jsonData['data']['jobDetail']['jobDescription']
        print("公司名稱: " , comName)
        print("工作內容: ", workDetails)

        with open('104.csv', 'a', newline='', encoding="UTF-8") as homeWork104:
            writer = csv.writer(homeWork104)
            writer.writerow(["編號", "職缺名稱", "工作連結", "公司名稱", "工作內容"])
            writer.writerow([str(index), jobs, jobURL2, comName, workDetails])

        print('='*10)

