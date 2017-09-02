import requests
from bs4 import BeautifulSoup
from sys import argv
import os
import pyprind
#user="Balance_Breaker"
script,user=argv
ur = "http://codeforces.com/submissions/"+user+"/page/1"
source_code = requests.get(ur)
plain_text = source_code.text
soup =BeautifulSoup(plain_text,"lxml")
page=soup.find_all('div',{'class':'pagination'})
page=page[1]
page=page.find_all('span')
pages=page[len(page)-1]
pages=pages.findAll('a')
pagenos=pages[0].text
#section=soup.findAll('table',{'class':'status-frame-datatable'})
#links = section[0].find_all('tr')
num=int(pagenos)
url='http://codeforces.com/submissions/'+user+'/page/%d' %num
code=requests.get(url)
plain_text=code.text
soup=BeautifulSoup(plain_text,"lxml")
section = soup.findAll('table',{'class':"status-frame-datatable"})
links = section[0].find_all('tr')

lastrownos=len(links)

#print(num)
#print(lastrownos)
cnt=(num-1)*50 + lastrownos-1
pbar=pyprind.ProgBar(cnt)
for j in xrange(1,num+1):
	url='http://codeforces.com/submissions/'+user+'/page/%d' %j
	code=requests.get(url)
	plain_text=code.text
	soup=BeautifulSoup(plain_text,"lxml")
	section = soup.findAll('table',{'class':"status-frame-datatable"})
	links = section[0].find_all('tr')


	for i in range(1,len(links)):
		pbar.update()
		row = links[i]
		id = row['data-submission-id']
		data = row.find_all('td')
		verdict=data[5]
		span=verdict.findAll('span',{'class':'verdict-accepted'})
		if(len(span)>0):
			val= data[3].find_all('a')
			lang = data[4]
			lang=lang.text
			lan='cpp'

			if(lang.find('C++')>=0):
				lan='cpp'
			elif(lang.find('Java')>=0):
				lan='java'
			elif(lang.find('C')>=0):
				lan='c'
			else:
				lan='py'
			val = val[0]
			str = val['href']
			str=str.split('/')
			num = str[3]
			prt=str[4]

			url = 'http://codeforces.com/contest/'+num+'/submission/'+id
			code = requests.get(url)
			code=code.text
			soup1=BeautifulSoup(code,"lxml")
			source = soup1.findAll('pre',{'class':'program-source'})
			try:
				source=source[0].text
				#soup2 = BeautifulSoup(source,"lxml")
				#problem_code = soup2.get_text()
			except:
				continue
			problem_code=source	
			name = num+prt+"." + lan

			newpath = './'+user#username
			if not os.path.exists(newpath):
				os.makedirs(newpath)
			
			name=newpath+'/'+name
			f = open(name,'w')	
			f.write(problem_code)
			f.close()
