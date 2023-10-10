# source venv/bin/activate
# python3 gradescraper.py
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

# Log in to brightspace
scraper.brightspace_login()

# Get brightspace home page
brightspace_homepage_url = 'https://brightspace.carleton.ca/d2l/home'
brightspace_homepage_html = scraper.get_carleton_page(brightspace_homepage_url)

# Get URL from the course selection button
soup = BeautifulSoup(brightspace_homepage_html, features='html.parser')
course_selection_element = soup.find('d2l-navigation-dropdown-button-icon')
course_selection_url = 'https://brightspace.carleton.ca' + course_selection_element['data-prl']

# Get list of courses
course_list_json = json.loads(scraper.get_carleton_page(course_selection_url)[9:])
course_list_html = patch_brightspace_page(course_list_json['Payload']['Html'])

# Get URLs to grade pages
grade_page_urls = []
soup = BeautifulSoup(course_list_html, features='html.parser')
for element in soup.find_all('a', {'class', 'd2l-link'}, onclick=False):
    course_id = element['href'][41:]
    grade_page_urls.append('https://brightspace.carleton.ca/d2l/lms/grades/my_grades/main.d2l?ou=' + course_id)

# Get all grades for all courses and create webpage
generated_grade_page_html = '<h1>Brightspace Sucks lol</h1>'
for x in range(len(grade_page_urls)):
    # Load grades page
    print('Loading course ' + str(x + 1) + '/' + str(len(grade_page_urls)) + '...')
    grade_page_html = scraper.get_carleton_page(grade_page_urls[x])
    soup = BeautifulSoup(grade_page_html, features='html.parser')
    
    # Get course name and grades table
    course_name = soup.find('a', {'class': 'd2l-navigation-s-link'})['title']
    grades_table = str(soup.find('table', {'class': 'd2l-table d2l-grid d_gl'}))
    
    # Only add course to the webpage if brightspace has the grades table for that course
    if grades_table != "None":
        generated_grade_page_html += '<h2><a href="' + grade_page_urls[x] + '">' + course_name + '</a></h2><br><br>'
        generated_grade_page_html += grades_table + '<br><br>'

patched_html = patch_brightspace_page(generated_grade_page_html)

# Save brightspace html
with open('brightspacegrades.html', 'w') as f:
    f.write(patched_html)