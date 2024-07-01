import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import random
import time
from unidecode import unidecode

# Construct the path to the chromedriver executable
chrome_driver_path = "./chromedriver.exe" # Replace the path with actual path if chromedriver not in same directory

chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-infobars")

# Create ChromeDriver service
service = ChromeService(executable_path=chrome_driver_path)

# Initialize WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

def rate_review(driver, stars):
    star_xpath = f"//span[contains(@aria-label, 'Rate {stars} stars')]"
    star_element = driver.find_element(By.XPATH, star_xpath)
    star_element.click()

def write_review(password, place_url, stars):
    try:
        driver.get(place_url)
        time.sleep(2)

        review_button = driver.find_element(By.CSS_SELECTOR, "button[jsaction='pane.reviewFlow.reviewDialog']")
        review_button.click()
        time.sleep(2)

        rate_review(driver, stars)
        time.sleep(2)

        review_text_area = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Write a review']")
        review_text_area.send_keys("This is a great place!")

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[jsaction='pane.reviewFlow.submit']")
        submit_button.click()
        
        time.sleep(5)
        print("Review posted successfully.")
    except Exception as e:
        print("An error occurred while posting the review:", e)
    finally:
        driver.quit()

def fill_form(first_name, last_name, birthday, gender, username, password):
    try:
        driver.get("https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp")

        first_name_input = driver.find_element(By.NAME, "firstName")
        last_name_input = driver.find_element(By.NAME, "lastName")
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        next_button = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe")
        next_button.click()

        wait = WebDriverWait(driver, 20)
        day = wait.until(EC.visibility_of_element_located((By.NAME, "day")))

        birthday_elements = birthday.split()
        month_dropdown = Select(driver.find_element(By.ID, "month"))
        month_dropdown.select_by_value(birthday_elements[1])
        day_field = driver.find_element(By.ID, "day")
        day_field.clear()
        day_field.send_keys(birthday_elements[0])
        year_field = driver.find_element(By.ID, "year")
        year_field.clear()
        year_field.send_keys(birthday_elements[2])

        gender_dropdown = Select(driver.find_element(By.ID, "gender"))
        gender_dropdown.select_by_value(gender)
        next_button = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe")
        next_button.click()

        time.sleep(2)
        if driver.find_elements(By.ID, "selectionc4"):
            create_own_option = wait.until(EC.element_to_be_clickable((By.ID, "selectionc4")))
            create_own_option.click()
        
        create_own_email = wait.until(EC.element_to_be_clickable((By.NAME, "Username")))
        username_field = driver.find_element(By.NAME, "Username")
        username_field.clear()
        username_field.send_keys(username)
        next_button = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe")
        next_button.click()
        
        password_field = wait.until(EC.visibility_of_element_located((By.NAME, "Passwd")))
        password_field.clear()
        password_field.send_keys(password)
        confirm_passwd_div = driver.find_element(By.ID, "confirm-passwd")
        password_confirmation_field = confirm_passwd_div.find_element(By.NAME, "PasswdAgain")
        password_confirmation_field.clear()
        password_confirmation_field.send_keys(password)
        next_button = driver.find_element(By.CLASS_NAME, "VfPpkd-LgbsSe")
        next_button.click()

        skip_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")))
        for button in skip_buttons:
            button.click()

        agree_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")))
        agree_button.click()

        print(f"Your Gmail successfully created:\n{{\ngmail: {username}@gmail.com\npassword: {password}\n}}")

    except Exception as e:
        print("Failed to create your Gmail, Sorry")
        print(e)
    finally:
        driver.quit()

def main():
    french_first_names = [
        "Amélie", "Antoine", "Aurélie", "Benoît", "Camille", "Charles", "Chloé", "Claire", "Clément", "Dominique",
        "Élodie", "Émilie", "Étienne", "Fabien", "François", "Gabriel", "Hélène", "Henri", "Isabelle", "Jules",
        "Juliette", "Laurent", "Léa", "Léon", "Louise", "Lucas", "Madeleine", "Marc", "Margaux", "Marie",
        "Mathieu", "Nathalie", "Nicolas", "Noémie", "Olivier", "Pascal", "Philippe", "Pierre", "Raphaël", "René",
        "Sophie", "Stéphane", "Suzanne", "Théo", "Thomas", "Valentin", "Valérie", "Victor", "Vincent", "Yves",
        "Zoé", "Adèle", "Adrien", "Alexandre", "Alice", "Alix", "Anatole", "André", "Angèle", "Anne",
        "Baptiste", "Basile", "Bernard", "Brigitte", "Céleste", "Céline", "Christophe", "Cyril", "Denis", "Diane",
        "Édouard", "Éléonore", "Émile", "Félix", "Florence", "Georges", "Gérard", "Guillaume", "Hugo", "Inès",
        "Jacques", "Jean", "Jeanne", "Joséphine", "Julien", "Laure", "Lucie", "Maëlle", "Marcel", "Martine",
        "Maxime", "Michel", "Nina", "Océane", "Paul", "Perrine", "Quentin", "Romain", "Solène", "Thérèse"
    ]

    french_last_names = [
        "Leroy", "Moreau", "Bernard", "Dubois", "Durand", "Lefebvre", "Mercier", "Dupont", "Fournier", "Lambert",
        "Fontaine", "Rousseau", "Vincent", "Muller", "Lefèvre", "Faure", "André", "Gauthier", "Garcia", "Perrin",
        "Robin", "Clement", "Morin", "Nicolas", "Henry", "Roussel", "Mathieu", "Garnier", "Chevalier", "François",
        "Legrand", "Gérard", "Boyer", "Gautier", "Roche", "Roy", "Noel", "Meyer", "Lucas", "Gomez",
        "Martinez", "Caron", "Da Silva", "Lemoine", "Philippe", "Bourgeois", "Pierre", "Renard", "Girard", "Brun",
        "Gaillard", "Barbier", "Arnaud", "Martins", "Rodriguez", "Picard", "Roger", "Schmitt", "Colin", "Vidal",
        "Dupuis", "Pires", "Renaud", "Renault", "Klein", "Coulon", "Grondin", "Leclerc", "Pires", "Marchand",
        "Dufour", "Blanchard", "Gillet", "Chevallier", "Perrot", "Adam", "Schneider", "Letellier", "Chauvin", "Perret",
        "Maurice", "Louis", "Boucher", "Robert", "Meunier", "Dubois", "Leroy", "Morel", "Laurent", "Dupuy",
        "Guillot", "Gosselin", "Richard", "Aubry", "Roux", "Dupont", "Pichon", "Berger", "Charles", "Guérin"
    ]
    
    your_first_name = random.choice(french_first_names)
    your_last_name = random.choice(french_last_names)

    your_first_name_normalized = unidecode(your_first_name).lower()
    your_last_name_normalized = unidecode(your_last_name).lower()

    your_username = f"{your_first_name_normalized}.{your_last_name_normalized}{random.randint(10, 2000)}"

    your_birthday = f"{random.randint(10, 30)} {random.randint(1, 12)} {random.randint(1985, 2000)}"
    your_gender = "1"
    your_password = "cheathack"

    fill_form(your_first_name, your_last_name, your_birthday, your_gender, your_username, your_password)

    # Use the created Gmail account to rate a place
    place_url = "https://www.google.com/maps/place/PLACE_ID"  # Replace PLACE_ID with the actual place ID
    write_review(your_password, place_url, 5) # Replace "5" with the number of stars you want to rate, for example 1 to 5

if __name__ == "__main__":
    main()
