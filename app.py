from time import strftime
from cs50 import SQL

# Import FastAPI to create the application and define API endpoints
from fastapi import FastAPI

# Import PlainTextResponse to return responses as plain text instead of JSON
from fastapi.responses import PlainTextResponse

# Import BaseModel to define and validate the structure of incoming request data
from pydantic import BaseModel



# Initialize the FastAPI application
app = FastAPI()

# Initialize the database connection
db = SQL("sqlite:///fiftyville.db")

# Define the expected structure of the incoming JSON request body
# The request must contain a "plate" field whose value is a string
class PlateRequest(BaseModel):
    plate: str

# Define a GET endpoint at the root URL to return a default message
@app.get("/", response_class=PlainTextResponse)
def index():
    return "Todo"

# Define a POST endpoint at the root URL to process a license plate
@app.post("/", response_class=PlainTextResponse)
def checking(data: PlateRequest):

    # Sanitize the license plate number
    data.plate = remove(data.plate)

    # Check whether the license plate exists in the database
    check = db.execute("SELECT COUNT(license_plate) as n FROM bakery_security_logs WHERE license_plate = ?", data.plate)

    # Determine whether the license plate was found
    if(check[0]['n']):

        # Record the license plate entry in the history table
        db.execute("INSERT INTO history(plate,  direction, time) VALUES(?, ?, ?)", data.plate, "in", strftime("%Y/%m/%d %H:%M:%S"))
        return "True"

    return "False"

# Remove non-alphanumeric characters from the license plate
def remove(plate: str) -> str:
    word = ""
    for i in plate:
        if (i.isalnum()):
            word += i
    return word.upper()
