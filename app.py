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

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# For Keeping track of driver sessions
URL ="https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no.php?state_cd=16&dist_cd=1&court_code=1&stateNm=Calcutta"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("Form.html",{"request":request})


@app.post("/search", response_class=HTMLResponse)
async def search_case(request: Request, case_type: str = Form(...), case_number: str = Form(...), year: str = Form(...)):
    # Details
    print(f" Case Type: {case_type}, Case Number: {case_number}, Year: {year}")

    # Passing this data to the scrapper
    # this will get the details and save it in html file for further processing
    await submit_case_details(URL,case_type, case_number, year)

    # Getting Details
    result = await get_case_details()
    return templates.TemplateResponse("result.html", {"request": request, "result": result})



if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
