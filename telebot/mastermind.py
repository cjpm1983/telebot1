import json
#import requests
from meaningless import WebExtractor


def get_response(msg):
    """
    you can place your mastermind AI here
    could be a very basic simple response like "معلش"
    or a complex LSTM network that generate appropriate answer
    """
    #r=requests.get("https://api.scripture.api.bible/v1/bibles", headers={"api-key":"b85d82225553e46aa3c3ea89142e7739"})
    #r=requests.get("https://api.scripture.api.bible/v1/bibles/a6aee10bb058511c-02/verses/JHN.3.16\?fums-version\=3",headers={"api-key":"b85d82225553e46aa3c3ea89142e7739"})

    #data = json.loads(r.text)['data']
    #data = json.loads(r.text)
    #bible = WebExtractor()
    #passage = bible.get_passage('Ecclesiastes', 1, 2)
    return "Dios te bendiga"

print(get_response("lolo"))
