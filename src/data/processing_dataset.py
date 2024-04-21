import pandas as pd
from sklearn.feature_selection import mutual_info_regression

df = pd.read_csv("../data/raw/mbajk_dataset.csv")
df.head()

df.drop(columns=["Unnamed: 0"], inplace=True)
df["date"] = pd.to_datetime(df["date"])
df.sort_values(by="date", inplace=True)
df.head()

df.isnull().sum()

for column in ['temperature', 'precipitation_probability', 'rain']:
    df.interpolate(method='linear', inplace=True)
    
df.isnull().sum()

target = "available_bike_stands"

input_cols = df.columns.tolist()
input_cols.remove(target)
input_cols.remove("date")

information_gain = mutual_info_regression(df[input_cols], df[target])

feature_importance = pd.Series(information_gain, index=input_cols)
feature_importance.sort_values(ascending=False, inplace=True)

top_features = feature_importance.head(4).index.tolist()
print(top_features)

df.to_csv("../data/processed/mbajk_processed.csv", index=False)