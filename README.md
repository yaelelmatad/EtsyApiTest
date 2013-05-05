EtsyApiTest
===========

Project which uses API to grab a bunch of etsy stores and then uses a simple analysis to compare similarity and group similar stores.

There are several codes in this directory.  The first one is getShops.py.  This one should be run as:

```bash
$ python getShops.py 5000 shopListingData.json
```
The second code trains the vector scaler (multiplier) by going through the data.  The training features are defined in the multiplier itself and are currently set to:
```python
typesOfVectors = ["tags", "category_path", "materials"]
```
To use that code you must give it the listing data output by previous python script as well as two output files for the feature scaler (multiplier) as well as feature vectors for all stores (so we don't have to calculate this twice!):
```bash
$ python trainShops.py shopListingData.json multipliers.json vectors.json
```
The final code takes the multipliers and vectors as input and either selects a random store and outputs five similar stores or, given a store name (that is in the data set), finds 5 similar stores to it. Usage (randomStore):
```bash
$ python findSimilarShops.py multipliers.json vectors.json
```
Or (with known store name):
```bash
$ python findSimilarShops.py multipliers.json vectors.json VintageIngenue
```
In either case Output appears in standard out as (or can be > to a file):
```bash
$ OriginalStore: SimilarStore1, SimilarStore2, SimilarStore3, SimilarStore4, SimilarStore5
```
Another version of this code loops over all the stores and produces an output file with all the shops.  To run it use:
```bash
$ python findSimilarShopsAllShops.py multiplier.json vectors.json similarShops.dat
```
I have included my ```shopListingData.json, multipliers.json, vectors.json, ``` and ```similarShops.dat``` in this repository.  

I have further included another script which calls the API to get store specific data about the stores in the shopListingData.json file.  That routine calls the API and gets the shop info.  It outputs the store data to a file called shopData.json.  It can be called as follows:
```bash
$ python getShopsShopInfo.py shopListingData.json shopData.json
```
I have also written another routine which reduces the apparent vector distance between two shops if the comparison ship is more popular (has more favorers).  The maximum bonus is about 10% of the vector distance with most shops getting almost no bonus at all.  To run that script use:
```bash
$ python findSimilarShopsALlShopsByPopularity.py multipliers.json vectors.json storeData.json similarShopsByPopularity.dat
```

I have further included ```storeData.json, ``` and ```similarShopsByPopularity.dat``` with this repository.

