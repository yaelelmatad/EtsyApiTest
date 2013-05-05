from etsy import Etsy, EtsyEnvProduction
import json
import sys
import time

def main(jsonListingInfo, jsonListingOutput):
    '''simple script to find storeData given a set of stores in the listing data from the etsy API, outputs shop data in json format'''
    api = Etsy('6hy9gw6rl7wbi4yklg3ezfx6', etsy_env=EtsyEnvProduction())

    listingFile = open(jsonListingInfo,'r')
    theStores = json.load(listingFile)
    listingFile.close()

    storeData = {}
    i=0

    for store in theStores:
        if i%50 == 0: #to watch progress of api calls
            print store, i
        storeData[store]=api.getShop(shop_id=store)
        time.sleep(0.5)#don't make etsy annnngrrry!!
        i+=1

    jsonFile = open(jsonListingOutput,'wb')
    json.dump(storeData,jsonFile, indent=4)
    jsonFile.close()


def usage():
    sys.stderr.write("""
    given store data, find the shop info that corresponds to that store. store the output in a json file.  Usage: \n
    python getShopsShopInfo.py shopListingData.json shopData.json
    \n""")

if __name__ == "__main__": 
  if len(sys.argv) != 3:
    usage()
    sys.exit(1)

  main(sys.argv[1],sys.argv[2])


