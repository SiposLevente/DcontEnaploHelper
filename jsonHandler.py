import json
from os.path import exists
from enum import Enum


class Data_types(Enum):
    Profile, Addresses, Notificaitons, GlucoseMeasurements, PhysicalActivities, Meals, MedicineIntakes, Feels, Therapy, SupervisedPatients, Supervisors, MeterDevices, Medicines, Articles, ClinicDoctors, GlucoseRanges, Conversations = range(
        0, 17)


# Returns a json object
def open_json(file_path):
    if exists(file_path):
        file = open(file_path)
        loaded_json = json.load(file)
        file.close()
        return loaded_json
    else:
        exit("Failed to read data!")


# Returns a list from a given json object, based on the data type
def get_data(data_type):
    loaded_json = open_json("./data/data.json")
    if data_type == Data_types.Profile:
        return loaded_json["Profile"]
    else:
        return list_from_data(loaded_json[data_type.name])


# Creates a list from a given type.
def list_from_data(data):
    data_list = list()
    for i in data:
        data_list.append(i)
    return data_list
