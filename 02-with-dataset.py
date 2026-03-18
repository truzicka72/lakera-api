#!uv run 

from click import prompt
import pandas as pd

import requests
import os

# dataset from Hugging Face
df = pd.read_json("hf://datasets/OpenSafetyLab/Salad-Data/base_set.json")

# print(df.head())
# print(df.columns)

# select random prompt
prompt = df.sample(1)["question"].values[0]
print(prompt)


# get from .env file LAKERA_GUARD_API_KEY
lakera_guard_api_key=os.getenv("LAKERA_GUARD_API_KEY")

session = requests.Session()  # Allows persistent connection
response = session.post(
    "https://api.lakera.ai/v2/guard",
    json={"breakdown":True, "messages": [{"content": prompt, "role": "user"}]},
    headers={"Authorization": f"Bearer {lakera_guard_api_key}"},
)
result = response.json()

print(result)

if result.get("flagged"):
    detected = [b for b in result.get("breakdown", []) if b.get("detected")]
    print(f"FLAGGED | {result['metadata']['request_uuid']}")
    for d in detected:
        print(f"  - {d['detector_type']}")
else:
    print("Not flagged")

