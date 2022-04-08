from time import sleep
from os.path import isfile, join, exists
from os import listdir, getcwd, rename, makedirs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configHandler import get_username, get_password


def get_dcont_data():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": getcwd()+"/data",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("https://fiok.dcont.hu/")
    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "Username")))
        element = driver.find_element(By.ID, "Username")
        element.send_keys(get_username())
        element = driver.find_element(By.ID, "Password")
        element.send_keys(get_password())
        driver.find_element(By.NAME, "button").click()
        try:
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "profile-dropdown-icon")))
            driver.get("https://enaplo.dcont.hu/beallitasok/fiok")
            try:
                button_path = "/html/body/div/div/div/main/div/div[2]/div[2]/section/div/div/div/div/div[2]/div[1]/div[2]/form/fieldset/div/button"
                element = WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                    (By.XPATH, button_path)))
                driver.find_element(
                    By.XPATH, button_path).click()
                if not exists(getcwd()+"/data"):
                    makedirs("data")
                path = getcwd()+"/data"
                data_file = ""
                timeout_counter = 30
                while data_file == "":
                    files = [f for f in listdir(path) if isfile(join(path, f))]
                    for file in files:
                        if file[0:12] == "DcontProfile" and file[-4::] == "json":
                            data_file = file
                    timeout_counter -= 1
                    if timeout_counter == 0:
                        driver.close()
                        return 4
                    sleep(2)
                rename("data/"+data_file, "data/data.json")
            except:
                driver.close()
                return 3
        except:
            driver.close()
            return 2
    except:
        driver.close()
        return 1
    driver.close()
    return 0

# to-do: adatok felvitele
