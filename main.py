import tkinter as tk
from os import remove
from os.path import exists
from tkinter import messagebox
from PIL import ImageTk, Image
from classes.profile import *
from classes.measurement import *
from configHandler import *
from webParser import *
from diabetesDataParser import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasAgg, NavigationToolbar2Tk)


def set_displayed_profil(profile):
    username_stringvar.set(
        "Name: " + profile.Lastname + " " + profile.Firstname)
    if profile.Sex == 1:
        gender_stringvar.set("Gender: Male")
    elif profile.Sex == 0:
        gender_stringvar.set("Gender: Female")
    else:
        gender_stringvar.set("Gender: -")
    email_stringvar.set("Email: " + profile.Email)
    if profile.DateOfBirth != "":
        age_stringvar.set("Age: " + str(profile.get_age()))
    else:
        age_stringvar.set("Age: -")


def refresh():
    if get_login_status() == "0":
        login_error()
    else:
        result = get_dcont_data()
        if result == 0:
            messagebox.showinfo("Success", "Data updated succesfully!")
            tmp_profile = get_profile()
            set_displayed_profil(tmp_profile)
        else:
            error_message = "Unexpected error!"
            if result == 1:
                error_message = "Failed to load page!"
            elif result == 2:
                error_message = "Failed to log in!"
            elif result == 3:
                error_message = "Failed start data download!"
            elif result == 4:
                error_message = "Error", "Download failed!"

            messagebox.showerror("Error", error_message)


def log_in_out():
    if get_login_status() == "1":
        set_username("")
        set_password("")
        set_login_status("0")
        set_displayed_profil(
            Profile("-", "-", "", "", "-", "-", "-", "-", "-", "-", "-", "-", "-"))
        if(exists("./data/data.json")):
            remove("./data/data.json")
        login_button_var.set("Log in!")
        messagebox.showinfo("Info", "Logged out!")
    else:
        login_window = tk.Toplevel(main_window)
        login_window.geometry("270x140")
        login_window.title("Log in")
        username_lable = tk.Label(login_window, text="Username: ", width=15)
        username_lable.place(x=20, y=20)

        username_entry = tk.Entry(login_window, width=15)
        username_entry.place(x=115, y=20)

        password_lable = tk.Label(login_window, text="Password: ", width=15)
        password_lable.place(x=22, y=50)

        password_entry = tk.Entry(login_window, width=15, show="*")
        password_entry.place(x=115, y=50)

        log_in_button = tk.Button(login_window, text="Log in!", command=lambda: login(
            username_entry.get(), password_entry.get(), login_window))
        log_in_button.place(x=100, y=90)


def login(username, password, login_window):
    set_username(username)
    set_password(password)
    set_login_status("1")
    login_button_var.set("Log out!")
    refresh()
    login_window.destroy()


def plot_values(data_list):
    value_list = list()
    date_list = list()
    for i in data_list:
        date_list.append(i.EntryDate)
        value_list.append(i.Value)
    x = date_list
    y = value_list
    plt.plot(x,y)
    plt.xticks(rotation=25)
    plt.show()


