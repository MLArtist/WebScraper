#### Introduction
This is a python based website crawling script equipped with following capabilities to trick the website robot and avoid getting blocked. 
* Randon time intervals
* User-Agent switching
* IP rotation through proxy server

#### Installation
Although, the script has been tested on Python3.6 but it should work with future versions of Python too. 

Install the libraries provided in requirements.txt by using following command 
*python -m pip install -r requirements.txt*

#### Running the script
run the script by using following command
*python websitescrap.py https://www.wikipedia.org*

**if you wish to start the crawling afresh from the supplied address, please use following command**
*python websitescrap.py https://www.wikipedia.org --start_afresh true*
