import tornado.httpclient
from bs4 import BeautifulSoup

req = 'inpPointFr_ajax=%C5s+Gamla+K%F6pstad%7C6014%7C0'
req +='&inpPointTo_ajax=Varberg+Station+%28Bussterm%29%7C6700%7C0'
req +='&inpPointInterm_ajax='
req +='&selRegionFr=741'
req +='&inpPointFr=%C5s+Gamla+K%F6pstad++%5BH%E5llplats%5D'
req +='&optTypeFr=0'
req +='&inpPointTo=Varberg+Station+%28Bussterm%29++%5BH%E5llplats%5D'
req +='&optTypeTo=0'
req +='&inpPointInterm='
req +='&selDirection=0'
req +='&inpTime=12%3A56'
req +='&inpDate=2014-03-14'
req +='&optReturn=0'
req +='&selDirection2=0'
req +='&inpTime2=23%3A34'
req +='&inpDate2=2014-03-11'
req +='&trafficmask=1'
req +='&trafficmask=2'
req +='&trafficmask=4'
req +='&Submit=S%F6k'
req +='&selChangeTime=0'
req +='&selWalkSpeed=0'
req +='&selPriority=0'
req +='&cmdAction=search'
req +='&EU_Spirit=False'
req +='&TNSource=HALLAND'
req +='&SupportsScript=True'
req +='&Language=se'
req +='&VerNo=7.1.1.2.0.38p3'
req +='&Source=querypage_adv'
req +='&MapParams='

httprequest = tornado.httpclient.HTTPRequest('http://193.45.213.123/halland/v2/querypage_adv.aspx', method='POST', headers=None, body=req) 

http_client = tornado.httpclient.HTTPClient()
try:
    response = http_client.fetch(httprequest)
    html_data = response.body
except httpclient.HTTPError as e:
    print "Error:", e
http_client.close()

html_doc = BeautifulSoup(html_data)

scripts = html_doc.find_all('script')

for script in scripts:
	rad = script.string
	try:
		rad = rad.strip()
	except:
		rad = "nodatainstring"
	if rad[:8] == 'dValidFr':
		done = rad

rawprice = done.split('\n')

tripdata = {}

for row in rawprice:
	row = row.strip()
	if row[:9] == 'priceArr[':
		parts = row.split('(')
		rownumb = row.split(']')[0].split('[')[1]
		tripdata[rownumb] = {}
		tripdata[rownumb]['prices'] = parts[1][1:-2].split('\',\'')

for index in tripdata:
	svar = html_doc.find(id="result-"+index)
	data = svar.find_all('td')
	tripdata[index]['times'] = {}
	tripdata[index]['times']['dep'] = data[1].string
	tripdata[index]['times']['arr'] = data[2].string
	tripdata[index]['times']['dur'] = data[3].string
	tripdata[index]['times']['changes'] = data[4].string

print tripdata








