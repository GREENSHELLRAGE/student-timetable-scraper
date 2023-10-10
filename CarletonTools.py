import requests
import html
from bs4 import BeautifulSoup


# Some of the code here may seem pretty weird because the login process it's going through was reverse engineered using Google Chrome's inspect tool.
# It's basically "emulating" what your browser does when logging into Carleton's services.
# Carleton's services have no protection against logging in and scraping pages extremely quickly lol.


class CarletonScraper:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


    def carleton_central_login(self) -> None:
        # Start requests session
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

        # Load Carleton Central login page
        print('Loading Carleton Central login page...')
        response = self.session.get('https://ssoman.carleton.ca/ssomanager/c/SSB', headers=self.headers)
        
        # Load CAS login page
        print('Loading CAS login page...')
        response = self.session.get(response.url, headers=self.headers)
        
        # Get login form url from login screen html
        soup = BeautifulSoup(response.text, features='html.parser')
        post_url = soup.find(id='options')['action']

        # Post username and password to the login form
        print('Posting username and password to login form...')
        values = {'userName': self.username, 'password': self.password}
        response = self.session.post(post_url, headers=self.headers, data=values)
        
        # Get value for loading screen form
        soup = BeautifulSoup(response.text, features='html.parser')
        wresult = html.unescape(soup.find('input', {'name': 'wresult'})['value'])
        wctx = html.unescape(soup.find('input', {'name': 'wctx'})['value'])

        # Post value to loading screen form and log in to Carleton Central
        print('Posting value to loading screen form and logging into Carleton Central...')
        values = {'wa': 'wsignin1.0', 'wresult': wresult, 'wctx': wctx}
        self.session.post('https://cas6.carleton.ca:443/cas/login', headers=self.headers, data=values)
        print('Successfully logged into Carleton Central!')

    
    def brightspace_login(self) -> None:
        # Start requests session
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

        # Load brightspace login page
        print('Loading Brightspace login page...')
        response = self.session.get('https://brightspace.carleton.ca/', headers=self.headers)
        
        # Get login form url from login screen html
        soup = BeautifulSoup(response.text, features='html.parser')
        post_url = soup.find(id='options')['action']

        # Post username and password to the login form
        print('Posting username and password to login form...')
        values = {'userName': self.username, 'password': self.password}
        response = self.session.post(post_url, headers=self.headers, data=values)
        
        # Get value for loading screen form
        soup = BeautifulSoup(response.text, features='html.parser')
        SAMLResponse = html.unescape(soup.find('input', {'name': 'SAMLResponse'})['value'])
        
        # Post value to loading screen form and log in to Brightspace
        print('Posting value to loading screen form and logging into Brightspace...')
        values = {'wa': 'wsignin1.0', 'SAMLresponse': SAMLResponse}
        self.session.post('https://brightspace.carleton.ca:443/d2l/lp/auth/login/samlLogin.d2l', headers=self.headers, data=values)

        print('Successfully logged into Brightspace!')


    def get_carleton_page(self, url: str) -> str:
        # Load url in current session
        print('Loading ' + url + '...')
        response = self.session.get(url, headers=self.headers)
        return response.text

    def post_carleton_page(self, url: str) -> str:
        # Load url in current session
        print('Posting to ' + url + ' and loading response...')
        response = self.session.post(url, headers=self.headers)
        return response.text

    
def patch_brightspace_page(html: str) -> str:
    print('Patching Brightspace links in HTML...')
    soup = BeautifulSoup(html, features='html.parser')
    # Find all links that start with '/' and add the start of the Brightspace URL
    for element in soup.find_all(href=True):
        if element['href'].startswith('/'):
            element['href'] = 'https://brightspace.carleton.ca' + element['href']
    for element in soup.find_all(src=True):
        if element['src'].startswith('/'):
            element['src'] = 'https://brightspace.carleton.ca' + element['src']
    return str(soup)


def patch_carleton_central_page(html: str) -> str:
    print('Patching Carleton Central links in HTML...')
    soup = BeautifulSoup(html, features='html.parser')

    # Insert SUCKS image beside Carleton Central so it says Carleton Central SUCKS at the top of the page
    sucks_image_html = '<img style="height:72px; margin-left: 420px;" src="https://previews.123rf.com/images/imagecatalogue/imagecatalogue1611/imagecatalogue161119259/65955834-sucks-text-rubber-seal-stamp-watermark-tag-inside-rounded-rectangular-shape-with-grunge-design-and-d.jpg">'
    soup.find('div', {'class': 'headerwrapperdiv'}).insert_before(BeautifulSoup(sucks_image_html, features='html.parser'))
    
    # Replace copyright banner with something better lol
    better_banner_html = "<h5>Scraped and patched with GREENSHELLRAGE's timetable scraper, Carleton Central sucks lol</h5>"
    soup.find('h5').replace_with(BeautifulSoup(better_banner_html, features='html.parser'))

    # Find all links that start with '/' and add the start of the Carleton Central URL
    for element in soup.find_all(href=True):
        if element['href'].startswith('/'):
            element['href'] = 'https://central.carleton.ca' + element['href']
    for element in soup.find_all(src=True):
        if element['src'].startswith('/'):
            element['src'] = 'https://central.carleton.ca' + element['src']
    return str(soup)