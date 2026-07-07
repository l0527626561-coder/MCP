# Israel Weather MCP Agent 🌦️

An autonomous AI Agent powered by the **Model Context Protocol (MCP)** that provides real-time weather information for cities in Israel. 

The agent uses **Playwright** for browser automation and implements a **RAG (Retrieval-Augmented Generation)** flow to extract live data from weather websites and provide accurate, context-aware answers directly in the chat.

## 🚀 Features
- **Real-time Data:** Fetches live weather updates from `weather2day.co.il`.
- **Browser Automation:** Automates searching, selecting cities, and navigating weather pages.
- **RAG Integration:** Extracts page content and provides it to the LLM to answer specific user queries.
- **Autonomous Tool Use:** The agent intelligently chains multiple tools (Open -> Search -> Select -> Extract) to fulfill a single request.

## 🛠️ Built With
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- [Playwright](https://playwright.dev/) (Browser Automation)
- [Anthropic Claude API](https://www.anthropic.com/api)
- [uv](https://github.com/astral-sh/uv) (Python Package & Project Manager)

## 📋 Prerequisites
- Python 3.10 or higher.
- `uv` installed on your machine.
- An Anthropic API Key with active credits.

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME
   ```
2. **Install Dependencies:**

  ```bash
   uv sync
   ```
3. **Configure Environment Variables:**
Set your Anthropic API key in your terminal (PowerShell example):

```bash
$env:ANTHROPIC_API_KEY = "your-api-key-here"
```
4. **Run the Agent:**

```bash
uv run host.py
```

## 💬 Usage Examples
Once the agent is running, you can ask questions like:

- "What is the weather in Bnei Brak right now?"
- "Give me the temperature in Jerusalem."
- "Open the weather site, search for Haifa, and tell me the humidity levels."

## 🧩 Tools Included
- `open_weather_forecast_israel`: Opens the weather website.
- `enter_weather_forecast_city_israel`: Types the city name into the search bar with active focus.
- `select_weather_forecast_city_israel`: Selects the correct city from the autocomplete list.
- `get_weather_data_israel`: Extracts the weather text from the page for the LLM to analyze.

---
Created by Michal. Code. Create. Innovate.