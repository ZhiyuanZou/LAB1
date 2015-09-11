__author__ = 'zou'

import json
import sys
import re
import urllib
from bs4 import BeautifulSoup




def getCurrPrice(soup):
  a = soup.find("span", class_ = "time_rtq_ticker")
  return float(a.string)

def getLargeTuple(soup):
  a = soup.find_all("td", class_ = re.compile("yfnc_"))
  tuple_list = []
  count = 0
  json_tuple = dict()
  for i in a:
  #  print i
    if(count%8==0):
      json_tuple = dict()
      json_tuple["Strike"] = i.string
      count = count + 1
    elif(count%8==1):
      json_tuple["Type"] = getType(i.string)
      json_tuple["Symbol"] = getSymbol(i.string)
      json_tuple["Date"] = getDate(i.string,json_tuple)
      count = count + 1
    elif(count%8==2):
      json_tuple["Last"] = i.string
      count = count + 1
    elif(count%8==3):
      json_tuple["Change"] = " "+i.b.string
      count = count + 1
    elif(count%8==4):
      json_tuple["Bid"] = i.string
      count = count + 1
    elif(count%8==5):
      json_tuple["Ask"] = i.string
      count = count + 1
    elif(count%8==6):
      json_tuple["Vol"] = i.string
      count = count + 1
    elif(count%8==7):
      json_tuple["Open"] = i.string
      count = count + 1
      tuple_list.append(json_tuple)
  return sorted(tuple_list,cmp= lambda x,y:compare(x,y),reverse=True)

def getSymbol(symbol):
  leading_non_digit = re.compile('^([A-Za-z])+')
  g = leading_non_digit.search(symbol)
  return g.group()

def getDate(symbol,tuple):
  digit = re.compile('[0-9]+')
  g = digit.search(symbol)
  s = g.group()
  if len(s)==7:
    s = s[1:]
    tuple['Symbol'] = tuple['Symbol']+"7"
  return s


def getType(symbol):
  leading_non_digit = re.compile('^([A-Za-z])+')
  g = leading_non_digit.search(symbol)
  r = re.sub(leading_non_digit,'',symbol)
  non_digit = re.compile('([A-Za-z])+')
  g = non_digit.search(r)
  return g.group()

def getURL(soup):
  href_list = []
  op_href = soup.find_all("a", href = re.compile("(/q/op\?s=).+(m=)"))
  for i in op_href:
    amp_href = re.sub("&","&amp;",i['href'])
    href_list.append("http://finance.yahoo.com" + amp_href)
 #   href_list.append("http://finance.yahoo.com" + i['href'])
  os_href = soup.find_all("a", href = re.compile("/q/os\?s="))
  for i in os_href:
    amp_href = re.sub("&","&amp;",i['href'])
    href_list.append("http://finance.yahoo.com" + amp_href)
  #  href_list.append("http://finance.yahoo.com" + i['href'])
  return href_list

def contractAsJson(filename):
  f=open(filename)
  soup = BeautifulSoup(f, 'html.parser')

  with open('data.txt', 'w') as outfile:
    json.dump({"currPrice":getCurrPrice(soup),"dateUrls":getURL(soup),"optionQuotes":getLargeTuple(soup)},outfile,indent=4,sort_keys=True)
  return json.dumps({"currPrice":getCurrPrice(soup),"dateUrls":getURL(soup),"optionQuotes":getLargeTuple(soup)},indent=4,sort_keys=True)

def compare(item1,item2):
  i1 = int(re.sub(",",'',item1['Open']))
  i2 = int(re.sub(",",'',item2['Open']))
  return i1-i2
