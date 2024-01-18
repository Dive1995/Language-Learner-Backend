import requests
from fake_useragent import UserAgent

ua = UserAgent()

random_agent= ua.random
headers = {'User-Agent': random_agent, 'Content-Type': 'application/json'}


REVERSO_TRANSLATE_BASE_URL = "https://api.reverso.net/translate/v1/translation"

def reverso_translate(data):
    print("data", data)
    print("Agent ", random_agent)
    payload = {
	    "format": "text",
	    "from": data['from'],
	    "input": data['input'],
        "options": {
	        "sentenceSplitter": True, 
            "origin": "translation.web", 
            "languageDetection": True,
            "contextResults": True,
        },
        "to": data['to']
    }
    response = requests.post(REVERSO_TRANSLATE_BASE_URL, json=payload, headers=headers)
    return response