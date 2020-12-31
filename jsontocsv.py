import pandas as pd
df = pd.read_json('StreamingHistory1.json')
df.to_csv('op1.csv')