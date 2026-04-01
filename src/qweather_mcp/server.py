import os
import json
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

QWEATHER_API_KEY = os.environ.get("QWEATHER_API_KEY", "")
QWEATHER_API_URL = os.environ.get("QWEATHER_API_URL", "https://devapi.qweather.com")

class QWeatherClient:
    def __init__(self, api_key: str, api_url: str = None):
        self.api_key = api_key
        self.api_url = api_url or QWEATHER_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_location(self, location: str) -> dict:
        """搜索城市"""
        url = f"{self.api_url}/geo/v2/city/lookup"
        params = {
            "location": location,
            "key": self.api_key,
            "number": 5
        }
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def get_current_weather(self, location_id: str) -> dict:
        """实时天气"""
        url = f"{self.api_url}/v7/weather/now"
        params = {"location": location_id, "key": self.api_key}
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def get_forecast(self, location_id: str, days: int = 3) -> dict:
        """天气预报"""
        endpoint = "7d" if days == 7 else "3d"
        url = f"{self.api_url}/v7/weather/{endpoint}"
        params = {"location": location_id, "key": self.api_key}
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def get_air_quality(self, location_id: str) -> dict:
        """空气质量 (v7版本，已弃用但仍可用)"""
        url = f"{self.api_url}/v7/air/now"
        params = {"location": location_id, "key": self.api_key}
        response = await self.client.get(url, params=params)
        return response.json()
    
    async def get_warning_v1(self, latitude: str, longitude: str) -> dict:
        """天气预警 v1版本 (推荐)"""
        url = f"{self.api_url}/weatheralert/v1/current/{latitude}/{longitude}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = await self.client.get(url, headers=headers)
        return response.json()
    
    async def get_warning_v7(self, location_id: str) -> dict:
        """天气预警 v7版本 (已弃用，2026年10月停止服务)"""
        url = f"{self.api_url}/v7/warning/now"
        params = {"location": location_id, "key": self.api_key}
        response = await self.client.get(url, params=params)
        return response.json()

# 创建MCP Server
app = Server("qweather-mcp")
weather_client: QWeatherClient = None

