from fastapi import FastAPI
from pathlib import Path
from fastapi import HTTPException
from python_foundations.reporting import process_all_sites
from python_foundations.lesson06 import load_sites
from api.schemas import SiteResponse, SummaryResponse

app = FastAPI()

def get_monitoring_report() -> dict:
    # determine project root
    project_root = Path(__file__).resolve().parent.parent

    # construct path to data/sites.json
    data_path = project_root / "data" / "sites.json"

    # call load_sites to load json records
    records = load_sites(data_path)

    # Check that loading succeeded and that the returned value is a list.
    if records is None:
        raise HTTPException(
            status_code = 500,
            detail = "Unable to load site monitoring data"
        )

    if not isinstance(records, list):
        raise HTTPException(
            status_code=500,
            detail="Site monitoring data must be a list"
        )

    # Pass records to process_all_sites
    report = process_all_sites(records)

    # return complete monitoring report dictionary
    return report

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/sites", response_model=list[SiteResponse])
def get_sites():
    report = get_monitoring_report()
    return report['sites']

@app.get("/summary", response_model=SummaryResponse)
def get_summary():
    report = get_monitoring_report()

    # return a dictionary conatining only the counters
    return {
        key: value for key, value in report.items() if key not in ("sites", "errors")
    }
