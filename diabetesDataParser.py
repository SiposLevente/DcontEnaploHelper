import json
from jsonHandler import Data_types, get_data
from classes.profile import Profile
from classes.measurement import GlucoseMeasurements, PhysicalActivities, Meals, MedicineIntakes, Feels, Measurement


def sort_key(e):
    return e["EntryDate"]


def get_measurements(data_type):
    data_list = get_data(data_type)
    data_list.sort(key=sort_key)
    measurement_list = list()
    prev_entry_date = ""
    for data in data_list:
        if prev_entry_date != data["EntryDate"] and data["DeletedAt"] == None:
            if data_type == Data_types.GlucoseMeasurements:
                measurement_list.append(GlucoseMeasurements(
                    data["Value"], data["EntryDate"], data["DeletedAt"], data["MealType"], data["MeterDeviceEntryDate"]))
            elif data_type == Data_types.PhysicalActivities:
                measurement_list.append(PhysicalActivities(
                    data["Value"], data["EntryDate"], data["DeletedAt"], data["Type"], data["Intensity"]))
            elif data_type == Data_types.Meals:
                measurement_list.append(Meals(data["Value"], data["EntryDate"], data["DeletedAt"],
                                        data["Details"], data["Calorie"], data["Fat"], data["Protein"]))
            elif data_type == Data_types.MedicineIntakes:
                measurement_list.append(MedicineIntakes(
                    data["Value"], data["EntryDate"], data["DeletedAt"], data["Medicine"]))
            elif data_type == Data_types.Feels:
                measurement_list.append(Feels(
                    data["Value"], data["EntryDate"], data["DeletedAt"], data["Note"], data["FeelTypes"]))
            else:
                exit("Error! Invalid data type")
        prev_entry_date = data["EntryDate"]
    return measurement_list


def get_profile():
    profile_data = get_data(Data_types.Profile)
    addresses_data = get_data(Data_types.Addresses)
    meter_devices_data = get_data(Data_types.MeterDevices)
    medicines_data = get_data(Data_types.Medicines)
    ranges_data = get_data(Data_types.GlucoseRanges)
    return Profile(profile_data["Email"], profile_data["Lastname"], profile_data["Firstname"], profile_data["DateOfBirth"], profile_data["CreatedAt"], profile_data["Sex"], profile_data["ConnectionToken"], profile_data["DiabetesType"], profile_data["DiagnosisYear"], addresses_data, meter_devices_data, medicines_data, ranges_data)
