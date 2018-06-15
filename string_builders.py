def unifyDriveTrainString(drivetrainStr, make):
    if drivetrainStr == "All Wheel Drive":
        drivetrainStr = "AWD"
    elif drivetrainStr == "Front Wheel Drive":
        drivetrainStr = "FWD"
    elif drivetrainStr == "Rear Wheel Drive":
        drivetrainStr = "RWD"

    if make == "Audi":
        drivetrainStr = ""

    return drivetrainStr


def unifyDoorStr(doorStr, bodyStr):
    # Because all Sedans have 4 doors:
    if bodyStr == "Sedan":
        doorStr = ""
    else:
        doorStr = doorStr+"-door "

    return doorStr


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
        drivetrainStr = unifyDriveTrainString(drivetrainStr, parameters['make'])

    if len(cylinders) > 1:
        cylStr = parameters["cylinder"]+"-cylinder "

    if len(transmissions) > 1:
        transmissonStr = parameters["transmission"]+" "

    if len(doors) > 1:
        doorStr = parameters["doors"]
        doorStr = unifyDoorStr(doorStr, bodyStr)

    if len(engine_types) > 1:
        engineTypeStr = parameters["engine_type"]+" "

    trimString = trimStr+bodyStr+bodySubStr+drivetrainStr+cylStr+transmissonStr+doorStr+engineTypeStr

    if trimString == "":
        if parameters["trim"] != "":
            trimString = parameters["trim"]
        else:
            trimString = parameters["model"]

    return trimString.strip()