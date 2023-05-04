import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/weight_data4.csv')

# datetimeカラムを文字列型に変換し、日付部分だけを取り出す
df['Date'] = df['Date'].str.split(' ').str[0]

# 結果を表示
print(df)

# CSVファイルに保存
df.to_csv('/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/weight_data4.csv', index=False)
