
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
from dotenv import load_dotenv
import os
import time

# Load variables from .env file
load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
form_link = os.getenv('FORM_LINK')

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.set_window_size(1130, 560)
driver.get(form_link)

# Login to Gmail Account


def login_to_gmail():
    email_textfield = driver.find_element(By.NAME, "identifier")
    email_next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    email_textfield.send_keys(email)
    email_next_button.click()

    driver.implicitly_wait(10)
    password_field = driver.find_element(By.NAME, "Passwd")
    password_field.send_keys(password)
    time.sleep(2)
    password_next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    password_next_button.click()


def calculate_age(date_input):
    if date_input != '':
        # Convert the input string to a datetime object
        date = datetime.strptime(date_input, "%m/%d/%Y")

        # Get the current date
        current_date = datetime.now()

        # Calculate the age
        age = current_date.year - date.year

        # Adjust the age if the birthday hasn't occurred yet this year
        if current_date.month < date.month or (current_date.month == date.month and current_date.day < date.day):
            age -= 1

        return age
    else:
        return "Not indicated"


def select_index(string_input):
    patterns = {
        r"installation": 0,
        r"redundancy": 1,
        r"retrenchment": 2,
        r"closure": 3,
        r"economic": 8,
    }
    for pattern, index in patterns.items():
        if re.search(pattern, string_input, re.IGNORECASE):
            return index
    return None


def enter_data():
    tracking_number = ""
    name = ""
    sex_input = ""
    termination_reason = ""

    while not tracking_number:
        tracking_number = input("Enter Tracking Number: ")
        if not tracking_number:
            print("Error: Input cannot be empty. Please try again.")

    while not name:
        name = input("Enter Fullname: ")
        if not name:
            print("Error: Input cannot be empty. Please try again.")

    email = input("Enter Email: ")
    contact_number = input("Enter Contact Number: ")

    while not sex_input:
        sex_input = input("Enter Gender: M = Male ; F = Female: ")
        if not sex_input:
            print("Error: Input cannot be empty. Please try again.")
    sex_value = (1, "Male") if sex_input.lower() == "m" else (0, "Female")
    sex_index, sex_text = sex_value

    birthdate = input("Enter birthdate (MM/DD/YYYY): ")
    age = calculate_age(birthdate)
    address = input("Enter Address: ")
    address_value = address if address != '' else "Not Indicated"
    employer_name = input("Enter Name of Employer: ")

    while True:
        termination_reason = input("Enter Reason of Termination: ")
        if not termination_reason:
            print("Error: Input cannot be empty. Please try again.")
        else:
            termination_index = select_index(termination_reason)
            if termination_index is None:
                print("Error: Input does not match any pattern. Please try again.")
            else:
                break

    print(f"""
    SSS Unemployment Benefit Data
    Tracking Number: {tracking_number}
    Fullname: {name}
    Email: {email}
    Contact Number: {contact_number}
    Sex: {sex_text}
    Age: {age}
    Address: {address_value}
    Name of Employer: {employer_name}
    Reason of Termination: {termination_reason}
    """)

    return tracking_number, name, email, contact_number, sex_index, age, address_value, employer_name, termination_index


def fill_form(tracking_number, name, email, contact_number, sex_index, age, address_value, employer_name, termination_index):
    tracking_number_field = driver.find_element(
        By.CSS_SELECTOR, '.whsOnd.zHQkBf')
    tracking_number_field.send_keys(tracking_number)
    next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    next_button.click()

    input("Press ENTER when form is loaded")

    fields = driver.find_elements(By.CSS_SELECTOR, '.whsOnd.zHQkBf')
    name_field = fields[0]
    email_field = fields[1]
    contact_field = fields[2]
    sex_radio_button = driver.find_elements(By.CSS_SELECTOR, '.AB7Lab.Id5V1')
    age_field = fields[3]
    address_field = driver.find_element(By.CSS_SELECTOR, '.KHxj8b.tL9Q4c')

    time.sleep(2)
    name_field.send_keys(name)
    email_field.send_keys(email)
    contact_field.send_keys(contact_number)
    sex_radio_button[sex_index].click()
    age_field.send_keys(age)
    address_field.send_keys(address_value)
    next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    next_button.click()

    input("Press ENTER when form is loaded")

    employer_name_field = driver.find_element(
        By.CSS_SELECTOR, '.whsOnd.zHQkBf')
    employer_name_field.send_keys(employer_name)
    termination_reason_chechbox = driver.find_elements(
        By.CSS_SELECTOR, '.uHMk6b.fsHoPb')
    termination_reason_chechbox[termination_index].click()
    next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    next_button.click()

    input("Press ENTER when form is loaded and upload the ID & Notice")

    processor_checklist = driver.find_elements(
        By.CSS_SELECTOR, '.uHMk6b.fsHoPb')
    processor_checklist[5].click()
    other_field = driver.find_element(By.CSS_SELECTOR, ".Hvn9fb.zHQkBf")
    other_field.send_keys("Roneal Denila")
    remark_input = f'Certified {datetime.now().strftime("%x")}'
    driver.find_element(
        By.CSS_SELECTOR, ".KHxj8b.tL9Q4c").send_keys(remark_input)
    print("")


# Main Program

login_to_gmail()

while True:
    data = enter_data()
    fill_form(*data)
