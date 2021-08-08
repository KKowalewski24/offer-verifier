# offer-verifier

#### Install Dependencies
In main directory run
```
pip install -r requirements.txt
```

#### Functional Requirements
* Access to Internet is required
* Works only for brand new items
* Works only for offers with `BUY_NOW` type
* Works only for offers with US Dollars as currency

#### How to use
* Run `python main.py -h` in order to get information about parameters
* Run `python main.py -p "OFFER_TITLE" --pdf -s`
* Additional parameter `-so` saves downloaded offers to file in binary format
* Additional parameter `--pdf` generates pdf report
* Additional parameter `-s` generates clustering statistics 

#### Data Analysis
* For KMeans K is always set to 2 because only 2 clusters are needed
* For testing of algorithm downloaded offers can be used in order to save time for downloading
* Field `feedback_score` from Seller is not added to feature vector but it is 
used to for choosing cluster with more credible offers 
