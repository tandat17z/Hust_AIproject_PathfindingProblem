import folium
import json
import io
import chardet
from bs4 import BeautifulSoup
import re

def buildMap(path, geojson_file):
    with open(geojson_file, 'rb') as f:
        result = chardet.detect(f.read())
    with io.open(geojson_file, 'r', encoding=result['encoding']) as f:
        data = json.load(f)

    map = folium.Map(location=(21.0444, 105.8430), zoom_start=17)

    folium.GeoJson(
        data,
        name="Trucbach-Badinh-Hanoi-Vietnam",
        tooltip = folium.GeoJsonTooltip(fields=["@id","name", "highway"]),
        style_function=lambda x: {
            # "fillColor": "#ffff00",
            "color": "rgba(0, 0, 0, 0)",
            "weight": 6,
        },
        highlight_function=lambda x: {
            "color": "rgba(55, 245, 39, 0.8)",
            "weight": 8,
        },
    ).add_to(map)
    map.save(path)


def addBlockToHtml(path):
    content_link = '''
    {% block link %} {% endblock link %}
    '''
    content_script = '''
    {% block script %} {% endblock script %}
    '''
    with open(path, "r") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")
    soup.body.insert(0, content_link)
    soup.html.append(content_script)

    # Lưu lại file sau khi chỉnh sửa
    with open(path, "w") as file:
        file.write(str(soup))


#---------------main-----------------
# path = "map.html"
geojson_file = 'geojson/mapTrucBach.geojson'
path = "../website/app/templates/base/map.html"
buildMap(path, geojson_file)
addBlockToHtml(path)

