'''For modifying i should maintain a pickle file with the dictionary and my content management system can then control the dynamic adding and deleting'''

def services_content():
	SERV_DICT = {"Bhukkad":["/services/Bhukkad", "Bhukkad", 8.9],"EatonGo":["/services/EatonGo","eatongo", 4.3],"Swiggy":["/services/Swiggy","swiggy",-1.4]}
	return SERV_DICT
				
def mall_content():
	MALL_DICT = {"The InOrbit":["/services/The InOrbit","Inorbit",9.0],"The Infinity":["/services/The Infinity","infinity",-1.2],"The GBR":["/services/The GBR","GBR",0.2]}
	return MALL_DICT