def data_windows(data_type):
    if get_login_status() == "0":
        login_error()
    else:
        data_window = tk.Toplevel(main_window)
        data_window.geometry("625x483")

        close_button = tk.Button(
            data_window, text="Close!", width=5, height=2, command=data_window.destroy)
        if data_type == Data_types.GlucoseMeasurements:
            data_window.minsize(625, 483)
            data_window.maxsize(625, 483)
            close_button.place(x=550, y=425)
        elif data_type == Data_types.PhysicalActivities:
            data_window.maxsize(364, 550)
            data_window.minsize(364, 550)
            close_button.place(x=155, y=490)
        elif data_type == Data_types.Therapy:
            data_window.maxsize(650, 150)
            data_window.minsize(650, 150)
            close_button.place(x=290, y=90)
        else:
            data_window.maxsize(275, 550)
            data_window.minsize(275, 550)
            close_button.place(x=107, y=490)

        if data_type != Data_types.Therapy:
            listBox = tk.Listbox(data_window, height=20,
                                 width=30, font=(12), justify="center")
            data_list = get_measurements(data_type)
            data_list.reverse()
            counter = 0
            currdate = ""
        if data_type == Data_types.GlucoseMeasurements:
            heigh_range = int(profile.GlucoseRanges[0]["Max"])
            low_range = int(profile.GlucoseRanges[0]["Min"])

            day_counter = 0
            avarage_sum = 0
            avarage_counter = 0

            avarage_all = 0
            avarage_week = 0
            avarage_week_counter = 0
            avarage_14_day = 0
            avarage_14_day_counter = 0
            avarage_month = 0
            avarage_month_counter = 0
            avarage_2_month = 0
            avarage_2_month_counter = 0
            avarage_3_month = 0
            avarage_3_month_counter = 0

            for i in data_list:
                if currdate != i.get_entry_date():

                    currdate = i.get_entry_date()
                    listBox.insert(counter, " --------------- "+str(i.get_entry_date()
                                                                    ) + " --------------- ")
                    listBox.itemconfig(counter, bg="lightblue")
                    day_counter += 1
                    if day_counter == 7:
                        avarage_week = avarage_sum/avarage_counter
                        avarage_week_counter = avarage_counter
                    if day_counter == 14:
                        avarage_14_day = avarage_sum/avarage_counter
                        avarage_14_day_counter = avarage_counter
                    if day_counter == 30:
                        avarage_month = avarage_sum/avarage_counter
                        avarage_month_counter = avarage_counter
                    if day_counter == 60:
                        avarage_2_month = avarage_sum/avarage_counter
                        avarage_2_month_counter = avarage_counter
                    if day_counter == 90:
                        avarage_3_month = avarage_sum/avarage_counter
                        avarage_3_month_counter = avarage_counter
                    counter += 1

                value = i.Value
                avarage_sum += value
                listBox.insert(counter, str(i.get_entry_time()) +
                               "    " + str(value))

                if value > heigh_range:
                    listBox.itemconfig(counter, bg="orange", fg="white")
                elif value < low_range:
                    listBox.itemconfig(counter, bg="red", fg="white")
                else:
                    listBox.itemconfig(counter, bg="green", fg="white")
                avarage_counter += 1
                counter += 1
            avarage_all = avarage_sum/avarage_counter

            avarage_week_lable = tk.Label(data_window, text="7-day avareage glucose value: "+str(
                round(avarage_week, 1)) + " ("+str(avarage_week_counter)+" measurements)")
            avarage_week_lable.place(x=275, y=0)

            avarage_14_day_lable = tk.Label(data_window, text="14-day avareage glucose value: "+str(
                round(avarage_14_day, 1)) + " ("+str(avarage_14_day_counter)+" measurements)")
            avarage_14_day_lable.place(x=275, y=20)

            avarage_30_day_lable = tk.Label(data_window, text="30-day avareage glucose value: "+str(
                round(avarage_month, 1)) + " ("+str(avarage_3_month_counter)+" measurements)")
            avarage_30_day_lable.place(x=275, y=40)

            avarage_60_day_lable = tk.Label(data_window, text="60-day avareage glucose value: "+str(
                round(avarage_2_month, 1)) + " ("+str(avarage_2_month_counter)+" measurements)")
            avarage_60_day_lable.place(x=275, y=60)

            avarage_90_day_lable = tk.Label(data_window, text="90-day avareage glucose value: "+str(
                round(avarage_3_month, 1)) + " ("+str(avarage_3_month_counter)+" measurements)")
            avarage_90_day_lable.place(x=275, y=80)

            avarage_lable = tk.Label(data_window, text="All time avareage glucose value: "+str(
                round(avarage_all, 1)) + " ("+str(avarage_counter)+" measurements)")
            avarage_lable.place(x=275, y=100)

            graph_button = tk.Button(
                data_window, text="Glucose graph", width=10, height=2, command=lambda: plot_values(data_list))
            graph_button.place(x=290, y=425)

        elif data_type == Data_types.PhysicalActivities:
            listBox = tk.Listbox(data_window, height=20,
                                 width=40, font=(12), justify="center")
            toggler = True
            for i in data_list:
                if currdate != i.get_entry_date():
                    currdate = i.get_entry_date()
                    listBox.insert(counter, " --------------- "+str(i.get_entry_date()
                                                                    ) + " --------------- ")
                    listBox.itemconfig(counter, bg="lightblue")
                    counter += 1

                value = i.Value
                intensity = ""
                if i.Intensity == 3:
                    intensity = "heavy"
                elif i.Intensity == 2:
                    intensity = "medium"
                else:
                    intensity = "light"

                listBox.insert(counter, str(i.get_entry_time()) +
                               "    " + str(value) + " minutes")
                if toggler:
                    listBox.itemconfig(counter, bg="lightgrey")
                counter += 1
                listBox.insert(counter, "intensity: " +
                               intensity + ", type: " + i.Type)
                if toggler:
                    listBox.itemconfig(counter, bg="lightgrey")
                counter += 1
                listBox.insert(counter, "---------------")
                if toggler:
                    listBox.itemconfig(counter, bg="lightgrey")
                counter += 1
                toggler = not toggler
        elif data_type == Data_types.Meals or data_type == Data_types.MedicineIntakes:
            for i in data_list:
                if currdate != i.get_entry_date():
                    currdate = i.get_entry_date()
                    listBox.insert(counter, " --------------- "+str(i.get_entry_date()
                                                                    ) + " --------------- ")
                    listBox.itemconfig(counter, bg="lightblue")
                    counter += 1

                value = i.Value
                listBox.insert(counter, str(i.get_entry_time()) +
                               "    " + str(value))
                counter += 1
        elif data_type == Data_types.Feels:
            for i in data_list:
                if currdate != i.get_entry_date():
                    currdate = i.get_entry_date()
                    listBox.insert(counter, " --------------- "+str(i.get_entry_date()
                                                                    ) + " --------------- ")
                    listBox.itemconfig(counter, bg="lightblue")
                    counter += 1

                value = i.Note
                listBox.insert(counter, str(i.get_entry_time()) +
                               "    " + str(value))
                counter += 1
        elif data_type == Data_types.Therapy:
            data = get_profile()
            insulin = tk.Label(data_window, text="Insulin types:")
            insulin0 = tk.Label(
                data_window, text="Rapid acting: " + data.Medicines[0])
            insulin1 = tk.Label(
                data_window, text="Basis insulin: " + data.Medicines[1])
            ranges = tk.Label(data_window, text="Ranges:")
            ranges_min = tk.Label(
                data_window, text="Low: " + str(data.GlucoseRanges[0]["Min"]))
            ranges_max = tk.Label(
                data_window, text="High: " + str(data.GlucoseRanges[0]["Max"]))

            insulin.place(x=0, y=0)
            insulin0.place(x=40, y=20)
            insulin1.place(x=40, y=40)
            ranges.place(x=0, y=60)
            ranges_min.place(x=40, y=80)
            ranges_max.place(x=40, y=100)

        if data_type != Data_types.Therapy:
            listBox.place(x=0, y=0)


