import json
from collections import OrderedDict

import pandas as pd
import typer
from folium import Map, Popup, Marker, Icon, IFrame
from folium.plugins import MarkerCluster
from geojson import Feature, FeatureCollection, Point

app = typer.Typer()

# オープンデータ用北海道施設位置情報データベース
# @see https://koukita.github.io/hokkaido_od_geodatabase/
url = "https://koukita.github.io/hokkaido_od_geodatabase/data/Hokkaido_OD_GeoDataBase2018.csv"

# geojsonはnullが入るとコケるので空文字に倒す
df = pd.read_csv(url, encoding="cp932").fillna(
    ""
)
df = df.query('データ区分 != "国・都道府県機関"')  # 該当データはlat=lngとなっており作成ミスっぽいので削除


@app.command()
def all():
    folium()
    geojson()

@app.command()
def geojson(dest="docs/example.geojson", pretty=True):
    """ genreate example.geojson """
    def __feature(row: pd.Series):
        """ GeoJSONのFeature要素(Point)を作成 """
        lat = row["緯度"]
        lng = row["経度"]
        name = row["施設名"]
        address = row["検索用住所"]
        data_type = row["データ区分"]

        coords = (lng, lat)  # 順番に注意
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

    # genrerate feature list
    features = df.apply(__feature, axis=1).tolist()

    # pretty or minify
    # (ファイルサイズはあまり関係なく、properties数が多くなりすぎるとGitHubで表示できなくなる)
    with open(dest, "w", encoding="utf-8") as f:
        if pretty:
            json.dump(
                FeatureCollection(features), f, ensure_ascii=False, indent=2
            )
        else:
            json.dump(
                FeatureCollection(features),
                f,
                ensure_ascii=False,
                separators=(",", ":"),
            )


@app.command()
def folium(dest="docs/folium.html"):
    """ genreate folium.html """
    my_map = Map(
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
        popup = Popup(
            IFrame(popup_html), min_width=400, max_width=400
        )
        Marker(
            location=[lat, lng], popup=popup, icon=Icon(color="red")
        ).add_to(marker_cluster)

    marker_cluster.add_to(my_map)
    my_map.save(dest)


if __name__ == "__main__":
    """
    usage:
      $ python main.py folium
      $ python main.py geojson
    """
    app()
