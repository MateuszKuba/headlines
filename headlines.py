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
            'city':'London,UK'
            }

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a2a311288049ff4c7cdc2215f4ce61c6"
    query = urllib.quote(query)  #making query readable for www ( for ex. translate spaces)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read() #reading www
    parsed = json.loads(data) #python dictionary
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]
                  }
    return weather

@app.route("/", methods=['GET','POST'])
def get_news(number = "bbc"):
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("Warsaw")
    return render_template("home.html",articles=feed["entries"],weather=weather)
    


if __name__ == '__main__':
  app.run(port=5002, debug=True)
  
  