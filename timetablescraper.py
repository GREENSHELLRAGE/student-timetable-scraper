# source venv/bin/activate
# python3 timetablescraper.py
import base64
import json
from bs4 import BeautifulSoup
from CarletonTools import *


# Get login cridentials from json file
with open('cridentials.json', 'r') as f:
    cridentials = json.loads(f.read())
my_username = base64.b64decode(cridentials["username"]).decode()
my_password = base64.b64decode(cridentials["password"]).decode()

print(my_username)

# Create instance of scraper
scraper = CarletonScraper(my_username, my_password)

# # Get student timetable page
scraper.carleton_central_login()
timetable_html = scraper.get_carleton_page('https://central.carleton.ca/prod/bwskfshd.P_CrseSchd')

# Patch student timetable html
print("Patching student timetable html...")
soup = BeautifulSoup(timetable_html, features='html.parser')

# Replace building abbreviations with full building names in timetable
full_building_names = {
    'AA': 'AA Architecture Building',
    'AP': 'AP Azrieli Pavillion',
    'AR': 'AR ARISE Building',
    'AT': 'AT Azrieli Theatre',
    'CB': 'CB Canal Building',
    'CO': 'CO Residence Commons',
    'DT': 'DT Dunton Tower',
    'HC': 'HC Human Computer Interaction Building',
    'HP': 'HP Herzberg Building',
    'HS': 'HS Health Sciences Building',
    'LA': 'LA Loeb Building',
    'MC': 'MC Minto Center for Advanced Studies in Engineering',
    'ME': 'ME Mackenzie Building',
    'ML': 'ML MacOdrum Library',
    'NB': 'NB Nesbitt Biology Building',
    'NI': 'NI Nicol Building',
    'NN': 'NN Nideyinàn (University Center)',
    'PA': 'PA Paterson Hall',
    'RB': 'RB Richcraft Hall',
    'RO': 'RO Robertson Hall',
    'SA': 'SA Southam Hall (Kailash Mital Theatre)',
    'SC': 'SC Steacie Building',
    'SR': 'SR Social Science Research Building',
    'TB': 'TB Tory Building',
    'TT': 'TT Carleton Technology & Training Center',
    'UC': 'UC University Centre',
    'VS': 'VS Visualization & Simulation Building',
}
for element in soup.find_all('td', {'class':'ddlabel'}):
    strings = list(element.stripped_strings)
    for short_name in full_building_names.keys():
        if strings[3].startswith(short_name):
            strings[3] = strings[3].replace(short_name, full_building_names[short_name])
    new_text = '\n'.join(strings)
    element.find('a').replace_with(new_text)

# Remove all links on page
for element in soup.find_all('a', href=True):
    element.extract()

# Remove everything other than the class schedule
for element in soup.find_all('div', {'class': 'infotextdiv'}):
    element.extract()
soup.find('div', {'class': 'pagetitlediv'}).extract()
soup.find('div', {'class': 'headerlinksdiv'}).extract()
soup.find('div', {'class': 'footerbeforediv'}).extract()
soup.find('div', {'class': 'footerlinksdiv'}).extract()
soup.find('div', {'class': 'pageheaderdiv1'}).extract()
soup.find('span', {'class': 'pageheaderlinks'}).extract()
soup.find('td', {'class': 'bgtabon'}).extract()
soup.find('form').extract()

# Insert extra info/notes at the bottom of the student timetable page
extra_info_html = '- Add notes here'
soup.find('span', {'class': 'releasetext'}).replace_with(BeautifulSoup('<span class="releasetext">' + extra_info_html + '</span>', features='html.parser'))

patched_html = patch_carleton_central_page(str(soup))

# Save timetable html
with open('centraltimetable.html', 'w') as f:
    f.write(patched_html)