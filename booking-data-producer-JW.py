from faker import Faker
from collections import defaultdict
import random
import requests
import json

def authHeader():
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJKdXN0aW4tRXZhbnM3ODAwIiwiZXhwIjoxNjM4ODYzNjc1LCJpYXQiOjE2Mzg4NDU2NzV9.sowxnfPU6S9Q6Am7LLAggzuSpdOBzQpPAcqEoooQ32xfoefxfJ1sEgQs-33JRFfh30zkGuGPLTfBY4Ul51MjBw"
    head = {'Authorization': 'Bearer ' + token}
    return head


def addBooking():
    faker = Faker()
    flights = requests.get("http://localhost:9001/flight", headers = authHeader())
    flightJSON = flights.json()
    flightList = []
    for f in range (len(flightJSON)):
        info = []
        info.append(flightJSON[f]["id"])
        flightList.append(info)
    numFlights = random.randint(1,4)
    flightsTaken = []
    for x in range(numFlights):
        randFlight = flightList[random.randint(0,len(flightList)-1)]
        flightsTaken.append(randFlight)

    passList = []
    numPass = random.randint(1,4)
    for x in range (numPass):
        passengers = defaultdict(list)
        genderOutput = random.randint(1,2)
        if(genderOutput ==1):
            passengers["given_name"].append(faker.first_name_male())
            passengers["gender"].append("male")
        else:
            passengers["given_name"].append(faker.first_name_female())
            passengers["gender"].append("female")

        passengers["family_name"].append(faker.last_name())
        passengers["dob"].append(str(faker.date_of_birth()))
        passengers["address"].append(faker.street_address())
        passList.append(passengers)
    stripe = defaultdict(list)
    stripe["stripeId"].append("stripe" + str(random.randint(1000,9999)))

    bookingInsert = defaultdict(list)
    bookingInsert["payment"].append(stripe)
    bookingInsert["flightIds"].append(flightsTaken)
    bookingInsert["passengers"].append(passList)
    bookingJSON = json.dumps(bookingInsert)
    bookingJSON = bookingJSON.replace("[", "")
    bookingJSON = bookingJSON.replace("]","")
    bookingJSON = bookingJSON.replace("tIds\": ","tIds\": [")
    bookingJSON = bookingJSON.replace(", \"passengers\": ","] , \"passengers\": [")
    bookingJSON = bookingJSON.replace("}}", "}]}")
    finalinput = json.loads(bookingJSON)
    response = requests.post("http://localhost:9003/booking", json=finalinput, headers = authHeader())
    

for x in range(10):
    addBooking()