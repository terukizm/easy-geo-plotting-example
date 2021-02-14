easy-geo-plotting-example
---

@see https://terukizm.github.io/easy-geo-plotting-example/


# Usage

## Setup

```
$ git clone git@github.com:terukizm/easy-geo-plotting-example.git
$ cd easy-geo-plotting-example/
$ poetry install
```

## generate folium

```
$ poetry run python main.py folium
$ open docs/folium.html
```

## generate geojson

```
$ poetry run python main.py geojson
$ cat docs/example.geojson | jq .
```
## geolonia example

```
$ cd docs/
$ python -m http.server 18080
-> http://localhost:18080/geolonia.html
```
