from etsy import Etsy, EtsyEnvProduction, EtsyEnvSandbox
import json
import sys
import time

def main(goalNumShops, jsonListingOutput):
    '''simple script to find goalNumShops number of shops from the etsy API, outputs shop listing data in json format'''
    api = Etsy('6hy9gw6rl7wbi4yklg3ezfx6', etsy_env=EtsyEnvProduction())
    myNumShops = 0

    myShops = [] #list of shops
    currOffset = 0
    arbitraryOffset = 50 #for changing offset later
    currShopNames = {}
    while len(myShops) < goalNumShops:
        print currOffset, len(myShops)
        getMoreStores = api.findAllShops(limit=100, offset=(currOffset)) #this api call maxes out at 100.
        for shop in getMoreStores:
            if shop['shop_name']:
                myShops.append(shop)
                currShopNames[shop['shop_name']]=shop['shop_id']
            if len(myShops) >= goalNumShops:
                break
        currOffset += arbitraryOffset #get a different offset from top
        
        time.sleep(1) #avoid making too many API calls too fast.

    currStoreListings = {}
    i = 0
    
    for shop in myShops:
        print shop['shop_name'],i
        currStoreListings[shop['shop_name']] = api.findAllShopListingsActive(shop_id=shop['shop_id'])
        time.sleep(0.25)#so as to not making too many calls at once to API (gets angry when > 5 / second?)
        i+=1
    
    jsonFile = open(jsonListingOutput,'wb')
    json.dump(currStoreListings,jsonFile, indent=4)
    jsonFile.close()


def usage():
    sys.stderr.write("""
    given an integer number of stores to retrieve writes to the second argument (json file)  \n""")

if __name__ == "__main__": 
  if len(sys.argv) != 3:
    usage()
    sys.exit(1)

  main(int(sys.argv[1]),sys.argv[2])


