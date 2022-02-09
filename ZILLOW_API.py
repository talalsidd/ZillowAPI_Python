import pandas as pd
import math, os, re, datetime, time
from google.colab import files
import requests, json
from openpyxl import load_workbook

cat_urls = ["https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-74.0797901339829%2C%22east%22%3A-73.55259893462062%2C%22south%22%3A40.6412468820408%2C%22north%22%3A40.77917657638982%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22isForSaleByAgent%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleByOwner%22%3A%7B%22value%22%3Afalse%7D%2C%22isNewConstruction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForSaleForeclosure%22%3A%7B%22value%22%3Afalse%7D%2C%22isComingSoon%22%3A%7B%22value%22%3Afalse%7D%2C%22isAuction%22%3A%7B%22value%22%3Afalse%7D%2C%22isForRent%22%3A%7B%22value%22%3Atrue%7D%2C%22isAllHomes%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D&wants={%22cat1%22:[%22listResults%22,%22mapResults%22]}&requestId=4"]
jsondata = ''
buildingkey = []
purls = []
alldata = []
urlids = []
proddata = []

time.sleep(2)
def myPeriodicFunction(): #To extract Count in categories
    header = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    response = requests.get(url=link, headers=header)
    jsondata = response.json()
    data = jsondata['categoryTotals']['cat1']['totalResultCount']
    print(data)
    purls.append(data)

def listPage(): #To extract Zillow IDs (Listing IDs)
    header = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }
    response = requests.get(url=apilink, headers=header)
    cruise_data = response.json()
    for m in cruise_data['cat1']['searchResults']['listResults']:
        if '.' not in m['zpid']:
            zillow_Id = m.get('zpid','N/A')
            alldata.append((zillow_Id))
        else:
            bkey = m.get('lotId','N/A')
            buildingkey.append(bkey)

def bkpage(): #To extract Zillow IDs from LOT IDs
    referer = 'https://www.zillow.com/'
    session = requests.session()
    headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "text/plain",
                "sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "referrer":referer,
                "referrerPolicy": "unsafe-url",
                "credentials": "include",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

    # set headers for all requests
    session.headers.update(headers)
    # --- search ---

    data = '''{"operationName":"BuildingQuery","variables":{"lotId":"'''+str(loID)+'''","cache":false,"update":false},"queryId":"650473038587ed5269d22776ec1dcd01"}'''
    url = "https://www.zillow.com/graphql/"
    page = session.post(url, json=json.loads(data), headers = headers)
    cruise_data = page.json()
    if cruise_data['data']['building']['floorPlans'] is not None:
        for j in cruise_data['data']['building']['floorPlans']:
            zillow_Id = j.get('zpid','N/A')
            alldata.append((zillow_Id))
    else:
        pass

