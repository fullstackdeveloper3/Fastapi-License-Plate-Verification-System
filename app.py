from time import strftime, strptime, localtime, time
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
db = SQL("sqlite:///anpr.db")

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
    data.plate = normalized(data.plate)

    # Check whether the license plate exists in the database
    # Determine whether a vehicle owner was found
    check = db.execute("SELECT * from users WHERE id = (SELECT owner_user_id as n FROM vehicles WHERE plate_normalized = ?)", data.plate)

    if check:
        # Check whether the user has an administrator or private role
        if check[0]["role"] in ["admin", "private"]:
            # Return the user's role
            return check[0]["role"]

        # Retrieve the user's membership information
        member = db.execute("SELECT * from memberships WHERE user_id = ?", check[0]["id"])

        # Convert membership date strings into datetime objects
        member[0]["starts_at"] = strptime(member[0]["starts_at"], "%Y-%m-%d %H:%M:%S")
        member[0]["expires_at"] = strptime(member[0]["expires_at"], "%Y-%m-%d %H:%M:%S")

        # Check whether the current time falls within the membership period
        if(member[0]["starts_at"] <= localtime(time()) and localtime(time()) <= member[0]["expires_at"]):
            return "True"

        return "False"
        
    return "False"

# Remove non-alphanumeric characters from the license plate
def normalized(plate: str) -> str:
    word = ""
    for i in plate:
        if (i.isalnum()):
            word += i
    return word.upper()
