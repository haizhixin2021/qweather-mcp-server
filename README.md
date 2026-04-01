# 和风天气 MCP Server

English | [中文](#中文说明)

A Model Context Protocol (MCP) server for QWeather (和风天气) API, enabling AI assistants to query real-time weather, forecasts, air quality, and weather warnings.

## ✨ Features

- 🔍 **City Search** - Search for cities and get location IDs for weather queries
- 🌤️ **Real-time Weather** - Get current weather conditions including temperature, humidity, wind, and more
- 📊 **Weather Forecast** - Get 3-day or 7-day weather forecasts
- 🌫️ **Air Quality** - Get real-time AQI, PM2.5, PM10, and other air quality metrics
- 🚨 **Weather Warnings** - Get weather disaster warnings (typhoons, rainstorms, heat waves, etc.)

## 🚀 Quick Start

### 1. Get Your API Key

1. Visit [QWeather Developer Platform](https://dev.qweather.com/)
2. Register and create an application
3. Get your API Key from the console

### 2. Configuration

Add the following configuration to your MCP client:

```json
{
  "mcpServers": {
    "qweather": {
      "command": "uvx",
      "args": ["qweather-mcp-server"],
      "env": {
        "QWEATHER_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or use pip installation:

```bash
pip install qweather-mcp-server
```

Then configure:

```json
{
  "mcpServers": {
    "qweather": {
      "command": "python",
      "args": ["-m", "qweather_mcp"],
      "env": {
        "QWEATHER_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### 3. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `QWEATHER_API_KEY` | ✅ Yes | - | Your QWeather API Key |
| `QWEATHER_API_URL` | No | `https://devapi.qweather.com` | QWeather API base URL |

#### Custom API Endpoint (Optional)

If you need to use a custom API endpoint (e.g., for paid plans or enterprise accounts), set `QWEATHER_API_URL`:

```json
{
  "mcpServers": {
    "qweather": {
      "command": "uvx",
      "args": ["qweather-mcp-server"],
      "env": {
        "QWEATHER_API_KEY": "your-api-key-here",
        "QWEATHER_API_URL": "https://api.qweather.com"
      }
    }
  }
}
```

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `search_city` | Search for cities by name (Chinese, Pinyin, or English) and get location IDs |
| `get_current_weather` | Get real-time weather for a location |
| `get_weather_forecast` | Get 3-day or 7-day weather forecast |
| `get_air_quality` | Get air quality index and pollutant levels |
| `get_weather_warning` | Get active weather disaster warnings |

> ⚠️ **API Deprecation Notice**: 
> - Air Quality API (`/v7/air/now`) will be deprecated on 2026-06-01
> - Weather Warning API (`/v7/warning/now`) will be deprecated on 2026-10-01
> 
> This server supports both legacy (v7) and new (v1) Weather Alert API. For best results, provide latitude and longitude when querying weather warnings.

## 📖 Usage Examples

### Search for a City
```
User: 搜索北京
AI: 找到以下城市：
1. 北京市 北京市 北京
   ID: 101010100
   坐标: 39.90498, 116.40528
```

### Get Current Weather
```
User: 查询北京现在的天气
AI: 🌤️ 实时天气

观测时间: 2025-04-01T14:00+08:00
温度: 18°C (体感 16°C)
天气: 晴
风向: 北风 3级 (12km/h)
湿度: 45%
气压: 1015hPa
能见度: 10km
降水量: 0mm
```

### Get Weather Forecast
```
User: 北京未来3天天气预报
AI: 📊 3天天气预报

📅 2025-04-01
   白天: 晴 22°C
   夜间: 晴 12°C
   风向: 北风 3级
   湿度: 45% 降水概率: 0%
...
```

### Get Air Quality
```
User: 北京空气质量怎么样
AI: 🌫️ 空气质量指数

AQI: 65 (良)
PM2.5: 45 μg/m³
PM10: 78 μg/m³
NO₂: 32 μg/m³
SO₂: 8 μg/m³
CO: 0.8 mg/m³
O₃: 89 μg/m³
主要污染物: PM2.5
```

### Get Weather Warnings
```
User: 北京有天气预警吗
AI: ✅ 当前无天气灾害预警
```

## 🔧 Development

```bash
# Clone the repository
git clone https://github.com/your-username/qweather-mcp-server.git
cd qweather-mcp-server

# Install dependencies
pip install -e .

# Set environment variables
export QWEATHER_API_KEY="your-api-key"
# Optional: custom API endpoint
# export QWEATHER_API_URL="https://api.qweather.com"

# Run the server
python src/qweather_mcp/server.py
```

### Debug with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python src/qweather_mcp/server.py
```

## 📝 Requirements

- Python >= 3.10
- MCP >= 1.8.1
- httpx >= 0.27.0

## 📄 License

MIT License

---

## 中文说明

一个基于 Model Context Protocol (MCP) 的和风天气 API 服务，让 AI 助手能够查询实时天气、天气预报、空气质量和天气预警。

### 功能特性

- 🔍 **城市搜索** - 搜索城市并获取城市ID
- 🌤️ **实时天气** - 获取当前天气状况，包括温度、湿度、风向风力等
- 📊 **天气预报** - 获取3天或7天天气预报
- 🌫️ **空气质量** - 获取实时AQI、PM2.5、PM10等空气质量指标
- 🚨 **天气预警** - 获取台风、暴雨、高温等天气灾害预警

### 快速开始

1. 前往[和风天气开发平台](https://dev.qweather.com/)注册并获取 API Key
2. 在 MCP 客户端中添加配置：

```json
{
  "mcpServers": {
    "qweather": {
      "command": "uvx",
      "args": ["qweather-mcp-server"],
      "env": {
        "QWEATHER_API_KEY": "你的API密钥"
      }
    }
  }
}
```

### 环境变量说明

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `QWEATHER_API_KEY` | ✅ 是 | - | 和风天气 API Key |
| `QWEATHER_API_URL` | 否 | `https://devapi.qweather.com` | 和风天气 API 地址 |

#### 自定义 API 地址（可选）

如果您使用付费版或企业版，可以自定义 API 地址：

```json
{
  "mcpServers": {
    "qweather": {
      "command": "uvx",
      "args": ["qweather-mcp-server"],
      "env": {
        "QWEATHER_API_KEY": "你的API密钥",
        "QWEATHER_API_URL": "https://api.qweather.com"
      }
    }
  }
}
```

> ⚠️ **API 弃用通知**: 
> - 空气质量 API (`/v7/air/now`) 将于 2026-06-01 弃用
> - 天气预警 API (`/v7/warning/now`) 将于 2026-10-01 弃用
> 
> 本服务同时支持旧版 (v7) 和新版 (v1) 天气预警 API。建议在查询预警时提供经纬度坐标以使用新版 API。

### 支持的客户端

- Cherry Studio
- Claude Desktop
- Cursor
- Cline
- 其他支持 MCP 协议的客户端
