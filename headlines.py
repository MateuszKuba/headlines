import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import feedparser
from flask import Flask

app = Flask(__name__)

BBC_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }




@app.route("/")
@app.route("/<number>")
def get_news(number = "bbc"):
    feed = feedparser.parse(BBC_FEEDS[number])
    first_article = feed['entries'][0]        
    first = first_article.get("summary")
    return """<html>
    <body>
        <h1> BBC Headlines </h1>
        <b>{0}</b> <br/>
        <i>{1}</i> <br/>
        <p>{2}</p> <br/>
    </body>
    </html>""".format(first_article.get("title"),first_article.get("published")
    ,first)
    


if __name__ == '__main__':
  app.run(port=5002, debug=True)
  
  