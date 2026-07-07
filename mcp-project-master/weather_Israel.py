from mcp.server.fastmcp import FastMCP
from playwright.async_api import TimeoutError as PlaywrightTimeout
from playwright.async_api import async_playwright

FORECAST_URL = "https://www.weather2day.co.il/forecast"


# create the server
mcp = FastMCP("weather-Israel")

# global variables to store browser state
browser_instance = None
context_instance = None
page_instance = None

@mcp.tool()
async def open_weather_forecast_israel():
    """Open a browser and navigate to the weather2day forecast page."""
    global browser_instance, page_instance
    
    pw = await async_playwright().start()
    # headless=False lets you see the browser during development
    browser_instance = await pw.chromium.launch(headless=False)
    page_instance = await browser_instance.new_page()
    
    await page_instance.goto(FORECAST_URL)
    return "הדפדפן נפתח באתר weather2day"

@mcp.tool()
async def enter_weather_forecast_city_israel(city_name: str):
    """Click the search field to focus it, then type the city name."""
    global page_instance
    
    # check if the browser is open before trying to type
    if not page_instance:
        return "שגיאה: הדפדפן לא פתוח. המערכת תנסה לפתוח אותו כעת."
    
    search_id = "#city_search_forecast" # ה-ID המדויק מהתמונה ששלחת
    
    try:
        # ודואים שהאלמנט גלוי וזמין ללחיצה
        await page_instance.wait_for_selector(search_id, state="visible", timeout=5000)
        
        # לחיצה אקטיבית על השדה כדי להבטיח פוקוס (השלב הקריטי שזיהית)
        await page_instance.click(search_id)
        
        # ניקוי תוכן קודם אם קיים
        await page_instance.fill(search_id, "")
        
        # הקלדה איטית שמדמה משתמש אנושי כדי להפעיל את ה-Autocomplete של האתר
        await page_instance.type(search_id, city_name, delay=150)
        
        # המתנה קצרה כדי לאפשר לרשימה להיפתח
        await page_instance.wait_for_timeout(2000)
        
        return f"הקלדתי '{city_name}' בשדה החיפוש. כעת ניתן לבחור מהרשימה."
        
    except Exception as e:
        return f"נכשלה הפעולה בשדה החיפוש: {str(e)}"
    

@mcp.tool()
async def select_weather_forecast_city_israel():
    """Select the first result from the opened autocomplete list."""
    global page_instance
    if not page_instance:
        return "Error: browser is not open."
    
    # selector for the first item in the autocomplete suggestion list
    list_item_selector = "#city_search_forecastautocomplete-list div"
    
    try:
        # wait for the list to become visible and clickable
        await page_instance.wait_for_selector(list_item_selector, timeout=5000)
        await page_instance.click(list_item_selector)
        return "City selected successfully from the list."
    except:
        # fallback: if the list did not open, try pressing Enter in the search field
        await page_instance.press("#city_search_forecast", "Enter")
        return "Search executed using Enter as a fallback."

@mcp.tool()
async def get_weather_data_israel():
    """Extract forecast data from the open page and return it as text for the LLM."""
    global page_instance
    if not page_instance:
        return "Error: no page is open. Navigate to a specific city first."
    
    try:
        # brief wait to make sure the data has loaded after selecting from the list
        await page_instance.wait_for_timeout(2000)
        
        # extract the page title to confirm we are on the correct city page
        title = await page_instance.title()
        
        # get the text from the forecast area; use a selector that targets the main content
        # on weather2day, the forecast region is typically within elements like forecast-wrap or weekly-forecast
        weather_element = await page_instance.locator("body").inner_text()
        
        # basic cleanup - reduce multiple spaces so the LLM doesn't receive unnecessary text
        clean_text = " ".join(weather_element.split())
        
        # return only part of the text (e.g. first 2000 characters) to stay within token limits
        return f"Site data for {title}:\n{clean_text[:2000]}"
        
    except Exception as e:
        return f"Error extracting data from the page: {str(e)}"

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
