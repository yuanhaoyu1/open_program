import requests
class weather_get:
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
        self.url_live = f'https://restapi.amap.com/v3/weather/weatherInfo?key={self.amap_key}&city={self.city}'
        self.url_all = f'https://restapi.amap.com/v3/weather/weatherInfo?key={self.amap_key}&city={self.city}&extensions=all'
        self.response = ""
    def get_weather(self):
        """Get the current weather"""
        try:
            # 获取实时天气数据
            self.response_live = requests.get(self.url_live)
            if self.response_live.status_code != 200:
                raise Exception(f"实时天气请求失败，状态码: {self.response_live.status_code}")
            weather_data_live = self.response_live.json()
            if weather_data_live.get("status") != "1" or not weather_data_live.get("lives"):
                raise Exception("实时天气数据无效")
            # 获取未来天气数据
            self.response_all = requests.get(self.url_all)
            if self.response_all.status_code != 200:
                raise Exception(f"未来天气请求失败，状态码: {self.response_all.status_code}")
            weather_data_all = self.response_all.json()
            if weather_data_all.get("status") != "1" or not weather_data_all.get("forecasts"):
                raise Exception("未来天气数据无效")
            # 解析实时天气数据
            live_weather = weather_data_live["lives"][0]
            self.weather_live = live_weather.get("weather", "未知")
            self.temp_live = live_weather.get("temperature", "未知")
            self.humidity = live_weather.get("humidity", "未知")
            # 解析未来天气数据
            forecast = weather_data_all["forecasts"][0]
            today_weather = forecast["casts"][0]
            tomorrow_weather = forecast["casts"][1]
            self.weather_all = today_weather.get("dayweather", "未知")
            self.temp_all = today_weather.get("daytemp", "未知")
            self.weather_all_two = tomorrow_weather.get("dayweather", "未知")
            self.temp_all_two = tomorrow_weather.get("daytemp", "未知")
            return (
                self.weather_live,
                self.weather_all,
                self.temp_live,
                self.temp_all,
                self.weather_all_two,
                self.temp_all_two,
            )
        except Exception as e:
            print(f"获取天气数据失败: {str(e)}")
            # 返回默认值
            return "未知", "未知", "未知", "未知", "未知", "未知"
    def get_weather_detail(self):
        i = 1
        #Get the detailed weather
        self.response_all = requests.get(self.url_all)
        if self.response_all.status_code == 200:
            # 解析响应内容，通常返回的是JSON格式
            weather_data_all = self.response_all.json()
        else:
            if i < 30:
                self.get_weather()
                i = i + 1
        if weather_data_all:
            # print("yes")
            weather_data_all = weather_data_all['forecasts'][0]['casts']
        # print(weather_data_all)
        return weather_data_all
# 主函数
if __name__ == '__main__':
    weather = weather_get()
    print(f"城市: {weather.city}")
    print("天气数据:", weather.get_weather())