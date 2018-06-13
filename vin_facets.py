import requests
import json
import xlsxwriter


def buildTrimString(trims,body_types,body_subtypes,drivetrains,cylinders,transmissions,doors,engine_types,parameters):
    trimStr = ""
    bodyStr = ""
    bodySubStr = ""
    drivetrainStr = ""
    cylStr = ""
    transmissonStr = ""
    doorStr = ""
    engineTypeStr = ""


    if len(trims)>1:
        trimStr = parameters["trim"]+" "

    if len(body_types)>1:
        bodyStr = parameters["body_type"]+" "

    if len(body_subtypes)>1:
        bodySubStr = parameters["body_subtype"]+" "

    if len(drivetrains) > 1:
        drivetrainStr = parameters["drivetrain"]+" "

    if len(cylinders) > 1:
        cylStr = parameters["cylinder"]+"-cylinder "

    if len(transmissions) > 1:
        transmissonStr = parameters["transmission"]+" "

    if len(doors) > 1:
        doorStr = parameters["doors"]+"-door "

    if len(engine_types) > 1:
        engineTypeStr = parameters["engine_type"]+" "


    trimString = trimStr+bodyStr+bodySubStr+drivetrainStr+cylStr+transmissonStr+doorStr+engineTypeStr
    return trimString.strip()

base_url = "https://marketcheck-prod.apigee.net/v1/search"
api_key = "aFHqYBK7moVJZN89peNCLNLKRnNN5Lxi"
latitude = 38.783207
longitude = -95.920740
radius = 3000000

# For year in years:
year = 2015
# Get all brands
# For brand in brands:
make = "Audi"
# 	Get all models
model = "A4"
# 	For model in models:

parameters = {"api_key": api_key,
              "latitude": latitude,
              "longitude": longitude,
              "radius": radius,
              "year": year,
              "make": make,
              "model": model,
              "rows": 1,
              "facets": "trim,body_type,body_subtype,drivetrain,cylinders,transmission,doors,engine_type"
              }

# response = requests.get("https://marketcheck-prod.apigee.net/v1/search?api_key=aFHqYBK7moVJZN89peNCLNLKRnNN5Lxi&latitude=38.783207&longitude=-95.920740&radius=300000&year=2015&make=Audi&model=A4&rows=1&facets=trim%2Cbody_type%2Cbody_subtype%2Cdrivetrain%2Ccylinders%2Ctransmission%2Cdoors%2Cengine_type")
response = requests.get(base_url, params=parameters)
data = response.json()

facets = data["facets"]

trims = facets["trim"]
if not trims:
    trims = [{"item": ""}]

body_types = facets["body_type"]
if not body_types:
    body_types = [{"item": ""}]

body_subtypes = facets["body_subtype"]
if not body_subtypes:
    body_subtypes = [{"item": ""}]

drivetrains = facets["drivetrain"]
if not drivetrains:
    drivetrains = [{"item": ""}]

cylinders = facets["cylinders"]
if not cylinders:
    cylinders = [{"item": ""}]

transmissions = facets["transmission"]
if not transmissions:
    transmissions = [{"item": ""}]

doors = facets["doors"]
if not doors:
    doors = [{"item": ""}]

engine_types = facets["engine_type"]
if not engine_types:
    engine_types = [{"item": ""}]

for trim in trims:
    for body_type in body_types:
        for body_subtype in body_subtypes:
            for drivetrain in drivetrains:
                for cylinder in cylinders:
                    for transmission in transmissions:
                        for door in doors:
                            for engine_type in engine_types:
                                parameters = {"api_key": api_key,
                                              "latitude": latitude,
                                              "longitude": longitude,
                                              "radius": radius,
                                              "year": year,
                                              "make": make,
                                              "model": model,
                                              "rows": 30,
                                              "trim": trim["item"],
                                              "body_type": body_type["item"],
                                              "body_subtype": body_subtype["item"],
                                              "drivetrain": drivetrain["item"],
                                              "cylinder": cylinder["item"],
                                              "transmission": transmission["item"],
                                              "doors": door["item"],
                                              "engine_type": engine_type["item"],
                                              }
                                response = requests.get(base_url, params=parameters)
                                data = response.json()

                                VINs = []
                                if len(data["listings"]) > 0:
                                    for listing in data["listings"]:
                                        currVIN = listing["vin"][0:8]
                                        # currVIN = replace_str_index(currVIN, 8, 'x')
                                        VINs.append(currVIN)

                                    if all(Vin == VINs[0] for Vin in VINs):
                                        VIN_use = VINs[0]
                                    else:
                                        # determine which VIN is correct and use that
                                        print("not all entries equal!!!")

                                    VinEntry = {}
                                    VinEntry["Year"] = year
                                    VinEntry["Make"] = make
                                    VinEntry["Model"] = model
                                    VinEntry["bR_trim"] = buildTrimString(trims,body_types,body_subtypes,drivetrains,cylinders,transmissions,doors,engine_types,parameters)
                                    VinEntry["VIN_1_3"] = VIN_use[0:2]
                                    VinEntry["VIN_4_7"] = VIN_use[3:6]
                                    VinEntry["VIN_8"] = VIN_use[7]




