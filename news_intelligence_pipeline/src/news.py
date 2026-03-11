import requests
import json

params = {
    'q': 'Apple bitcoin microsoft',
    'sortBy': 'popularity',
    'apiKey': '{API_KEY}'
}

response = requests.get("https://newsapi.org/v2/everything?",params=params)

if response.status_code == 200:
 data = response.json()

with open('news_intelligence_pipeline/data/news_api_response.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)