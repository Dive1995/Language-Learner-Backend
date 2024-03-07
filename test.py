import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "video", json={"video_id":"uF_pY__Hgu0", "lang": {
        "first": ["de", "de-DE"],
        "second": ["en"]
    }})
# response = requests.post(BASE + "vocabulary/context", {"word":"nichts"})
# response = requests.post(BASE + "vocabulary/translation", {"input":"Hund", "to":"de", "from":"en"})
# response = requests.get(BASE + "video", {"video_id":"dBF65_kHdNg", "lang":"de"})
print(response.json())


# # dBF65_kHdNg working (EN, has many other languages too)