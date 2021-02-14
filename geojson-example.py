import json
from collections import OrderedDict

import pandas as pd
from geojson import Feature, FeatureCollection, Point

# オープンデータ用北海道施設位置情報データベース
# @see https://koukita.github.io/hokkaido_od_geodatabase/
url = "https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv"
df = pd.read_csv(url, encoding="cp932")


def __make_feature(row: pd.Series):
    """ GeoJSONのFeature要素(Point)を作成 """
    coords = (row["経度"], row["緯度"])
    props = OrderedDict(
        {
            "施設名": row["施設名"],
            "検索用住所": row["検索用住所"],
            "データ区分": row["データ区分"],
        }
    )
    return Feature(geometry=Point(coords), properties=props)


features = df.apply(__make_feature, axis=1).tolist()

dest = "doc/example.geojson"
with open(dest, "w", encoding="utf-8") as f:
    json.dump(FeatureCollection(features), f, ensure_ascii=False, indent=2)
