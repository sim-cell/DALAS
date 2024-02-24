# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
url = 'https://www2.hm.com/en_us/women/products/jeans.html'
response=requests.get(url,headers=headers)
soup=BeautifulSoup(response.content,'lxml')
print(len(soup.select('.hm-product-item')))
# for item in soup.select('.hm-product-item'):
# 	try:
# 		print('----------------------------------------')
# 		print(item)
# 	except Exception as e:
# 		#raise e
# 		print('')