@app.list_tools()
async def list_tools() -> list[Tool]:
    """定义可用工具"""
    return [
        Tool(
            name="search_city",
            description="搜索城市信息，获取城市ID（查询天气前需要先获取城市ID）",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，支持中文、拼音、英文，如'北京'、'beijing'"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="get_current_weather",
            description="获取指定城市的实时天气情况，包括温度、体感温度、天气状况、风向风力、湿度、气压、能见度等",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "城市ID，通过search_city工具获取"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="get_weather_forecast",
            description="获取指定城市的天气预报，支持3天或7天预报",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "城市ID，通过search_city工具获取"
                    },
                    "days": {
                        "type": "integer",
                        "description": "预报天数，可选3或7，默认为3",
                        "enum": [3, 7],
                        "default": 3
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="get_air_quality",
            description="获取指定城市的实时空气质量指数(AQI)、PM2.5、PM10、空气质量等级等信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "城市ID，通过search_city工具获取"
                    }
                },
                "required": ["location_id"]
            }
        ),
        Tool(
            name="get_weather_warning",
            description="获取指定城市的天气灾害预警信息，如台风、暴雨、高温等预警",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_id": {
                        "type": "string",
                        "description": "城市ID，通过search_city工具获取"
                    },
                    "latitude": {
                        "type": "string",
                        "description": "纬度（可选，用于新版预警API）"
                    },
                    "longitude": {
                        "type": "string",
                        "description": "经度（可选，用于新版预警API）"
                    }
                },
                "required": ["location_id"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    global weather_client
    if not weather_client:
        api_key = os.environ.get("QWEATHER_API_KEY", "")
        if not api_key:
            return [TextContent(type="text", text="错误：未设置QWEATHER_API_KEY环境变量")]
        weather_client = QWeatherClient(api_key)
    
    try:
        if name == "search_city":
            location = arguments.get("location", "")
            data = await weather_client.search_location(location)
            
            if data.get("code") != "200" or not data.get("location"):
                return [TextContent(type="text", text=f'未找到城市"{location}"，请检查城市名称是否正确。')]
            
            cities = []
            for city in data["location"]:
                cities.append({
                    "id": city["id"],
                    "name": city["name"],
                    "full_name": f"{city['adm1']} {city['adm2']} {city['name']}",
                    "lat": city["lat"],
                    "lon": city["lon"]
                })
            
            result = "找到以下城市：\n\n"
            for i, c in enumerate(cities, 1):
                result += f"{i}. {c['full_name']}\n   ID: {c['id']}\n   坐标: {c['lat']}, {c['lon']}\n\n"
            result += "请使用对应的城市ID查询天气。"
            
            return [TextContent(type="text", text=result)]
        
        elif name == "get_current_weather":
            location_id = arguments.get("location_id", "")
            data = await weather_client.get_current_weather(location_id)
            
            if data.get("code") != "200":
                return [TextContent(type="text", text=f"获取天气失败: {data.get('code')}")]
            
            now = data["now"]
            result = (
                f"🌤️ 实时天气\n\n"
                f"观测时间: {now['obsTime']}\n"
                f"温度: {now['temp']}°C (体感 {now['feelsLike']}°C)\n"
                f"天气: {now['text']}\n"
                f"风向: {now['windDir']} {now['windScale']}级 ({now['windSpeed']}km/h)\n"
                f"湿度: {now['humidity']}%\n"
                f"气压: {now['pressure']}hPa\n"
                f"能见度: {now['vis']}km\n"
                f"降水量: {now['precip']}mm"
            )
            return [TextContent(type="text", text=result)]
        
        elif name == "get_weather_forecast":
            location_id = arguments.get("location_id", "")
            days = arguments.get("days", 3)
            data = await weather_client.get_forecast(location_id, days)
            
            if data.get("code") != "200":
                return [TextContent(type="text", text=f"获取预报失败: {data.get('code')}")]
            
            result = f"📊 {days}天天气预报\n\n"
            for day in data["daily"]:
                result += (
                    f"📅 {day['fxDate']}\n"
                    f"   白天: {day['textDay']} {day['tempMax']}°C\n"
                    f"   夜间: {day['textNight']} {day['tempMin']}°C\n"
                    f"   风向: {day['windDirDay']} {day['windScaleDay']}级\n"
                    f"   湿度: {day['humidity']}% 降水概率: {day.get('precip', '0')}%\n\n"
                )
            return [TextContent(type="text", text=result)]
        
        elif name == "get_air_quality":
            location_id = arguments.get("location_id", "")
            data = await weather_client.get_air_quality(location_id)
            
            if data.get("code") != "200":
                return [TextContent(type="text", text=f"获取空气质量失败: {data.get('code')}")]
            
            air = data["now"]
            result = (
                f"🌫️ 空气质量指数\n\n"
                f"AQI: {air['aqi']} ({air['category']})\n"
                f"PM2.5: {air['pm2p5']} μg/m³\n"
                f"PM10: {air['pm10']} μg/m³\n"
                f"NO₂: {air['no2']} μg/m³\n"
                f"SO₂: {air['so2']} μg/m³\n"
                f"CO: {air['co']} mg/m³\n"
                f"O₃: {air['o3']} μg/m³\n"
                f"主要污染物: {air.get('primary', '无')}"
            )
            return [TextContent(type="text", text=result)]
        
        elif name == "get_weather_warning":
            location_id = arguments.get("location_id", "")
            latitude = arguments.get("latitude", "")
            longitude = arguments.get("longitude", "")
            
            if latitude and longitude:
                data = await weather_client.get_warning_v1(latitude, longitude)
                
                alerts = data.get("alerts", [])
                if not alerts:
                    return [TextContent(type="text", text="✅ 当前无天气灾害预警")]
                
                result = "🚨 天气预警\n\n"
                for w in alerts:
                    severity_map = {"minor": "轻微", "moderate": "中等", "severe": "严重", "extreme": "极端"}
                    severity = severity_map.get(w.get("severity", ""), w.get("severity", ""))
                    result += (
                        f"⚠️ {w.get('headline', w.get('eventType', {}).get('name', '未知预警'))}\n"
                        f"级别: {severity}\n"
                        f"类型: {w.get('eventType', {}).get('name', '未知')}\n"
                        f"发布时间: {w.get('issuedTime', '')}\n"
                        f"生效时间: {w.get('effectiveTime', '')} 至 {w.get('expireTime', '')}\n"
                        f"内容: {w.get('description', '')}\n\n"
                    )
                return [TextContent(type="text", text=result)]
            else:
                data = await weather_client.get_warning_v7(location_id)
                
                if data.get("code") != "200":
                    return [TextContent(type="text", text=f"获取预警信息失败: {data.get('code')}")]
                
                warnings = data.get("warning", [])
                if not warnings:
                    return [TextContent(type="text", text="✅ 当前无天气灾害预警")]
                
                result = "🚨 天气预警\n\n"
                for w in warnings:
                    result += (
                        f"⚠️ {w['title']}\n"
                        f"级别: {w.get('severity', w.get('level', '未知'))}\n"
                        f"类型: {w.get('typeName', w['type'])}\n"
                        f"发布时间: {w['pubTime']}\n"
                        f"生效时间: {w.get('startTime', '')} 至 {w.get('endTime', '')}\n"
                        f"内容: {w['text']}\n\n"
                    )
                return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"执行出错: {str(e)}")]

def main():
    """入口函数"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(run())

if __name__ == "__main__":
    main()