profile = Profile("-", "-", "", "-", "-", "-",
                  "-", "-", "-", "-", "-", "-", "-")
if get_login_status() == "1":
    profile = get_profile()


main_window = tk.Tk()
main_window.geometry("490x445")
main_window.title("Dcont enapló helper")
main_window.minsize(490, 445)
main_window.maxsize(490, 445)

canvas = tk.Canvas()
canvas.place(x=0, y=0)
img = ImageTk.PhotoImage(Image.open("./profile_picture/profile.png"))
canvas.create_image(140, 140, image=img)

username_stringvar = tk.StringVar()
username_lable = tk.Label(main_window,  textvariable=username_stringvar)
username_lable.place(x=20, y=270)
username_stringvar.set("Name: " + profile.Lastname + " " + profile.Firstname)

gender_stringvar = tk.StringVar()
gender_lable = tk.Label(main_window,  textvariable=gender_stringvar)
gender_lable.place(x=20, y=290)
if profile.Sex == 1:
    gender_stringvar.set("Gender: Male")
elif profile.Sex == 0:
    gender_stringvar.set("Gender: Female")
else:
    gender_stringvar.set("Gender: -")

email_stringvar = tk.StringVar()
email_lable = tk.Label(main_window,  textvariable=email_stringvar)
email_lable.place(x=20, y=310)
email_stringvar.set("Email: " + profile.Email)

age_stringvar = tk.StringVar()
age_lable = tk.Label(main_window,  textvariable=age_stringvar)
age_lable.place(x=20, y=330)
if get_login_status() == "1":
    age_stringvar.set("Age: " + str(profile.get_age()))
else:
    age_stringvar.set("Age: -")

refresh_button = tk.Button(main_window, text="Refresh!", command=refresh)
refresh_button.place(x=20, y=370, height=50, width=100)

login_button_var = tk.StringVar()
login_button = tk.Button(
    main_window, textvariable=login_button_var, command=log_in_out)
login_button.place(x=140, y=370, height=50, width=100)
if get_login_status() == "1":
    login_button_var.set("Log out!")
else:
    login_button_var.set("Log in!")


glucose_button = tk.Button(main_window, text="Glucose data",
                           command=lambda: data_windows(Data_types.GlucoseMeasurements))
glucose_button.place(x=275, y=20, width=200, height=50)

activity_button = tk.Button(main_window, text="Physical activities",
                            command=lambda: data_windows(Data_types.PhysicalActivities))
activity_button.place(x=275, y=90, width=200, height=50)

meals_button = tk.Button(main_window, text="Meals",
                         command=lambda: data_windows(Data_types.Meals))
meals_button.place(x=275, y=160, width=200, height=50)

medicine_button = tk.Button(main_window, text="Medicine",
                            command=lambda: data_windows(Data_types.MedicineIntakes))
medicine_button.place(x=275, y=230, width=200, height=50)

feels_button = tk.Button(main_window, text="Feels",
                         command=lambda: data_windows(Data_types.Feels))
feels_button.place(x=275, y=300, width=200, height=50)

therapy_button = tk.Button(main_window, text="Therapy data",
                           command=lambda: data_windows(Data_types.Therapy))
therapy_button.place(x=275, y=370, width=200, height=50)


def login_error():
    messagebox.showerror("Error", "Please log in!")


main_window.mainloop()
