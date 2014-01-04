from urllib2 import urlopen
from json import load
import csv
import codecs

begin_date="20131122"
end_date="20131130"
query="thanksgiving"
input_num="10"
count=int(input_num)

url="http://api.nytimes.com/svc/search/v2/articlesearch.json?"
url+="q="+query+"&begin_date="+begin_date+"&end_date="+end_date
url+="&page="+str(count/10)
key="&api-key=0451890265f0725be9486ecc5a132e66:18:68505529"
url+=key

response=urlopen(url)
js=load(response)
temp=[['time stamp','url','lead paragraph','abstract']]

try:
       
    with codecs.open("result.csv",mode="w") as f:
        writer=csv.writer(f,delimiter='\t') 
        for story in js['response']['docs']:
            if not story['lead_paragraph']:
                story['lead_paragraph']=''
            if not story['abstract']:
                story['abstract']=''
            temp.append([story['pub_date'],story['web_url'],story['lead_paragraph'].encode('utf-8','ignore'), story['abstract'].encode('utf-8','ignore')])       
        for i in range(len(temp)):
            for j in range(4):
                writer.writerow(temp[i][j])                   
       
except Exception,e:
    print str(e)
    
f=open("result.csv","r")
for row in f:
    print row

