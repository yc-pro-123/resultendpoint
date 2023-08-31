realsem=["1-1","1-2","2-1","2-2","3-1","3-2","4-1","4-2"]
_20_codes={
"1-1":{"reg":["1467"],"supply":["1504" ,"1572" ,"1615" ,"1658"] },
"1-2":{"reg":["1503"],"supply":["1570","1620","1656"  ]   },
"2-1":{"reg":["1560"],"supply":["1610","1667"]  },
"2-2":{"reg":["1605"],"supply":["1663"]  },
"3-1":{"reg":["1645"],"supply":[ "1686" ]  },
"3-2":{"reg":["1690"],"supply":[  ]  },
"4-1":{"reg":[],"supply":[  ]  },
"4-2":{"reg":[],"supply":[  ]  },
}


def xo(rno):
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
    return ssem,sem_codes
