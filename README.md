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
* Run `python main.py -p "OFFER_TITLE" --pdf`
* Additional parameter `--pdf` generates pdf report
