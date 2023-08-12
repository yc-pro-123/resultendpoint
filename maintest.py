import requests , json , time
from bs4 import BeautifulSoup as be
from timeit import default_timer as timer
import aiohttp ,requests
import asyncio
from flask import Flask, request,Response
import studsem
from studsem import xo
app = Flask('__name__')

api ="http://results.jntuh.ac.in/resultAction"

rno="20UJ1A0449"
# normal result fetch
async def reg(session,code,rno):	
	param={"degree":"btech","examCode":code,"etype":"r17","result":"null","grad":"null","type":"intgrade","htno":rno
	}
	async with session.get(api,params=param,timeout=8) as resp:
            print(resp.status)
            res_status = resp.status
            re= await resp.text()
	return re , res_status
#rcrv result fetch
async def rcrv(session,code,rno):
	param={"degree":"btech","examCode":code,"etype":"r17","result":"gradercrv","grad":"null","type":"rcrvintgrade","htno":rno
	}
	async with session.get(api,params=param,timeout=8) as resp:
            res_status=resp.status
            re= await resp.text()
	return re ,res_status

async def info(code,rno):
    async with aiohttp.ClientSession(timeout=9) as session:
        param={"degree":"btech","examCode":code,"etype":"r17","result":"null","grad":"null","type":"intgrade","htno":rno}
        #re=requests.get(url=api,params=param)
        print(".........")
        
        re=await asyncio.gather(reg(session,code,rno),return_exceptions=True)
        #print(re[0])
        #async with session.get(api,params=param,timeout=4) as resp:
#            print(".........")
#            res_status=resp.status
#            re= await resp.text()
        #print(re[0][0])
        beu = be(re[0][0],"html.parser")
        #print(beu.find_all('table'))
        t=beu.find_all('table')[0].find_all('td')
        #print(t)
        details={"HTNO":t[1].text ,"NAME":t[3].text,"FATHER NAME":t[5].text,"COLLEGE CODE":t[7].text}
        #print(details)
    return details


#data processing
async def dataprocess(data):	
	b={}
	fail,fass=0,0
	beu = be(data,"html.parser")
	#print(beu.find_all('table'))
	
	t=beu.find_all('table')[1].find_all('tr')
	l=len(t)
	print(" length of data obtained " ,l)
	#---------sem i.e "3-1":{ "code":{},"code":{}.....}
	for i in range(1,len(t),1):
		sub_tab=t[i].find_all('td')
		#print(sub_tab)
		c={}
		c["subject_code"]=sub_tab[0].text
		c["subject_name"]=sub_tab[1].text
		c["internal_marks"]=sub_tab[2].text
		c["external_marks"]=sub_tab[3].text
		c["total_marks"]=sub_tab[4].text
		c["grade_earned"]=sub_tab[5].text
		c["subject_credits"]=sub_tab[6].text
		b[sub_tab[0].text]=c
		#print(c)
		if c["grade_earned"] == "F" or c["grade_earned"] == "Ab":
			fail=fail+1
		else:
		    ++fass
		#print(c)	
	return b,fail,fass
#To find whether the  is Valid 
# returns True for Invalid htno respose
async def invalid_htno(data):
	beu = be(data,"html.parser")
	try:
		#print(beu.find_all("td"))
		t=beu.find_all("td")[2].text
		#print("B6 Invalid ",t)	
		if t=="invalid hallticket number":		
			return True
		else:
			return False
	except:
		return False




async def fetch(session,key):
	data,f_status=None,None
	print("fetch started....",end="")
	#print(ssem)		
	#exmcode=sem_codes[sse]	
	#key = exmcode["reg"]
	#print(ssem,key)	
	res,res_status=await reg(session,key,rno)
	
	if(res_status==200):
		tda=await invalid_htno(res)
		print("Invalid HTNO status :",tda,end="")
		if tda != True:	
			print("Data Processing...",end="")		
			data,f_status,p=await dataprocess(res)
	print(f"Failed In :{f_status} Subjects")	
	if(f_status!=0):
	    res1,res_status1=await rcrv(session,key,rno)
	    if(res_status1 == 200):
	        print("RCRV entered .......")
	        tda1=await invalid_htno(res1)
	        if tda1!= True:
	            print("Applied 4 RCRV ")
	            data1,f_status1,p_status= await dataprocess(res1)
	            data.update(data1)
	            f_status=f_status-p_status	            
	return [data,f_status]

async def main1(ap):
    async with aiohttp.ClientSession(timeout=600) as session:
        
        #ap=sem_codes[ssem[0]]["supply"]
        #ap=["1467","1503","1560","1605","1645"]
        #ap=["1605","1645"]
        print(ap)
        if len(ap)==0:
            return ""
        results = []
        heyy=[]
        
        #async with asyncio.TaskGroup() as t:
        for i in ap:
        	print(i)
        	heyy.append(fetch(session,i))
        	#results.append(t.create_task(fetch(session,i)))
        #print(results[0].result())
        e=await asyncio.gather(*heyy,return_exceptions=True)
        #print(e)
        return e
        #while not queue.empty():
#        	results.append(await queue.get())
#        print(results)

def index(rno):
    ssem,sem_codes=xo(rno)
    print("Proxess Started....",end="")
    print(ssem)
    print(sem_codes)
    r=[]
    for each in ssem:
        if len(sem_codes[each]["reg"])!=0:
            r.append(sem_codes[each]["reg"][0])
    print(r)
    print("vcgg")
    print(r[0],rno)
    details=asyncio.run(info(r[0],rno))
    print("ooooooooo")
    e=asyncio.run(main1(r))
    print(len(e))
    for i in range(len(e)):
        if(e[i][1]!=0):
            keys=sem_codes[ssem[i]]["supply"]
            if len(keys)==0:
                continue
            print("Supply Codes",ssem[i],keys)
            res=asyncio.run(main1(keys))
            print(res,"\n\n")
           
            for up in res:
                if up[0]== None:
                    continue
                    #print(len(res),up)
                e[i][0].update(up[0])
    results=[]
    for i in e:
        yo={ssem[e.index(i)]:i[0]}
        results.append(yo)
    data={}
    data["data"]={"details":details,"results":results}
    #print(data)
    return json.dumps(data)


@app.route('/rno=<rno>',methods=["POST","GET"])    
def main(rno):
    try:
        return index(rno)
    except:
        "<h1>Try Again Later !!</h1>"
if __name__ == "__main__":
    #main(rno)  
    app.run()  