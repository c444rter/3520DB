import mechanicalsoup
import pandas as pd
import sqlite3

url = "https://en.wikipedia.org/wiki/Textile"
browser = mechanicalsoup.StatefulBrowser()
browser.open(url)

table = browser.page.find_all("table")

td = table[0].find_all("td")
textiles = [value.text.strip() for value in td]

print(textiles)


column_names = ["Name", 
                "Product",
                "Type",
                "TextilesNamedBy",
                "Description"
                ]

# column[0:][::5]
# # column[1:][::11]
# # column[2:][::11]

dictionary = {}

for idx, key in enumerate(column_names):
    dictionary[key] = textiles[idx:][::5]


df = pd.DataFrame(data = dictionary)
print(df.head())
print(df.tail())

connection = sqlite3.connect("textile.db")
cursor = connection.cursor()
cursor.execute("create table Textile ( " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into Textile values (?,?,?,?,?)", df.iloc[i])

connection.commit()

connection.close()