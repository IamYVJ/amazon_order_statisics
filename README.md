
# Amazon Order Statistics

Know how many orders you have made and how much you have spent on Amazon!

## Variables

- `USE_FIREFOX` 
Default Value: _TRUE_ 
To be changed to _FALSE_ to use Chrome
- `USE_DRIVER_MANAGER` 
Default Value: _TRUE_ 
To be changed to _FALSE_ if required webdriver is defined in _PATH_
- `START_YEAR` 
Default Value: _2014_ 
First year to be scraped
- `END_YEAR` 
Default Value: _2022_ 
Last year to be scraped
## Steps To Run

### Windows Terminal

- `git clone https://github.com/IamYVJ/amazon_order_statisics.git`
- `cd amazon_order_statisics`
- `pip3 install -r requirements.txt`
- `python3 scraper.py`

## Requirements

The script is written in Python 3

Firefox or Chrome should be installed on the system

