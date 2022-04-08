class Measurement:
    def __init__(self, Value, EntryDate, DeletedAt):
        self.Value = Value
        self.EntryDate = EntryDate
        self.DeletedAt = DeletedAt

    def key_func(e):
        return e.EntryDate

    def get_entry_date(self):
        return self.EntryDate[:10]
    
    def get_entry_time(self):
        #2020-12-11T19:22:00
        return self.EntryDate[11:16]

    def get_deletion_date(self):
        return self.EntryDate[:10]

class GlucoseMeasurements(Measurement):
    def __init__(self, Value, EntryDate, DeletedAt, MealType, MeterDeviceEntryDate):
        super().__init__(Value, EntryDate, DeletedAt)
        self.MealType = MealType
        self.MeterDeviceEntryDate = MeterDeviceEntryDate


class PhysicalActivities(Measurement):
    def __init__(self, Value, EntryDate, DeletedAt, Type, Intensity):
        super().__init__(Value, EntryDate, DeletedAt)
        self.Type = Type
        self.Intensity = Intensity


class Meals(Measurement):
    def __init__(self, Value, EntryDate, DeletedAt, Details, Calorie, Fat, Protein):
        super().__init__(Value, EntryDate, DeletedAt)
        self.Details = Details
        self.Calorie = Calorie
        self.Fat = Fat
        self.Protein = Protein


class MedicineIntakes(Measurement):
    def __init__(self, Value, EntryDate, DeletedAt, Medicine):
        super().__init__(Value, EntryDate, DeletedAt)
        self.Medicine = Medicine


class Feels(Measurement):
    def __init__(self, Value, EntryDate, DeletedAt, Note, FeelTypes):
        super().__init__(Value, EntryDate, DeletedAt)
        self.Note = Note
        self.FeelTypes = FeelTypes
