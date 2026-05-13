import requests
import random
from datetime import datetime
class ChinaEnvironmentMonitor:
    def get_city_by_ip(self):  # 高德IP定位API
        api_key = '32eb1903eb56c179b6771571a80d65bc'
        url = f"https://restapi.amap.com/v3/ip?key={api_key}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            if data["status"] == "1":
                city = data.get("city", "未知")
                return city[:-1] if city.endswith("市") else city
            else:
                return "定位失败"
        except Exception as e:
            return f"错误: {str(e)}"
    def __init__(self, city=None):  # 允许用户手动指定城市
        self.city = city or self.get_city_by_ip()  # 优先使用用户指定的城市
        self.amap_key = '32eb1903eb56c179b6771571a80d65bc'
    def get_co2_simulation(self):
        """模拟生成CO₂浓度数据（单位：ppm）"""
        base = 400  # 大气本底值
        hour = datetime.now().hour
        # 模拟交通高峰波动
        fluctuation = 50 * abs((hour - 8) / 12) + random.uniform(-10, 10)
        return round(base + fluctuation, 1)
    def get_light_intensity(self):
        """通过天气现象推算光照强度（单位：lux）"""
        try:
            # 获取实时天气
            url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={self.amap_key}&city={self.get_city_by_ip()}"
            res = requests.get(url).json()
            weather = res['lives'][0]['weather']
            # 根据天气推算光照
            light_map = {
                "晴": 80000,  # 晴天
                "多云": 30000,  # 多云
                "阴": 10000,  # 阴天
                "雨": 5000,  # 雨天
                "雪": 7000  # 雪天
            }
            return light_map.get(weather, 20000)  # 默认值
        except Exception as e:
            print(f"获取光照强度失败: {str(e)}")
            return None
# 使用示例
monitor = ChinaEnvironmentMonitor()
print(f"模拟CO₂浓度: {monitor.get_co2_simulation()}ppm")
print(f"推算光照强度: {monitor.get_light_intensity()}lux")