import requests
import json
import openpyxl
from collections import Counter
import operator
from openpyxl import Workbook, load_workbook
from string_builders import *


def get_models(base_url, parameters):
    response = requests.get(base_url, params=parameters)
    data = response.json()
    facets = data["facets"]
    models = facets["model"]
    return models


def get_trims(base_url, parameters):
    response = requests.get(base_url, params=parameters)
    data = response.json()
    facets = data["facets"]
    trims = facets["trim"]
    return trims


call_counter = 0
base_url = "https://marketcheck-prod.apigee.net/v1/search"
api_key = "aFHqYBK7moVJZN89peNCLNLKRnNN5Lxi"
latitude = 38.783207
longitude = -95.920740
radius = 3000000

make = "Honda"

wb = load_workbook(make+'.xlsx')
ws = wb['Sheet1']

# years = range(1999, 2020)
# years = range(2002, 2020)
years = [2015]
for year in years:
    # Get all models
    parameters = {"api_key": api_key,
                  "latitude": latitude,
                  "longitude": longitude,
                  "radius": radius,
                  "year": year,
                  "make": make,
                  "rows": 1,
                  "facets": "model"
                  }
    models = get_models(base_url, parameters)

    for model in models:
        model = model["item"]
        print("num_calls: " + str(call_counter))
        print(str(year)+" "+make+" "+model)

        parameters = {"api_key": api_key,
                      "latitude": latitude,
                      "longitude": longitude,
                      "radius": radius,
                      "year": year,
                      "make": make,
                      "model": model,
                      "rows": 1,
                      "facets": "trim"
                      }

        trims = get_trims(base_url, parameters)

        for trim in trims:
            trim = trim["item"]

            parameters = {"api_key": api_key,
                          "latitude": latitude,
                          "longitude": longitude,
                          "radius": radius,
                          "year": year,
                          "make": make,
                          "model": model,
                          "trim": trim,
                          "rows": 1,
                          "facets": "trim,body_type,body_subtype,drivetrain,cylinders,transmission,doors,engine_type"
                          }

            response = requests.get(base_url, params=parameters)
            call_counter += 1
            if response.status_code != 200:
                VinEntry_4Excel = [year, make, model,
                                   "Entire model",
                                   response.status_code, response.status_code, response.status_code]

                ws.append(VinEntry_4Excel)

            else:
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
                else:
                    # Remove entries that indicate a single cylinder (Audi issue)
                    singleCylIndex = next((index for (index, d) in enumerate(cylinders) if d["item"] == "1"), None)
                    if singleCylIndex:
                        del cylinders[singleCylIndex]

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
                                                call_counter += 1
                                                if response.status_code ==200:
                                                    data = response.json()

                                                    VINs = []
                                                    if len(data["listings"]) > 0:
                                                        for listing in data["listings"]:
                                                            currVIN = listing["vin"][0:8]
                                                            VINs.append(currVIN)

                                                        VinBuckets = Counter(VINs)
                                                        VIN_use = max(VinBuckets.items(), key=operator.itemgetter(1))[0]
                                                        num_occurrence = VinBuckets[VIN_use]
                                                        num_all = len(VINs)

                                                        # ActualCylinderBuckets = Counter(int(float(data["listings"]["build"]["cylinders"])))
                                                        # ActualCylinders = data["listings"][0]["build"]["cylinders"]

                                                        VinEntry = {}
                                                        VinEntry["Year"] = year
                                                        VinEntry["Make"] = make
                                                        VinEntry["Model"] = model
                                                        VinEntry["bR_trim"] = buildTrimString(trims,body_types,body_subtypes,drivetrains,cylinders,transmissions,doors,engine_types,parameters)
                                                        VinEntry["VIN_1_3"] = VIN_use[0:3]
                                                        VinEntry["VIN_4_7"] = VIN_use[3:7]
                                                        VinEntry["VIN_8"] = VIN_use[7]

                                                        VinEntry_4Excel = [VinEntry["Year"], VinEntry["Make"], VinEntry["Model"],
                                                                           VinEntry["bR_trim"], VinEntry["VIN_1_3"], VinEntry["VIN_4_7"],
                                                                           VinEntry["VIN_8"], num_occurrence, num_all ]
                                                    else:
                                                        VinEntry_4Excel = [year, make, model, buildTrimString(trims, body_types, body_subtypes, drivetrains, cylinders, transmissions, doors, engine_types, parameters), "DNF", "DNF", "DNF"]
                                                else:
                                                    VinEntry_4Excel = [year, make, model, buildTrimString(trims, body_types, body_subtypes, drivetrains, cylinders, transmissions, doors, engine_types, parameters), response.status_code, response.status_code, response.status_code]

                                                ws.append(VinEntry_4Excel)

    wb.save(make+".xlsx")

