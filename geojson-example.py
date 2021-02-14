import json
from collections import OrderedDict

import pandas as pd
from geojson import Feature, FeatureCollection, Point

# オープンデータ用北海道施設位置情報データベース
# @see https://koukita.github.io/hokkaido_od_geodatabase/
url = "https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv"
df = pd.read_csv(url, encoding="cp932").fillna("")  # geojsonはnullが入るとコケるので空文字に倒す
df = df.query('データ区分 != "国・都道府県機関"')

print(df)

def __make_feature(row: pd.Series):
    """ GeoJSONのFeature要素(Point)を作成 """
    lat = row["緯度"]
    lng = row["経度"]
    name = row["施設名"]
    address = row["検索用住所"]
    data_type = row["データ区分"]

    coords = (lng, lat)
    description = f"""
    <p>{address}</p>
<table>
  <tbody>
    <tr>
        <th>緯度</th>
        <td>{lat}</td>
    </tr>
    <tr>
        <th>経度</th>
        <td>{lng}</td>
    </tr>
    <tr>
        <th>データ区分</th>
        <td>{data_type}</td>
    </tr>
  </tbody>
</table>
"""
    props = OrderedDict(
        {
            "title": name,
            "description": description,
        }
    )
    return Feature(geometry=Point(coords), properties=props)


features = df.apply(__make_feature, axis=1).tolist()

# pretty
# (ファイルサイズはあまり関係なく、properties数が多くなりすぎるとGitHubで表示できなくなる)
dest = "docs/example.geojson"
with open(dest, "w", encoding="utf-8") as f:
    json.dump(FeatureCollection(features), f, ensure_ascii=False, indent=2)
