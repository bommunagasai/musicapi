# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import json
app = Flask(__name__)


response = requests.get("http://www.bbc.co.uk/radio1/chart/singles/print")
HTML = response.text
soup = BeautifulSoup(HTML,"html.parser")
table = soup.find("table", attrs={"border":"1"})

# The first tr contains the field names.
#http://www.convertmp3.io/fetch/?format=text&video=https://www.youtube.com/watch?v=i62Zjga8JOM
headings = [th.get_text() for th in table.find("tr").find_all("th")]
headings.append(u'videoId_1')
headings.append(u'videoId_2')
c=0
datasets = []
for row in table.find_all("tr")[1:]:
    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    data = [td.get_text() for td in row.find_all("td")]
    search_query = data[4]+" "+data[5]
    response1 = requests.get("https://www.youtube.com/results?search_query="+search_query)
    HTML1 = response1.text
    soup1 = BeautifulSoup(HTML1,"html.parser")
    lit = []
    i=0
    c=0
    for link in soup1.find_all('a'):
    	lit.append(link.get('href'))
    	
    	if i>20:
    		if lit[i][1] == "w" and c==0:
    			f= lit[i]
    			c=c+1
    		if lit[i][1] == "w" and c==1 and f != lit[i]:
    			g= lit[i]
    			break
    	i=i+1

    data.append(f)
    data.append(g)
    dicti = {}
    for i in range(len(headings)):
    	if headings[i] not in dicti.keys():
    		dicti[headings[i]] = data[i]
    datasets.append(dicti)


@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'Music': datasets})

if __name__ == '__main__':
    app.run(debug=True)
