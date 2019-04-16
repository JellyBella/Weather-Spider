from bs4 import BeautifulSoup
from urllib import request
import csv
import pymysql

# 爬取网页
with request.urlopen('http://www.weatherzone.com.au/station.jsp?lt=site&lc=87184&list=ob') as response:
   html = response.read()
soup = BeautifulSoup(html, 'html.parser')

# 解析数据
div = soup.find('table', attrs = {'class':'standard-table'})
tr = div.find_all('tr')
#print(tr)
data = []
for i in range(2,len(tr)):
    #print(tr[i-2])
    td = tr[i-2].find_all('td')
    #print(td)
    data.append([])
    for ele in td:
        data[i-2].append(ele.text.strip())

for i in range(0,len(data)):
    for j in range(0,len(data[i])):
        print(data[i][j],end=',')
    print()
print(len(data))
with open('data.csv', 'w+') as myfile:
     wr = csv.writer(myfile, delimiter = ',')
     wr.writerows(data)

if __name__ == "__main__":
    db = pymysql.connect(host="localhost",user="root",password="",db="test",charset="utf8mb4")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS weather")
    createTab = """CREATE TABLE weather(
        time VARCHAR(20) NOT NULL PRIMARY KEY,
        winddir VARCHAR(10),
        windspd VARCHAR(10),
        windgust VARCHAR(10),
        tmp VARCHAR(10),
        dewpt VARCHAR(4),
        feelslike VARCHAR(4),
        rh VARCHAR(10),
        fire VARCHAR(2),
        rain VARCHAR(10),
        rain10 VARCHAR(10),
        pres VARCHAR(10)
    );"""
    cursor.execute(createTab)

    for i in data:
        sql = "INSERT INTO `weather`(`time`,`winddir`,`windspd`,`windgust`,`tmp`,`dewpt`,`feelslike`,`rh`,`fire`,`rain`,`rain10`,`pres`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql, (i[0], i[1], i[2], i[3], i[4], i[5],i[6],i[7],i[8],i[9],i[10],i[11]))
            db.commit()
            print(i[0]+" is success")
        except:
            db.rollback()

    db.close()
