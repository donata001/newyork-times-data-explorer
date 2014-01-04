import webapp2
import csv
from urllib2 import urlopen
from json import load


html="""
<!doctype html>
<html>
    <head>
        <title> NY times data fetching web app</title>
    </head>
    <body>
        <h2>NewYork Times data explorer</h2>
        <script type="text/javascript">
            
                    function error_check(){
                    
                    var query=document.getElementsByName('query')[0].value;
                    var input_num=document.getElementsByName('input_num')[0].value   
                    var flag;
                    if (query===""||query.length>100) {
                        alert ("please put a key word with length less than 100!");
                        window.location="http://newyork-times-data-explorer.appspot.com/"
                        flag=false;
                    }
                    else if ((input_num==="")||isNaN(input_num)||parseInt(input_num)<1) {
                        alert("please enter a valid count number!");
                        window.location="http://newyork-times-data-explorer.appspot.com/"
                        flag=false;
                    }
                    else if (parseInt(input_num)>1000) {
                        alert ("please enter a smaller count number!");
                        window.location="http://newyork-times-data-explorer.appspot.com/"
                        flag=false;
                    }
                    else {
                    flag=true;
                    }
                
                return flag;
                }
            </script>
            
        <form method="post", onSubmit="return error_check();">
            <lable for="key word">Key word:</lable>
            <input name="query", type="text"><br>          
            <lable for="count">Count:</lable>
            <input name="input_num", type="text"><br>
            <lable for="begin_date">begin date format(yyyymmdd): </lable>
            <input name="begin_date", type="text"><br>
            <lable for="end_date">end date format(yyyymmdd): </lable>
            <input name="end_date", type="text"><br>
            <p>New York Times API is using keyword search, so please make your key word more specific and time span longer</p>
            <input type="submit", value="submit query"><br>
               
        </form>
    </body>
</html>


"""



class MainPage(webapp2.RequestHandler):
        
    def get(self):
        self.response.write(html)
            
    def post(self):
        query=self.request.get("query")
        input_num=self.request.get("input_num")
        count=int(input_num)
        url="http://api.nytimes.com/svc/search/v2/articlesearch.json?"
        begin_date=self.request.get("begin_date")
        end_date=self.request.get("end_date")
        url+="q="+query+"&begin_date="+begin_date+"&end_date="+end_date
        url+="&page="+str(count/10)
        key="&api-key=0451890265f0725be9486ecc5a132e66:18:68505529"
        url+=key
        response=urlopen(url)
        js=load(response)

        self.response.write("Your key word is: "+query+" with count of "+input_num)       
        self.response.write(" Between:"+ begin_date+"and"+end_date+" the related search results are as follows: "+ "\n")        
        temp=[['time stamp','url','lead paragraph','abstract']]
        
        try:
                        
            for story in js['response']['docs']:
               
                if not story['lead_paragraph']:
                    story['lead_paragraph']=''
                if not story['abstract']:
                    story['abstract']=''
                    
                temp.append([story['pub_date'],story['web_url'],story['lead_paragraph'].encode('utf-8','ignore'), story['abstract'].encode('utf-8','ignore')])
            self.response.headers['Content-Type']='application/csv'
            writer=csv.writer(self.response.out,delimiter='\t')
                
            for i in range(len(temp)):
                writer.writerow(temp[i][0:4])
        except Exception,e:
            self.response.write(str(e))
            
   


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
                 

