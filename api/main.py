from fastapi import FastAPI, HTTPException
from api.state import get_driver_options, get_all_options
from api.consumer import start_consumer_thread

app = FastAPI(title="LiveF1Strategy API")


# Start Kafka consumer thread at startup
@app.on_event("startup")
def startup_event():
    start_consumer_thread()


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/drivers/{driver_number}/options")
def driver_options(driver_number: int):
    opts = get_driver_options(driver_number)
    if not opts:
        raise HTTPException(status_code=404, detail="No options for driver")
    return opts


@app.get("/session/options")
def session_options():
    return get_all_options()
