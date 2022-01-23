from html.parser import HTMLParser
import requests
import subprocess

class ForecastParser(HTMLParser):
    encounteredTodaysForecast = False 
    forecast = ""

    def feed(self, feed):
        self.forecast = ""
        super().feed(feed)
        return self.forecast

    def handle_starttag(self, startTag, attrs):
        if startTag == "p" and attrs and attrs[0][1] == "navToTop":
           encounteredTodaysForecast = False
        elif startTag == "a":
            encounteredTodaysForecast = False

    def handle_data(self, data):

        if data.startswith("Vorhersage  - heute"):
            self.encounteredTodaysForecast = True
        elif data.startswith("Vorhersage  - morgen") or data.startswith("Vorhersage  - morgen"):
            self.encounteredTodaysForecast = False
        elif self.encounteredTodaysForecast and data and len(data) > 3:
            self.forecast += data

        
try:
    parser = ForecastParser()
    url = "https://www.dwd.de/DE/wetter/vorhersage_aktuell/berlin_brandenburg/vhs_bbb_node.html"
    headers = {'User-Agent': 'Wetteransage'}
    result = requests.get(url, headers=headers)
    forecast = parser.feed(result.text)
    subprocess.call(f'espeak-ng -vde-DE "{forecast}"', shell=True)  

except:
    print("Invalid URL or some error occured while making the GET request to the specified URL")