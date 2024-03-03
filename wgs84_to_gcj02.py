import json
import math

def wgs84_to_gcj02(lon, lat):
    """
    将WGS 84坐标转换为GCJ-02坐标
    :param lon: 经度
    :param lat: 纬度
    :return: 转换后的经纬度
    """
    def transform_lat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transform_lon(x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret

    def delta(lat, lon):
        a = 6378245.0  # 地球长半轴
        ee = 0.00669342162296594323  # 偏心率平方
        d_lat = transform_lat(lon - 105.0, lat - 35.0)
        d_lon = transform_lon(lon - 105.0, lat - 35.0)
        rad_lat = lat / 180.0 * math.pi
        magic = math.sin(rad_lat)
        magic = 1 - ee * magic * magic
        sqrt_magic = math.sqrt(magic)
        d_lat = (d_lat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * math.pi)
        d_lon = (d_lon * 180.0) / (a / sqrt_magic * math.cos(rad_lat) * math.pi)
        mg_lat = lat + d_lat
        mg_lon = lon + d_lon
        return mg_lon, mg_lat

    if lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271:
        return lon, lat
    else:
        return delta(lat, lon)

# 示例使用

def convert_coordinates(nested_coordinates, all_coordinates):
    """
    递归转换坐标系

    :param nested_coordinates: 嵌套的坐标列表
    :param all_coordinates: 所有转换后的坐标将被添加到这个列表
    """
    if isinstance(nested_coordinates, list):
        # 检查当前列表是否代表一个坐标对 [lon, lat]
        if len(nested_coordinates) == 2 and all(isinstance(coord, (float, int)) for coord in nested_coordinates):
            # 假设 wgs84_to_gcj02 是一个函数，用于转换坐标系
            gcj02_lon, gcj02_lat = wgs84_to_gcj02(nested_coordinates[0], nested_coordinates[1])
            all_coordinates.append([gcj02_lon, gcj02_lat])
        else:
            # 如果当前列表不是坐标对，递归处理列表中的每个元素
            for item in nested_coordinates:
                convert_coordinates(item, all_coordinates)

def file_deal(input_file_path):
    try:
        with open(input_file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)  # 加载JSON数据

        all_coordinates = []
        for feature in data["features"]:
            geometry = feature["geometry"]
            convert_coordinates(geometry["coordinates"],all_coordinates)

        formatted_data = []
        for i, coords in enumerate(all_coordinates):
            next_id = i + 1 if i + 1 < len(all_coordinates) else 0
            formatted_data.append({
                "id": i,
                "location": f"{coords[0]},{coords[1]}",
                "edge": [next_id]
            })

        formatted_output_file_path = 'a.json'
        with open(formatted_output_file_path, 'w',encoding='utf-8') as file:
            json.dump(formatted_data, file, indent=4)




    except Exception as e:
        print(f"处理文件时出错: {e}")

    print('ok')


if __name__ == "__main__":
    file_deal(input_file_path='export (4).json')
