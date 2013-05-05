EtsyApiTest
===========

Project which uses API to grab a bunch of etsy stores and then uses a simple analysis to compare similarity and group similar stores.

There are three main codes in this directory.  The first one is getShops.py.  This one should be run as:

```bash
$python getShops.py 5000 shopListingData.json
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
In either case Output appears as:
```bash
$ OriginalStore: SimilarStore1 SimilarStore2 SimilarStore3 SimilarStore4 SimilarStore5
```
I have included my ```bash shopListingData.json multipliers.json vectors.json``` in this repository.  
