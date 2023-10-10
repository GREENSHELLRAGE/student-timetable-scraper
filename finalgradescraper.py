# source venv/bin/activate
# python3 finalgradescraper.py
import base64
import json
from bs4 import BeautifulSoup
from CarletonTools import *

# Get login cridentials from json file
with open('cridentials.json', 'r') as f:
    cridentials = json.loads(f.read())
my_username = base64.b64decode(cridentials["username"]).decode()
my_password = base64.b64decode(cridentials["password"]).decode()

# Create instance of scraper
scraper = CarletonScraper(my_username, my_password)

# Get final grades from carleton central
scraper.carleton_central_login()

# Get list of semesters
final_grades_selection_url = 'https://central.carleton.ca/prod/bwskogrd.P_ViewTermGrde'
final_grades_selection_page = scraper.get_carleton_page(final_grades_selection_url)

# Get final grade for each semester
soup = BeautifulSoup(final_grades_selection_page, features='html.parser')
for semester in soup.find_all('option'):
    final_grades_url = 'https://central.carleton.ca/prod/bwskogrd.P_ViewGrde?term_in=' + semester['value']
    final_grades_page = scraper.get_carleton_page(final_grades_url)
    patched_html = patch_carleton_central_page(final_grades_page)

    # Save final grades html
    file_name = 'grades' + semester['value'] + '.html'
    with open(file_name, 'w') as f:
        f.write(patched_html)