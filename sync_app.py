import requests , json , time ,concurrent.futures,time

from bs4 import BeautifulSoup as be
from timeit import default_timer as timer
from flask import Flask, request,Response
app = Flask('__name__')

_20_codes={
"1-1":{"reg":["1467"],"supply":["1504" ,"1572" ,"1615" ,"1658"] },
"1-2":{"reg":["1503"],"supply":["1570","1620","1656"  ]   },
"2-1":{"reg":["1560"],"supply":["1610","1667"]  },
"2-2":{"reg":["1605"],"supply":["1663"]  },
"3-1":{"reg":["1645"],"supply":[  ]  },
"3-2":{"reg":[],"supply":[  ]  },
"4-1":{"reg":[],"supply":[  ]  },
"4-2":{"reg":[],"supply":[  ]  }


}
#code="1645"
#rno="20UJ1A0421"
api ="http://results.jntuh.ac.in/resultAction"
realsem=["1-1","1-2","2-1","2-2","3-1","3-2","4-1","4-2"]
	
# normal result fetch
def reg(code,rno):	
	param={"degree":"btech","examCode":code,"etype":"r17","result":"null","grad":"null","type":"intgrade","htno":rno
	}
	re=requests.post(url=api,data=param)
	return re.content , re.status_code,re.text
#rcrv result fetch
def rcrv(code,rno):
	param={"degree":"btech","examCode":code,"etype":"r17","result":"gradercrv","grad":"null","type":"rcrvintgrade","htno":rno
	}
	re=requests.post(url=api,data=param)
	return re.content , re.status_code,re.text
	
d={}			
a={}
#data processing
def dataprocess(data):	
	b={}
	fail=False
	beu = be(data,"html.parser")
	t=beu.find_all('table')[1].find_all('tr')
	
	for i in range(1,len(t),1):
		sub_tab=t[i].find_all('td')
		#print(sub_tab)
		c={}
		c["subject_code"]=" "
		c["subject_name"]=" "
		c["internal_marks"]=" "
		c["external_marks"]=" "
		c["total_marks"]=" "
		c["grade_earned"]=" "
		c["subject_credits"]=" "
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
			fail=True
		
		#print(c)	
	return b,fail
#To find whether the  is Valid 
# returns True for Invalid htno respose
def invalid_htno(data):
	beu = be(data,"html.parser")
	try:
		t=beu.find_all("td")[2].text
		#print(t)	
		if t=="invalid hallticket number":		
			return True
		else:
			return False
	except:
		return False

    

def main(exmcode,rno):
	m1=time.perf_counter()
	key = exmcode["reg"]
	fstatus=False
	if (len(exmcode["reg"])== 0):
		return 0
#start = timer()
	res,res_status,res_text=reg(key,rno)
#print("The Request Status code :",res_status,"\nData is :",res_text)
	if res_status==200:
		tda=invalid_htno(res)
		#print("Invalid HTNO status :",tda)
		if tda != True:			
			data,fstatus=dataprocess(res)
			
			#print("Processed Data :",data,"\n\nF_Status=",fstatus,"\n\n Time required to process data is : ",t2-t1)	
			#a[ssem[0]]=data
	#		print(a)
	else:
		print("error occured")
	
	
	
	while(fstatus==True):
		print("while enterned")
		invalid_status=True
		
		result,result_status,temp=rcrv(key,rno)
		invalid_status=invalid_htno(result)
		
		if invalid_status ==False :
			print("RCRV added......")
			data1,fstatus=dataprocess(result)
			data.update(data1)
	
	
		if ((len(exmcode["supply"]) != 0 )and (fstatus == True) ):	
			key=exmcode["supply"][0]
			#print("Supply code :",key)
			result,result_status,temp=reg(key,rno)
			exmcode["supply"].pop(0)
			invalid_status=invalid_htno(result)				
			if invalid_status ==False :
				data1,fstatus=dataprocess(result)
				data.update(data1)		
		else:
			print("Exit while loop via Break ; i e.Zero status")
			break ;	
	m3=time.perf_counter()
	print("The over all Time :" ,m3-m1)
	return data

	#a[ssem[i]]=data
	#d.update(a)
@app.route('/rno=<rno>',methods=["POST" ,"GET"])   
def index(rno):	
	if request.method == 'GET':
		print(request)
		#rno=request.args.get('rno',default = "20UJ1A0449",type= str)
		print(rno)
		#mem rexognition
		if rno[4:6]=="1A":
			mem = "REG"
			sem_codes=eval("_%s_codes"%rno[:2])
		elif rno[4:6]=="5A":
			mem = "LE"
			sem_codes=eval("_%s_codes"%str(int(rno[:2])-1))
		else:
			mem=None
			
		#sem assigning
		if mem == "REG":
			ssem=realsem
		elif mem =="LE":
			realsem.pop(0)
			realsem.pop(0)
			ssem=realsem
		else:
			pass	
		
		for i in range(len(ssem)): 	
			if len(sem_codes[ssem[i]]["reg"]) == 0:
				break ;
			c=i+1		
		t1 = time.perf_counter()
		print("Timer started....")
		with concurrent.futures.ThreadPoolExecutor(12) as exe:
		    e={ssem[i] : exe.submit(main,sem_codes[ssem[i]],rno).result() for i in range(c)}	
		t2 = time.perf_counter()
		print(f"Time Taken To Process this : {t2-t1}")
		return e
	else:
		return '<h1>Hii JNTUH RESULTS</h1>'
if __name__ =='__main__':
    app.run(debug=True)
#print("Final Data :",e)
	
	
	
