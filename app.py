from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from scrapper import submit_case_details
from case_details_collector import get_case_details
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import asyncio
import aiosqlite
from database import init_db, log_search_query, log_raw_response



app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# For Keeping track of driver sessions
URL ="https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no.php?state_cd=16&dist_cd=1&court_code=1&stateNm=Calcutta"

# Adding Startup code for the database to get initialized
@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Removing Old Orders PDF if they exits
    folder = "static/pdf"
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):  
                os.remove(file_path)
    return templates.TemplateResponse("Form.html",{"request":request})


@app.post("/search", response_class=HTMLResponse)
async def search_case(request: Request, case_type: str = Form(...), case_number: str = Form(...), year: str = Form(...)):
    # Details
    print(f" Case Type: {case_type}, Case Number: {case_number}, Year: {year}")

    # Log the search query
    query_id = await log_search_query(case_type, case_number, year, success=False)

    # Passing this data to the scrapper
    # this will get the details and save it in html file for further processing
    response_message = await submit_case_details(URL,case_type, case_number, year)
    
    if response_message=="Success":
        # Getting Details
        result = await get_case_details()

         # Reading the raw HTML content
        with open("scrapped_page/case_details.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Loging the successful response
        await log_raw_response(query_id, html_content, result)
        
        # Updating the query success status
        async with aiosqlite.connect('court_cases.db') as db:
            await db.execute("UPDATE search_queries SET success = ? WHERE id = ?", (True, query_id))
            await db.commit()

        return templates.TemplateResponse("result.html", {"request": request, "result": result})
    
    elif response_message=="Invalid":
        # Response for invalid details
        return templates.TemplateResponse("invalid_details.html",{"request":request})
    
    else:
        # Show error page when response is False
        return templates.TemplateResponse("error_page.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
