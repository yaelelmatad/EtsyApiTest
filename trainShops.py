from __future__ import division
import json
import sys
import math

class featureVectorTrain:
    def __init__(self, featureVectorName):
        self.counts= {}
        #this will just be a placeholder to count the TOTAL number of times we come across any particular binary feature
        self.multiplier= {}
        #this will then hold 1/count
        self.shopVectors={}
        #spare feature vectors that only include features which appear in this particular shop
        #eventually get normalized so that |shopVector| = 1
        self.featureVectorProperty = featureVectorName

    def addToCounts(self, shop_name, trainingList):
        '''routine to add new data to training corpus'''
        #given a list of features, add it to the dictionaries
        self.shopVectors.setdefault(shop_name,{})
        for item in trainingList:
            self.counts.setdefault(item,0) #if not in dict, add it
            self.counts[item]+=1 #increment it either way
            self.shopVectors[shop_name].setdefault(item,0)
            self.shopVectors[shop_name][item]+=1
        return

    def normalizer(self):
        '''routine that normalizes the feature vector multiplier by taking the value in counts and inverting it, also normalizes the shopVectors by making sure they are of length 1'''
        #call this when done training
        #normalize by frequency of observed feature
        for item in self.counts:
            self.multiplier[item]=float(1)/float(self.counts[item])

        for shop in self.shopVectors:
            length = 0
            for item in self.shopVectors[shop]:
                length += math.pow(self.shopVectors[shop][item],2)

            for item in self.shopVectors[shop]:
                self.shopVectors[shop][item]= float(self.shopVectors[shop][item])/float(length)
            
       
       
    def getMultiplier(self):
        '''return the multiplier after training, make sure to train and normalize before calling this function'''
        return self.multiplier
    
    def getShopVectors(self):
        '''return the shopvectors.  make sure to train and normalize before calling this routine'''
        return self.shopVectors

def main(jsonListingData, jsonOutpuForMultiplier, jsonOutputFileForVectors):
    listingDataFile = open(jsonListingData, "r")
    listingData = json.load(listingDataFile)
    listingDataFile.close()
    typesOfVectors = []
    #features that I've decided to train on.
    #if title or description desired must do some spliting/tokenization/cleaning up of text
    typesOfVectors = ["tags", "category_path", "materials"]
    vectorClasses = {}
    #set up the different feature vectors and initialize the dictionaries
    for typeVec in typesOfVectors:
        vectorClasses[typeVec] = featureVectorTrain(typeVec)
    
    #go through the shop data and start training.
    for shop in listingData:
        for listing in listingData[shop]:
            for typeVec in typesOfVectors:
                if len(listing[typeVec]) > 0:
                    vectorClasses[typeVec].addToCounts(shop, listing[typeVec])
    
    #normalize the vectors appropraitely and then dump them to json
    multipliers = {}
    shopVectors = {}
    for typeVec in typesOfVectors:
        vectorClasses[typeVec].normalizer()
        multipliers[typeVec] = vectorClasses[typeVec].getMultiplier()
        shopVectors[typeVec] = vectorClasses[typeVec].getShopVectors()

    multFile = open(jsonOutpuForMultiplier,'wb')
    json.dump(multipliers,multFile,indent=4)
    multFile.close()

    shopVecFile = open(jsonOutputFileForVectors,'wb')
    json.dump(shopVectors,shopVecFile,indent=4)
    shopVecFile.close()

    #print json.dumps(listingData,indent=4)

def usage():
    sys.stderr.write("""
    given a json files with shopnames and listing details train the multiplier for the feature vector and write that hash to a file (2nd arg), also outputFeatureVectorInfo in third arg (memoization) \n""")

if __name__ == "__main__": 
  if len(sys.argv) != 4:
    usage()
    sys.exit(1)

  main(sys.argv[1],sys.argv[2],sys.argv[3])
