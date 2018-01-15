from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from urlparse import urlparse
import sys
import requests
import time
from login import login
import threading
import os

WAIT=2
TIMEOUT=10

urls = ['localhost:1342', '127.0.0.1:1342']
sessionid = login('admin', 'eevii0et8em7wei9Tahw', 'http://' + urls[0])
print 'sessionid=', sessionid

url = sys.argv[1]

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')            # TODO how to make this shit work with a sandbox

driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)

print 'Setting cookies'
for cookie_url in urls:
  driver.get('http://%s/'%cookie_url)
  driver.add_cookie(dict(name='sessionid', value=sessionid, httponly=True))

def killthread():
  time.sleep(TIMEOUT)
  print 'Killing after timeout'
  os._exit(1)

t = threading.Thread(target=killthread)
t.daemon = True
t.start()

print("Fetching url " + url)
driver.get(url)
print("Waiting a bit")
time.sleep(WAIT)
print("Fetched url " + url)
driver.quit()
exit(0)
