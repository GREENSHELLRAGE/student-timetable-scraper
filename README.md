# Student Timetable Scraper
It feels like the Carleton Central and Brightspace websites log you out EVERY 5 NANOSECONDS!

So I made this...

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
The strings ```"CUNET\your_user_name"``` and ```"your_password"``` must be encoded in base64, which you can do [here](https://amp.base64encode.org/).

# Usage

```timetablescraper.py``` -> downloads your student timetable from Carleton Central and saves it as ```centraltimetable.html```

```gradescraper.py``` -> downloads your grades from all of your courses from Brightspace and saves it as ```brightspacegrades.html```

```finalgradescraper.html``` -> downloads your final grades from Carleton Central and saves them in multiple files, 1 for each semester

# Known Issues

Sometimes Carleton Central will force you to confirm your personal information before letting you use the rest of the site, and this will cause the login code to crash. If this happens, log into Carleton Central normally through your browser and click Continue until you reach the main menu. Once you can access the main menu the Python scripts should work again.

The login code will also crash if Carleton even slightly changes the login process. When this happens, I will need to update the login code before it works again.
