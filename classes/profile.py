from datetime import date


class Profile:
    def __init__(self, Email, Lastname, Firstname, DateOfBirth, CreatedAt, Sex, ConnectionToken, DiabetesType, DiagnosisYear, Addresses, MeterDevices, Medicines, GlucoseRanges):
        self.Email = Email
        self.Lastname = Lastname
        self.Firstname = Firstname
        self.DateOfBirth = DateOfBirth
        self.CreatedAt = CreatedAt
        self.Sex = Sex
        self.ConnectionToken = ConnectionToken
        self.DiabetesType = DiabetesType
        self.DiagnosisYear = DiagnosisYear
        self.Addresses = Addresses
        self.MeterDevices = MeterDevices
        self.Medicines = Medicines
        self.GlucoseRanges = GlucoseRanges

    def get_age(self):
        year = int(self.DateOfBirth[:4])
        month = int(self.DateOfBirth[5:7])
        day = int(self.DateOfBirth[8:10])
        dob = date(year, month, day)
        return int((date.today() - dob).days/365)