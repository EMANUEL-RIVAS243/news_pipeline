
import pandas as pd
import requests
import json
import schedule
import time
from datetime import datetime

def job():
    url = ('https://newsapi.org/v2/top-headlines?country=us&apiKey=08600cff031f4911856bdbd35290b326')
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data['articles']) # type: ignore
    df.fillna('Unknown', inplace=True)

    df = df[['title', 'publishedAt', 'source.id']]
    df.rename(columns={"publishedAt":"date", "source.id":"source"}, inplace=True) # type: ignore

    filename = f"news_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    # Exporting to csv
    df.to_csv(filename, columns=['date', 'title', 'source'], index=False)
    print(f"[{datetime.now()}] CSV guardado como {filename}")

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
