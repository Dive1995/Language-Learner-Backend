import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "video", {"video_id":"QDLLgV2fgx4", "lang":"de"})
response = requests.post(BASE + "video", {"video_id":"dBF65_kHdNg", "lang":"de"})
print(response.json())


# # dBF65_kHdNg working (EN, has many other languages too)