def productPage(): #To extract all attributes from product API page
    try:

        # -- create session ---
        referer = "https://www.zillow.com/"+id+"_zpid/"
        session = requests.session()

        headers = {
                    "accept": "*/*",
					"accept-language": "en-US,en;q=0.9",
					"content-type": "text/plain",
					"sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
					"sec-ch-ua-mobile": "?0",
					"sec-ch-ua-platform": "\"Windows\"",
					"sec-fetch-dest": "empty",
					"sec-fetch-mode": "cors",
					"sec-fetch-site": "same-origin",
                    "referrer":referer,
                    "referrerPolicy": "unsafe-url",
                    "credentials": "include",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
        }

        # set headers for all requests
        session.headers.update(headers)
        # --- search ---

        data = """{
                "operationName": "ForSaleShopperPlatformFullRenderQuery",
                "variables": {
                    "zpid": """+id+""",
                    "contactFormRenderParameter": {
                    "zpid": """+id+""",
                    "platform": "desktop",
                    "isDoubleScroll": true
                    }
                },
                "clientVersion": "home-details/6.0.11.6845.master.07fea64",
                "queryId": "7a1cd3977445cb36e076a9debdb35c6e"
                }"""
        url = "https://www.zillow.com/graphql/?zpid="+id+"&contactFormRenderParameter=&queryId=7a1cd3977445cb36e076a9debdb35c6e&operationName=ForSaleShopperPlatformFullRenderQuery"
        page = session.post(url, json=json.loads(data), headers = headers)
        cruise_data = page.json()
        prod_data = cruise_data['data']['property']
        ZIILOWID = prod_data['zpid']
        PROPERTY_URL = "https://www.zillow.com" + prod_data.get('hdpUrl','N/A')
        LIVING_AREA = prod_data.get('livingArea','N/A')
        BEDROOMS = prod_data.get('bedrooms','N/A')
        BATHROOMS = prod_data.get('bathrooms','N/A')
        FACTS = prod_data['resoFacts']
        FLOORS = FACTS.get('stories','N/A')
        YEARBUILT = prod_data.get('yearBuilt','N/A')
        CONDITION =  prod_data.get('yearBuilt','N/A')
        ZIPCODE =  prod_data.get('zipcode','N/A')
        CITY =  prod_data.get('city','N/A')
        STATE =  prod_data.get('state','N/A')
        STRADDRESS =  prod_data['address']['streetAddress']
        ADDRESS = STRADDRESS +", "+CITY+", "+STATE+" "+ZIPCODE
        try:
            VIEW =  FACTS['view'][0]
        except:
            VIEW = '--'
        LOCATION1 =  prod_data['neighborhoodRegion']
        if LOCATION1 is not None:
            LOCATION = LOCATION1.get('name','N/A')
        else:
            LOCATION = '--'
        MONTHLY_HOUSING_PRICE = prod_data.get('price','N/A')
        RENT =  prod_data.get('price','N/A')
        PROPERTY_TYPE = prod_data.get('homeType','N/A')
        CONS_MAT = FACTS['constructionMaterials']
        CONSTRUCTION =', '.join(CONS_MAT)
        TAXHIST = prod_data['taxHistory']
        TIME = dict()
        TAX_PAID = dict()
        TVALUE = dict()
        j=1
        if TAXHIST is not None:
            TAXHLEN = len(prod_data['taxHistory'])
            if TAXHLEN>0:
                for datahis in TAXHIST:
                    TAX_PAID[j] = datahis['taxPaid']
                    TVALUE[j] = datahis['value']
                    TAX_TIME = datahis['time']
                    s = TAX_TIME / 1000.0
                    TIME[j] = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d')
                    proddata.append((ZIILOWID,PROPERTY_URL,LIVING_AREA,BEDROOMS,BATHROOMS,FLOORS,YEARBUILT,CONDITION,CITY,STATE,ZIPCODE,STRADDRESS,ADDRESS,VIEW,LOCATION,MONTHLY_HOUSING_PRICE,RENT,PROPERTY_TYPE,CONSTRUCTION,TIME[j],TAX_PAID[j],TVALUE[j]))
                    j=j+1
            else:
                TAX_PAID = '--'
                TVALUE = '--'
                TIME = '--'
                proddata.append((ZIILOWID,PROPERTY_URL,LIVING_AREA,BEDROOMS,BATHROOMS,FLOORS,YEARBUILT,CONDITION,CITY,STATE,ZIPCODE,STRADDRESS,ADDRESS,VIEW,LOCATION,MONTHLY_HOUSING_PRICE,RENT,PROPERTY_TYPE,CONSTRUCTION,TIME,TAX_PAID,TVALUE))
        else:
          TAX_PAID = '--'
          TVALUE = '--'
          TIME = '--'
          proddata.append((ZIILOWID,PROPERTY_URL,LIVING_AREA,BEDROOMS,BATHROOMS,FLOORS,YEARBUILT,CONDITION,CITY,STATE,ZIPCODE,STRADDRESS,ADDRESS,VIEW,LOCATION,MONTHLY_HOUSING_PRICE,RENT,PROPERTY_TYPE,CONSTRUCTION,TIME,TAX_PAID,TVALUE))
    except ConnectionError as e:
        print (e)
        page = "No response"    

for link in cat_urls: #Loop to extract count from 1st function
    myPeriodicFunction()
    time.sleep(.8)
print(purls)
time.sleep(2)
i=0
for link2 in cat_urls: #Loop to make pagination URLs
    if(int(purls[i])<1000):
        totalcalls =  math.ceil(purls[i]/40)
        i=i+1
        print(totalcalls)
        k=1
        while(k<=totalcalls):
            parlink = re.sub('.*currentPage%22%3A\d+','',link2)
            parlink2 = re.sub('\d+%7D%2C%22mapBound.*','',link2)
            apilink = parlink2 + str(k) + parlink
            print(k)
            listPage()
            time.sleep(1)
            k=k+1     
    else:
        i=i+1
        continue
time.sleep(2)
if len(buildingkey)>0: #To extracting LOT IDs
    print('Getting Lot ID')
    for loID in buildingkey:
        if loID is not None:
            print(loID)
            bkpage()
            time.sleep(1)
        else:
            pass
else:
    pass
print('Now extracting data from IDs')
for id in alldata: #Extracting from product data page
    print(id)
    if id == "undefined":
        pass
    else:
        productPage()
        time.sleep(1)

#Below is the pandas' part as the data array 'proddata' has been put into a dataframe with column names

df = pd.DataFrame(proddata,columns =["ZILLOW ID","PROPERTY URL","LIVING AREA","BEDROOMS","BATHROOMS","FLOORS","YEAR BUILT","CONDITION","CITY","STATE","ZIPCODE","STREET ADDRESS","ADDRESS","VIEW","LOCATION","MONTHLY HOUSING PRICE","RENT","PROPERTY TYPE","CONSTRUCTION","TAX DATE","TAX PAID","HOUSE VALUE"])
now_time = datetime.datetime.now().strftime("%d-%m-%Y")
#remove duplicate entries
df.drop_duplicates(keep=False, inplace=True)


# if file does not exist write header 
if not os.path.isfile('ZILLOW_DATA_'+now_time+'.csv'):
    df.to_csv('ZILLOW_DATA_'+now_time+'.csv', index=False)

else:                       # else it exists so append without writing the header

    df.to_csv('ZILLOW_DATA_'+now_time+'.csv', mode='a', header=False,index=False)
files.download('ZILLOW_DATA_'+now_time+'.csv')
