# Student Timetable Scraper
These Python scripts log in to Carleton Central and Brightspace and can be used to get your student timetable and grades. Since the Brightspace API is not available to students, I had to reverse engineer the login process using Google Chrome's inspect tool, so the login code may be slightly cryptic. It basically "emulates" what your browser does when you enter your username and password and log in normally.

At some point I should probably turn this into a proper Python package that can be installed using ```pip install```, but for now it's just a few crappy Python scripts.

# Dependencies

BeautifulSoup: ```pip install bs4```

You'll also need to create a ```cridentials.json``` file in the same directory as the Python code with the following strings:
```json
{
  "username": "CUNET\your_user_name",
  "password": "your_password"
}
```
The strings ```"CUNET\your_user_name"``` and ```"your_password"``` must be encoded in base64.

# Usage

```timetablescraper.py``` -> downloads your student timetable from Carleton Central and saves it as ```centraltimetable.html```

```gradescraper.py``` -> downloads your grades from all of your courses from Brightspace and saves it as ```centraltimetable.html```

```finalgradescraper.html``` -> downloads your final grades from Carleton Central and saves them in multiple files, 1 for each semester
