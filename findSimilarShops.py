from __future__ import division
import json
import sys
import math
import random

#hard coded number of similar stores to spit out since HW said 5, could always add to command line
nSimilarStores = 5

class vectors:
    def __init__(self, featureVectorName, multiplier, shopVectors):
        self.multiplier= multiplier
        #this will then hold 1/count
        self.shopVectors= shopVectors
        #spare feature vectors that only include features which appear in this particular shop
        #eventually get normalized so that |shopVector| = 1
        self.featureVectorProperty = featureVectorName

    def getMultiplier(self):
        '''return the multiplier after training, make sure to train and normalize before calling this function'''
        return self.multiplier
    
    def getShopVectors(self):
        '''return the shopvectors.  make sure to train and normalize before calling this routine'''
        return self.shopVectors

    def calculateDistance(self, shop1, shop2):
        '''given two shop names, calculate the distance for this typeOfVector only'''
        #check that both of the vectors are in this class, if not use the default empty dictionary
        vec1 = {}
        vec2 = {}
        if shop1 in self.shopVectors:
            vec1 = self.shopVectors[shop1]
        if shop2 in self.shopVectors:
            vec2 = self.shopVectors[shop2]

        #the vectors are sparse, so not all keys appear in all vectors.  Figure out which keys are in just one, and which are in both
        allKeys = vec1.keys() + vec2.keys()
        sharedKeys = []
        justInFirst = []
        justInSecond = []
        for key in set(allKeys):
            if key in vec1.keys() and key in vec2.keys():
                sharedKeys.append(key)
            elif key in vec1.keys():
                justInFirst.append(key)
            else:
                justInSecond.append(key)

    
        dist2 = 0 #actually the squared distance
        #since we used all our store data to train our multiplier, we know that the multiplier contains all keys
        for key in justInFirst:
            dist2 += math.pow(vec1[key],2)*(self.multiplier[key])
            #dist2 += math.pow(vec1[key],2)
        for key in justInSecond:
            dist2 += math.pow(vec2[key],2)*(self.multiplier[key])
            #dist2 += math.pow(vec2[key],2)
        for key in sharedKeys:
            dist2 += math.pow(vec2[key]-vec1[key],2)*(self.multiplier[key])
            #dist2 += math.pow(vec2[key]-vec1[key],2)
        return math.sqrt(dist2)


def main(jsonInputForMultiplier, jsonInputFileForVectors, originalShop = ""):
    
    #read the json input
    multFile = open(jsonInputForMultiplier,'r')
    multipliers =json.load(multFile)
    multFile.close()

    shopVecFile = open(jsonInputFileForVectors,'r')
    shopVectors = json.load(shopVecFile)
    shopVecFile.close()

    #find out how many different things we trained against
    typesOfVectors = [key for key in multipliers]

    #initialize the vectorClasses with the trained data
    vectorClasses = {}
    for typeVec in typesOfVectors:
        vectorClasses[typeVec] = vectors(typeVec, multipliers[typeVec],shopVectors[typeVec])

    #find all the shop names (not necessarily unique)
    shopNamesNotSet = []
    #so we can get all shops, not all shops appear in all feature sets
    for typeVec in typesOfVectors:
        shopNamesNotSet += [shop for shop in shopVectors[typeVec]]
    
    #now remove duplicates
    shopNames = set(shopNamesNotSet)

    #check to see if user provided a shopName to find distances, else select random
    if originalShop == "":
        originalShop= random.sample(shopNames,1)[0]
    elif originalShop not in shopNames:
        print "You specified a shop that is not in the dataset, please check your shopname."
        sys.exit(1)

    distances = []
    for shop in shopNames:
        #go through all the shops and calculate the distance
        if shop == originalShop:
            #don't waste your time calculating self distance
            continue

        dist = 0
        for typeVec in typesOfVectors:
            #there are len(typesOfVectors) different "length" vectors to calculate
            dist+=vectorClasses[typeVec].calculateDistance(originalShop,shop)

        #if shop != originalShop:
        distances.append((shop,dist))
   
        #certainly not necessary to keep all the distances and then sort.  could just keep the list of "nSimilarStores" currently with lowest distane values, but the sort is quick on only 5000 members
    
    sortedDist = sorted(distances, key=lambda t: t[1])
    #sort on second element of tuple
    stringToPrint = originalShop+ ": " + sortedDist[0][0]
    for i in range(1,nSimilarStores):
        stringToPrint += ", " + sortedDist[i][0]

    #print out the string starting with original store then : then nSimilarStores number of similar stores
    print stringToPrint


def usage():
    sys.stderr.write("""
    given a multiplier.json and a shopvectors.json choose and random store and find the five most similar stores. If add name of store, will use that store as the originalStore to find similarStores: \n Example Usage: python findSimilarShops.py multiplier.json vectors.json (ScottAllenPaintings)  \n""")

if __name__ == "__main__":
    #check the usage is correct, user can specif 2 or 3 arguments
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage()
        sys.exit(1)
    elif len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2] )
    else: #len(sys.argv) == 4:
        main(sys.argv[1],sys.argv[2], originalShop = sys.argv[3])
