from pathlib import Path

import pandas as pd
import requests

# Документация к запросам https://eonet.gsfc.nasa.gov/docs/v3
URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

# список для сбора данных
records = []
category = "wildfires"  # категория событий, которую мы хотим получить
max_days = 30

params = {"status": "all", "category": category, "days": max_days}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

events = response.json()["events"]
for event in events:
    for geometry in event.get("geometry", []):
        if geometry["type"] != "Point":
            continue

        record = {
            "id": event.get("id"),
            "title": event.get("title"),
            "description": event.get("description"),
            "link": event.get("link"),
            "category": category,
            "date": geometry.get("date"),
            "longitude": geometry.get("coordinates")[0],
            "latitude": geometry.get("coordinates")[1],
        }
        records.append(record)

df = pd.DataFrame(records)


# Выберем только нужные колонки для предпросмотра
preview_columns = ["id", "date", "longitude", "latitude"]
print(df[preview_columns].head(15).to_string(index=False))


project_root = Path(__file__).resolve().parents[2]
output = project_root / "data" / "wildfires.csv"

output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False, encoding="utf-8")
print(f"Датасет сохранён: {output}")
