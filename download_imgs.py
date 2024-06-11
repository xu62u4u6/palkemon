import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def download_imgs(df, dir):
    os.makedirs(dir, exist_ok=True)
    for ind in range(len(df)):
        img_url, name = df.loc[ind, ["herf", "name"]]
        img_response = requests.get(img_url)

        if img_response.status_code == 200:
            with open(f'{dir}/{name}.jpg', 'wb') as f:
                f.write(img_response.content)
        df.loc[ind, "res"] =  img_response.status_code
    return df

# 準備pal的圖片資料
pal_url = "https://palworld.fandom.com/wiki/Alpha_Pals"
res = requests.get(pal_url)
assert res.status_code == 200
soup = BeautifulSoup(res.text, 'html.parser')

# 創建需要爬取的表格列表
table_elements = soup.select('#mw-content-text > div > table')
pal_df = pd.DataFrame(columns=["name", "herf", "res"])
for table in table_elements:
    # 提取名稱和連結並填入df
    url_elements = table.find_all('a', href=True)
    for ind in range(0, len(url_elements), 2):
        pal_df.loc[ind, "herf"] = url_elements[ind]["href"]
        pal_df.loc[ind, "name"] = url_elements[ind+1]["title"]
pal_df.index = range(len(pal_df))
pal_df.head()


# 準備pokemon的圖片資料
pokemon_url = "https://pokemondb.net/pokedex/national"
response = requests.get(pokemon_url)
assert res.status_code == 200
soup = BeautifulSoup(response.text, 'html.parser')

pokemon_df = pd.DataFrame(columns=["name", "herf", "res"])

# 抓出所有infocard元素
infocards = soup.select('.infocard')
for ind, infocard in enumerate(infocards):
    # 提取名稱和連結並填入df
    name = infocard.select_one('.ent-name').text.strip()
    img_link = infocard.select_one('.infocard-lg-img img')['src']
    pokemon_df.loc[ind, "herf"] = img_link
    pokemon_df.loc[ind, "name"] = name

# 存圖片到本地
pal_df = download_imgs(pal_df, "test1")
pokemon_df = download_imgs(pokemon_df, "test2")

