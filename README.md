EtsyApiTest
===========

Project which uses API to grab a bunch of etsy stores and then uses a simple analysis to compare similarity and group similar stores.

There are three main codes in this directory.  The first one is getShops.py.  This one should be run as:

  python getShops.py 5000 shopListingOutput.json

The second code trains the vector scaler (multiplier) by going through the data.  The training features are defined in the multiplier itself and are currently set to:
```python
    typesOfVectors = ["tags", "category_path", "materials"]
```
