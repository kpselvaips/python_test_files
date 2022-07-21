from ast import Not
from sqlite3 import Time
import requests
from scrapy.selector import Selector
import pdb
import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta
import re
import json
session = requests.Session()

    





def listing_date(response):
    # listing_time = []
    for count,k in enumerate(response.xpath('//div[@class="tiered-results-container"]//div[@role="presentation"]//article')):
        list_time = k.xpath(".//span[@class='styles__Content-sc-1l20hun-1 fXGSYx']/text()").get('')
        list_url = 'https://www.realestate.com.au' + k.xpath(".//div[@class='residential-card__image']/a/@href").get('')
        general = {}
        general['red_listing_number'] = count+1
        general['red_listing_url'] = list_url
        TODAY = datetime.date.today()
        splitted = list_time.split()
        if len(splitted) == 1 and splitted[0].lower() == 'today':
            general['red_listing_date'] =  str(TODAY.isoformat())
        elif len(splitted) == 2 and splitted[1].lower() == 'yesterday':
            date = TODAY - relativedelta(days=1)
            general['red_listing_date'] =  str(date.isoformat())
        elif len(splitted) == 4 and splitted[2].lower() in [ 'hour' , 'hours']:
            date = datetime.datetime.now() - relativedelta(hours=int(splitted[1]))
            general['red_listing_date'] =  str(date.strftime("%Y-%m-%d %H:%M:%S"))
        elif len(splitted) == 4 and splitted[2].lower() in ['days','day','d']:
            date = TODAY - relativedelta(days=int(splitted[1]))
            general['red_listing_date'] =  str(date.isoformat())
        else:
            general['red_listing_date'] = 'None'
        
        payload={}
        headers = {
            'authority': 'www.realestate.com.au',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'reauid=3b4b39170768000088d7ba6247030000af140000; optimizelyEndUserId=oeu1656412085885r0.25656927744862235; split_audience=e; _gcl_au=1.1.523094324.1656412086; s_ecid=MCMID%7C34538290368699095190663284463031741019; mid=262553104037995068; _fbp=fb.2.1656412089881.55098120; VT_LANG=language%3Den-US; QSI_SI_6JrMsWODZbnK3NH_intercept=true; _gid=GA1.3.1372397379.1657534409; s_vi=[CS]v1|31660666512884FC-400015693F523115[CE]; QSI_SI_eUTxcS7Ex4BwMYt_intercept=true; Country=IN; fullstory_audience_split=B; _sp_ses.2fe7=*; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C19187%7CMCMID%7C34538290368699095190663284463031741019%7CMCAAMLH-1658309459%7C12%7CMCAAMB-1658309459%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1657711859s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; ab.storage.deviceId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22dbb8f242-bb18-8759-20d2-fe803fd16d48%22%2C%22c%22%3A1656592730077%2C%22l%22%3A1657704659612%7D; DM_SitId1464=true; DM_SitId1464SecId12708=true; DM_SitIdT1464=true; DM_SitId1464SecIdT12708=true; cto_bundle=zVru019ldWo5aUNmQUlqUDRscnFjVWVYemE4aFRkNXVOVHQxeUVyZiUyRjFobmhvd3pCRVBRSFRZdk5nZ1NVQWg2NVVBeDdYSktyV1Ixd2d2THFKb2dzWk1tY0hWQlRVQmVsSXZha2h3YjhqeEFjWHdzc21IeEolMkI3alhoeVRBYiUyQlJjQ1pVaHVXeHglMkY0TkJ5cE0zaDNLbXprem9DNXVLU3NZZTZNaiUyRlVRQlElMkZBaFlmZEElM0Q; KP2_UIDz-ssn=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; KP2_UIDz=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; pageview_counter.srs=7; _ga_F962Q8PWJ0=GS1.1.1657704659.24.1.1657705527.0; _ga=GA1.1.99835123.1656592696; nol_fpid=xvejeo4dvhwy6zx3vo9fp1s6yhhko1656592696|1656592696236|1657705528202|1657705528230; utag_main=v_id:0181b49e8243001bd42ec3513b4b0506f002806700978$_sn:11$_se:22$_ss:0$_st:1657707329768$vapi_domain:realestate.com.au$dc_visit:11$ses_id:1657704659279%3Bexp-session$_pn:10%3Bexp-session$dc_event:10%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _sp_id.2fe7=8377e8eb-7137-42a3-9794-811ebc909efc.1656592696.11.1657705530.1657629028.dfc3358b-da64-43c4-8817-dd7587ba658c; ab.storage.sessionId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%222b1e60d0-d49b-2eef-4f49-9d615369c991%22%2C%22e%22%3A1657707329822%2C%22c%22%3A1657704659611%2C%22l%22%3A1657705529822%7D; External=%2FAPPNEXUS%3D2438618132344474568%2FCASALE%3DYrrXPg3XrW41SnooYvXrMgAA%25264391%2FOPENX%3D04186b85-c919-4c3f-9caa-391ec5426041%2FPUBMATIC%3D8A02ECF6-DB00-4834-8514-04B91AD9AF5B%2FRUBICON%3DL4Y0X58H-26-C6WL%2FTRIPLELIFT%3D3862754328669873697640%2F_EXP%3D1689241472%2F_exp%3D1689241472; Country=IN; KP2_UIDz=0YcG2PDEQloItcjn2cYsTb8d2O4AMvt0nFv8t2X2B21jmlBeMsU0AraWtnYKor3m66e6kQsoeG660bbs26DaIVaXpa73uTMQsBXpRIQuEgtySRtLOvExBm0KpC4dvjYAANX2b7de9Ag6KfBYoG87mOjRo; KP2_UIDz-ssn=0YcG2PDEQloItcjn2cYsTb8d2O4AMvt0nFv8t2X2B21jmlBeMsU0AraWtnYKor3m66e6kQsoeG660bbs26DaIVaXpa73uTMQsBXpRIQuEgtySRtLOvExBm0KpC4dvjYAANX2b7de9Ag6KfBYoG87mOjRo',
            'referer': 'https://www.realestate.com.au/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
        
        response_2 = Selector(requests.request("GET", list_url, headers=headers, data=payload))
        response_3 = requests.request("GET",list_url,headers=headers,data=payload)
        # with open("text.html","w") as f:
        #     f.write(response_2.text)
        
        general['id'] = response_2.xpath("//*[contains(text(),'Property ID')]/text()[2]").get()
        general['red_url'] = response_2.xpath("//link[@rel='canonical']/@href").get()
        general['red_title'] = response_2.xpath('//span[@aria-label="House property type"]/text()').get()
        # # red_listing_date
        if re.findall(r'ListItem","position":1,"name"\:\"([^>]*?)\"',response_3.text):
            property_status = re.findall(r'ListItem","position":1,"name"\:\"([^>]*?)\"',response_3.text)[0]
            if property_status == 'Sold':
                general['red_sold'] = 'True'
            else:
                general['red_sold'] = 'False'
        if re.findall(r'"latitude"\:([^>]*?)\,',response_3.text):
            general['red_location_latitude'] = re.findall(r'"latitude"\:([^>]*?)\,',response_3.text)[0]
        else:
            general['red_location_latitude'] = None
        if re.findall(r'"longitude"\:([^>]*?)\,',response_3.text):
            general['red_location_longitude'] = re.findall(r'"longitude"\:([^>]*?)\,',response_3.text)[0]
        else:
            general['red_location_longtitude'] = None   
        if response_2.xpath('//script[@type="application/ld+json"]/text()'):
            data = json.loads(response_2.xpath('//script[@type="application/ld+json"]/text()').get())
            addr = data[0].get('address','')
            if addr!="":
                address= data[0].get('address','')    
                general['red_address_street'] = address.get('streetAddress')
                general['red_address_suburb'] = address.get('addressLocality')
                general['red_address_state'] = address.get('addressRegion')
                general['red_address_postcode'] = address.get('postalCode')
        general['red_price'] = response_2.xpath("//span[@class='property-price property-info__price']/text()").get()
        general['red_outdoor_features_garage_spaces'] = response_2.xpath("//div[@class='property-info__header']/div/div/div/div[3]/p/text()").get()
        general['red_general_features_building_size'] = response_2.xpath("//*[contains(text(),'Building size')]/span/text()").get()
        general['red_general_features_bathrooms'] = response_2.xpath("//div[@class='property-info__header']/div/div/div/div[2]/p/text()").get()
        general['red_general_features_property_type'] = response_2.xpath('//span[@aria-label="House property type"]/text()').get()
        general['red_general_features_bedrooms'] = response_2.xpath("//div[@class='property-info__header']/div/div/div/div[1]/p/text()").get()
        general['red_general_features_land_size'] = response_2.xpath("//*[contains(text(),'Land size')]/span/text()").get()
        if re.findall(r'<article class="property-description ">(.*?)<\/article>',response_3.text):
            disc = re.findall(r'<article class="property-description ">(.*?)<\/article>',response_3.text)[0]
            general['red_discription'] = re.sub('<[^>]*','',disc).replace('\t','')
        if re.findall(r'ListItem","position":1,"name"\:\"([^>]*?)\"',response_3.text):
            general['red_listing_source'] = re.findall(r'ListItem","position":1,"name"\:\"([^>]*?)\"',response_3.text)[0]
        if re.findall(r'"name"\:\"([^>]*?)\"\,\"branding\"',response_3.text):
            general['red_agency_name'] = re.findall(r'"name"\:\"([^>]*?)\"\,\"branding\"',response_3.text)[0].replace('\\u002F','')
        if re.findall(r'floorplans.0":{"templatedUrl"\:\"([^>]*?)\"',response_3.text):
            general['red_floorplan'] = re.findall(r'floorplans.0":{"templatedUrl"\:\"([^>]*?)\"',response_3.text)[0].replace('u002F','').replace('\\','/').replace('{size}','1080x720-resize,r=33,g=40,b=46')
        time = datetime.datetime.now()
        general['red_scrape_date'] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open('sample.json',"a") as f:
            json.dump(general,f)    

    if response.xpath('//a[@title="Go to Next Page"]'):
        for j in response.xpath('//a[@title="Go to Next Page"]'):
            next_page_url = 'https://www.realestate.com.au' + j.xpath('./@href').get('')
            payload={}
            headers = {
            'authority': 'www.realestate.com.au',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'reauid=3b4b39170768000088d7ba6247030000af140000; optimizelyEndUserId=oeu1656412085885r0.25656927744862235; split_audience=e; _gcl_au=1.1.523094324.1656412086; s_ecid=MCMID%7C34538290368699095190663284463031741019; mid=262553104037995068; _fbp=fb.2.1656412089881.55098120; VT_LANG=language%3Den-US; QSI_SI_6JrMsWODZbnK3NH_intercept=true; _gid=GA1.3.1372397379.1657534409; s_vi=[CS]v1|31660666512884FC-400015693F523115[CE]; QSI_SI_eUTxcS7Ex4BwMYt_intercept=true; Country=IN; fullstory_audience_split=B; _sp_ses.2fe7=*; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C19187%7CMCMID%7C34538290368699095190663284463031741019%7CMCAAMLH-1658309459%7C12%7CMCAAMB-1658309459%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1657711859s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; ab.storage.deviceId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22dbb8f242-bb18-8759-20d2-fe803fd16d48%22%2C%22c%22%3A1656592730077%2C%22l%22%3A1657704659612%7D; DM_SitId1464=true; DM_SitId1464SecId12708=true; DM_SitIdT1464=true; DM_SitId1464SecIdT12708=true; cto_bundle=zVru019ldWo5aUNmQUlqUDRscnFjVWVYemE4aFRkNXVOVHQxeUVyZiUyRjFobmhvd3pCRVBRSFRZdk5nZ1NVQWg2NVVBeDdYSktyV1Ixd2d2THFKb2dzWk1tY0hWQlRVQmVsSXZha2h3YjhqeEFjWHdzc21IeEolMkI3alhoeVRBYiUyQlJjQ1pVaHVXeHglMkY0TkJ5cE0zaDNLbXprem9DNXVLU3NZZTZNaiUyRlVRQlElMkZBaFlmZEElM0Q; KP2_UIDz-ssn=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; KP2_UIDz=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; pageview_counter.srs=7; _ga_F962Q8PWJ0=GS1.1.1657704659.24.1.1657705527.0; _ga=GA1.1.99835123.1656592696; nol_fpid=xvejeo4dvhwy6zx3vo9fp1s6yhhko1656592696|1656592696236|1657705528202|1657705528230; utag_main=v_id:0181b49e8243001bd42ec3513b4b0506f002806700978$_sn:11$_se:22$_ss:0$_st:1657707329768$vapi_domain:realestate.com.au$dc_visit:11$ses_id:1657704659279%3Bexp-session$_pn:10%3Bexp-session$dc_event:10%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _sp_id.2fe7=8377e8eb-7137-42a3-9794-811ebc909efc.1656592696.11.1657705530.1657629028.dfc3358b-da64-43c4-8817-dd7587ba658c; ab.storage.sessionId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%222b1e60d0-d49b-2eef-4f49-9d615369c991%22%2C%22e%22%3A1657707329822%2C%22c%22%3A1657704659611%2C%22l%22%3A1657705529822%7D; External=%2FAPPNEXUS%3D2438618132344474568%2FCASALE%3DYrrXPg3XrW41SnooYvXrMgAA%25264391%2FOPENX%3D04186b85-c919-4c3f-9caa-391ec5426041%2FPUBMATIC%3D8A02ECF6-DB00-4834-8514-04B91AD9AF5B%2FRUBICON%3DL4Y0X58H-26-C6WL%2FTRIPLELIFT%3D3862754328669873697640%2F_EXP%3D1689241472%2F_exp%3D1689241472; Country=IN; KP2_UIDz=0YcG2PDEQloItcjn2cYsTb8d2O4AMvt0nFv8t2X2B21jmlBeMsU0AraWtnYKor3m66e6kQsoeG660bbs26DaIVaXpa73uTMQsBXpRIQuEgtySRtLOvExBm0KpC4dvjYAANX2b7de9Ag6KfBYoG87mOjRo; KP2_UIDz-ssn=0YcG2PDEQloItcjn2cYsTb8d2O4AMvt0nFv8t2X2B21jmlBeMsU0AraWtnYKor3m66e6kQsoeG660bbs26DaIVaXpa73uTMQsBXpRIQuEgtySRtLOvExBm0KpC4dvjYAANX2b7de9Ag6KfBYoG87mOjRo',
            'referer': 'https://www.realestate.com.au/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
            response_1 = Selector(requests.request("GET",next_page_url,headers=headers,data=payload))
            listing_date(response_1)
def property_url(response):
    for i in response.xpath("//*[contains(text(),'NSW')]"):
        area_url = "https://www.realestate.com.au" + i.xpath("./@href").get('')
        payload={}
        headers = {
  'authority': 'www.realestate.com.au',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'reauid=3b4b39170768000088d7ba6247030000af140000; optimizelyEndUserId=oeu1656412085885r0.25656927744862235; split_audience=e; _gcl_au=1.1.523094324.1656412086; s_ecid=MCMID%7C34538290368699095190663284463031741019; mid=262553104037995068; _fbp=fb.2.1656412089881.55098120; VT_LANG=language%3Den-US; QSI_SI_6JrMsWODZbnK3NH_intercept=true; _gid=GA1.3.1372397379.1657534409; s_vi=[CS]v1|31660666512884FC-400015693F523115[CE]; QSI_SI_eUTxcS7Ex4BwMYt_intercept=true; Country=IN; fullstory_audience_split=B; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; DM_SitId1464SecId12708=true; DM_SitId1464=true; _sp_ses.2fe7=*; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C19189%7CMCMID%7C34538290368699095190663284463031741019%7CMCAAMLH-1658492399%7C12%7CMCAAMB-1658492399%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1657894799s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; ab.storage.deviceId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22dbb8f242-bb18-8759-20d2-fe803fd16d48%22%2C%22c%22%3A1656592730077%2C%22l%22%3A1657887599110%7D; DM_SitIdT1464=true; DM_SitId1464SecIdT12708=true; KP2_UIDz-ssn=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; KP2_UIDz=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; pageview_counter.srs=1; utag_main=v_id:0181b49e8243001bd42ec3513b4b0506f002806700978$_sn:17$_se:8$_ss:0$_st:1657890416443$vapi_domain:realestate.com.au$dc_visit:17$ses_id:1657887597767%3Bexp-session$_pn:4%3Bexp-session$dc_event:4%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _sp_id.2fe7=8377e8eb-7137-42a3-9794-811ebc909efc.1656592696.17.1657888617.1657876834.00a4cb89-f45a-44d5-8071-db83a1db6916; ab.storage.sessionId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22e6cb8fae-9055-530c-3233-148931134126%22%2C%22e%22%3A1657890416856%2C%22c%22%3A1657887599107%2C%22l%22%3A1657888616856%7D; _ga_F962Q8PWJ0=GS1.1.1657887596.31.1.1657888617.0; _ga=GA1.3.99835123.1656592696; nol_fpid=xvejeo4dvhwy6zx3vo9fp1s6yhhko1656592696|1656592696236|1657888617131|1657888617171; cto_bundle=mWHTpF9ldWo5aUNmQUlqUDRscnFjVWVYemF6ZE9qQ2Vrb093S3NzWFRabCUyQk03WiUyQnVINHVva0E1T2pxRE0yN3BldEJqJTJCSTQ4MzFyS3hLZ1R1VUdCRlBvbWg4Zk1wRTRjSHoyeVAlMkYycVdGQ0VIVlV0RjlOVThlVEM1NyUyQk83SzlPSktkVkNJVTNRYVJZWTlxcGFjVVpleFFnckV0ZUNPanRqclZaYzBsdzJKZlFQN0x3JTNE; External=%2FAPPNEXUS%3D2438618132344474568%2FCASALE%3DYrrXPg3XrW41SnooYvXrMgAA%25264391%2FOPENX%3D04186b85-c919-4c3f-9caa-391ec5426041%2FPUBMATIC%3D8A02ECF6-DB00-4834-8514-04B91AD9AF5B%2FRUBICON%3DL4Y0X58H-26-C6WL%2FTRIPLELIFT%3D3862754328669873697640%2F_EXP%3D1689424541%2F_exp%3D1689424554; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fproperty-house-wa-jindalee-139610039~1657876844343%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2F~1657888577663%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2Fin-nsw%2Flist-1~1657888604194%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2F~1657888618936; Country=IN; KP2_UIDz=0Ui5GloaWrAghRi8o6aRhiPxLontSZhI3cLDLWcwyeVKa6vFHgy6xpcmSpXsJCZSvjzYb1gWIqw4fnUzXFLgaDfSGL7ynvnuhxnLeS0ibFpuz7o2LxJ6e0CHFxZv50kQPZxUB4k1yZ3EqB9lQCbLBgJ5M; KP2_UIDz-ssn=0Ui5GloaWrAghRi8o6aRhiPxLontSZhI3cLDLWcwyeVKa6vFHgy6xpcmSpXsJCZSvjzYb1gWIqw4fnUzXFLgaDfSGL7ynvnuhxnLeS0ibFpuz7o2LxJ6e0CHFxZv50kQPZxUB4k1yZ3EqB9lQCbLBgJ5M',
  'referer': 'https://www.realestate.com.au/buy/',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        response_1 = Selector(requests.request("GET",area_url,headers = headers,data = payload))

        listing_date(response_1)
def main_url():
    main_url = 'https://www.realestate.com.au/buy/'

    payload={}
    headers = {
  'authority': 'www.realestate.com.au',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'max-age=0',
  'cookie': 'reauid=3b4b39170768000088d7ba6247030000af140000; optimizelyEndUserId=oeu1656412085885r0.25656927744862235; split_audience=e; _gcl_au=1.1.523094324.1656412086; s_ecid=MCMID%7C34538290368699095190663284463031741019; mid=262553104037995068; _fbp=fb.2.1656412089881.55098120; VT_LANG=language%3Den-US; QSI_SI_6JrMsWODZbnK3NH_intercept=true; _gid=GA1.3.1372397379.1657534409; s_vi=[CS]v1|31660666512884FC-400015693F523115[CE]; QSI_SI_eUTxcS7Ex4BwMYt_intercept=true; Country=IN; fullstory_audience_split=B; AMCVS_341225BE55BBF7E17F000101%40AdobeOrg=1; DM_SitId1464=true; DM_SitId1464SecId12708=true; _sp_ses.2fe7=*; AMCV_341225BE55BBF7E17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C19189%7CMCMID%7C34538290368699095190663284463031741019%7CMCAAMLH-1658492399%7C12%7CMCAAMB-1658492399%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1657894799s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; ab.storage.deviceId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22dbb8f242-bb18-8759-20d2-fe803fd16d48%22%2C%22c%22%3A1656592730077%2C%22l%22%3A1657887599110%7D; DM_SitIdT1464=true; DM_SitId1464SecIdT12708=true; _gat_gtag_UA_143679184_2=1; KP2_UIDz-ssn=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; KP2_UIDz=03yKubgRNAKVVoP8qal3I81wF4Xk209rpsXE5sT5DrXAFAHEenHOEEiLotR4J7yGifxycxaG0gHqF4tposIBXc6fhTY7EZl2k09oBQYcQLQExCtNVA7WypabGbdWEyXLL3Tq7PS63vwHRKhoFdcUgiPe4On; pageview_counter.srs=1; _ga_F962Q8PWJ0=GS1.1.1657887596.31.1.1657888602.0; _ga=GA1.1.99835123.1656592696; nol_fpid=xvejeo4dvhwy6zx3vo9fp1s6yhhko1656592696|1656592696236|1657888602618|1657888602690; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fproperty-house-wa-jindalee-139610039~1657876844343%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2F~1657888577663%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2Fin-nsw%2Flist-1~1657888604194; cto_bundle=HaTBvV9ldWo5aUNmQUlqUDRscnFjVWVYemF5NURKY3dQJTJGcXlKYzBOcE5US285THclMkZIMmZnQThCMFBPMFc1WTlieTc4eEpsazlLOHFCQzN1bGhWRXMlMkJuZ1FoRk9zY2Q4SE1LUDVVTzdjU1VGSzdCOSUyRmNPSHRTJTJCNzRRcTVnc1k3RVVDdEF6UUloUTNBRjJIbUVVb1JVTGhnRGR2d2dYTTFKMmdCVCUyRnRpRGl5ZldHZTQlM0Q; utag_main=v_id:0181b49e8243001bd42ec3513b4b0506f002806700978$_sn:17$_se:7$_ss:0$_st:1657890404303$vapi_domain:realestate.com.au$dc_visit:17$ses_id:1657887597767%3Bexp-session$_pn:3%3Bexp-session$dc_event:3%3Bexp-session$dc_region:ap-southeast-2%3Bexp-session; _sp_id.2fe7=8377e8eb-7137-42a3-9794-811ebc909efc.1656592696.17.1657888604.1657876834.00a4cb89-f45a-44d5-8071-db83a1db6916; ab.storage.sessionId.746d0d98-0c96-45e9-82e3-9dfa6ee28794=%7B%22g%22%3A%22e6cb8fae-9055-530c-3233-148931134126%22%2C%22e%22%3A1657890404364%2C%22c%22%3A1657887599107%2C%22l%22%3A1657888604364%7D; External=%2FAPPNEXUS%3D2438618132344474568%2FCASALE%3DYrrXPg3XrW41SnooYvXrMgAA%25264391%2FOPENX%3D04186b85-c919-4c3f-9caa-391ec5426041%2FPUBMATIC%3D8A02ECF6-DB00-4834-8514-04B91AD9AF5B%2FRUBICON%3DL4Y0X58H-26-C6WL%2FTRIPLELIFT%3D3862754328669873697640%2F_EXP%3D1689424541%2F_exp%3D1689424541; Country=IN; KP2_UIDz=0Ui5GloaWrAghRi8o6aRhiPxLontSZhI3cLDLWcwyeVKa6vFHgy6xpcmSpXsJCZSvjzYb1gWIqw4fnUzXFLgaDfSGL7ynvnuhxnLeS0ibFpuz7o2LxJ6e0CHFxZv50kQPZxUB4k1yZ3EqB9lQCbLBgJ5M; KP2_UIDz-ssn=0Ui5GloaWrAghRi8o6aRhiPxLontSZhI3cLDLWcwyeVKa6vFHgy6xpcmSpXsJCZSvjzYb1gWIqw4fnUzXFLgaDfSGL7ynvnuhxnLeS0ibFpuz7o2LxJ6e0CHFxZv50kQPZxUB4k1yZ3EqB9lQCbLBgJ5M',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = Selector(requests.request("GET",main_url,headers=headers,data=payload))
    property_url(response)



main_url()
