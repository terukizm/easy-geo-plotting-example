import folium
import pandas as pd
from folium.plugins import MarkerCluster

# オープンデータ用北海道施設位置情報データベース
url = "https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv"
df = pd.read_csv(url, encoding="cp932")
df = df.query('データ区分 != "国・都道府県機関"')

print(df)

my_map = folium.Map(
    location=[43.0645597, 141.3481196],
    zoom_start=10,
    width="100%",
    height="90%",
    tiles="openstreetmap",
)
marker_cluster = MarkerCluster()

for _, row in df.iterrows():
    lat = row["緯度"]
    lng = row["経度"]
    name = row["施設名"]
    address = row["検索用住所"]
    data_type = row["データ区分"]

    popup_html = f"""
<h1>{name}</h1>
<h2>{address}</h2>
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
    popup = folium.Popup(
        folium.IFrame(popup_html), min_width=400, max_width=400
    )
    folium.Marker(
        location=[lat, lng], popup=popup, icon=folium.Icon(color="red")
    ).add_to(marker_cluster)


marker_cluster.add_to(my_map)
my_map.save("docs/folium.html")
