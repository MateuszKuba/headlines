import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib2
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }
DEFAULTS = {'publication':'bbc',
            'city':'London,UK',
            'currency_from':'GBP',
            'currency_to':'USD'
            }

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a2a311288049ff4c7cdc2215f4ce61c6"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=019a20814ecf4d9b9005800080232c50"

def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate


def get_weather(query):
    
    query = urllib.quote(query)  #making query readable for www ( for ex. translate spaces)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read() #reading www
    parsed = json.loads(data) #python dictionary
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   'country': parsed['sys']['country']
         }
    return weather


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed["entries"]
    
@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    
    
    ######
    
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from,currency_to)
    return render_template("home.html",articles=articles,weather=weather,
                           currency_from=currency_from,currency_to=currency_to,rate = rate)

if __name__ == '__main__':
  app.run(port=5002, debug=True)
  
  