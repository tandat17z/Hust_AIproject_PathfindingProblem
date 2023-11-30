import folium
import json
import io
import chardet
from bs4 import BeautifulSoup
import re

def BuildMap(path):
    geojson_file = 'geojson/export.geojson'
    with open(geojson_file, 'rb') as f:
        result = chardet.detect(f.read())
    with io.open(geojson_file, 'r', encoding=result['encoding']) as f:
        data = json.load(f)

    map = folium.Map(location=(21.0444, 105.8430), zoom_start=17)

    folium.GeoJson(
        data,
        name="Trucbach-Badinh-Hanoi-Vietnam",
        tooltip = folium.GeoJsonTooltip(fields=["name", "highway"]),
        style_function=lambda x: {
            # "fillColor": "#ffff00",
            "color": "rgba(0, 0, 0, 0.3)",
            "weight": 6,
        },
        highlight_function=lambda x: {
            "color": "rgba(55, 245, 39, 0.8)",
            "weight": 8,
        },
    ).add_to(map)

    map.add_child(
        folium.ClickForMarker('<b>Lat:</b> ${lat} <br /><b>Lon:</b> ${lng}')
    )

    map.save(path)


# Đoạn mã JavaScript mới để thay thế
NEW_CODE1 = '''
var num = 0;
function newMarker(e){
    if( num < 2){
        num += 1;
'''

NEW_CODE2 = 'toFixed(8)'

NEW_CODE3 = '''
if( num == 1){
    new_mark.bindTooltip(`<b>Start</b> <br /> <b>Lat:</b> ${lat} <br /><b>Lng:</b> ${lng}`);
}
else{
    new_mark.bindTooltip(`<b>End</b> <br /> <b>Lat:</b> ${lat} <br /><b>Lng:</b> ${lng}`);
}

var searchLink = document.getElementById("search");
searchLink.href += ('_' +encodeURIComponent(lat) + '_' + encodeURIComponent(lng));
}
};
'''

def editHtml(path):
    with open(path, "r") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")

    # thêm thẻ <a> Tìm kiếm ------------------
    new_div = soup.new_tag("p", style= "text-align: center;")

    new_a_tag = soup.new_tag("a", href="", id="search")
    new_a_tag.string = "Seach"

    new_div.append(new_a_tag)
    soup.body.insert(0, new_div)

    # Sửa function newMarker
    script_tag = soup.find('script', string=lambda text: 'function newMarker' in str(text))
    if script_tag:
        pattern1 = re.compile(r'function newMarker\((.*?)\)\s*{', re.DOTALL)
        pattern2 = re.compile(r'toFixed\(.\)')
        pattern3 = re.compile(r'new_mark.bind[^;]*;[^;]*;')
        pattern4 = re.compile(r'new_mark.dragging.enable\(\);')
        script_tag.string = re.sub(pattern1, NEW_CODE1, script_tag.string)
        script_tag.string = re.sub(pattern2, NEW_CODE2, script_tag.string)
        script_tag.string = re.sub(pattern3, NEW_CODE3, script_tag.string)
        script_tag.string = re.sub(pattern4, '', script_tag.string)

    # Lưu lại file sau khi chỉnh sửa
    with open(path, "w") as file:
        file.write(str(soup))


#---------------main-----------------
path = "../website/app/templates/map.html"
# path = "map.html"
BuildMap(path)
editHtml(path)

