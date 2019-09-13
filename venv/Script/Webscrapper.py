from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

name = ""
element = ""
f="";
urls = []
with open("UPS_S.csv") as csvFile:
   csv_reader = csv.reader(csvFile, delimiter=',')
   for row in csv_reader:
     urls.append(row[0])


csvFile1 = "UPS_Store.csv"
csv = open(csvFile1, "w")

for i in urls:
    raw = simple_get(i)
    if raw is not None:
        soup = BeautifulSoup(raw, 'html.parser')
        for Header in soup.find_all('div', class_="Teaser-address"):
            if Header is not None:
                c = Header.text
                c = c.replace(",", "")
                csv.write(c + "\n")
                #if Header.text:
                   # csv.write(Header['class'] + "\n")

        #for container in soup.find_all('span', id="app_ctl00_scTable_lbZip"):
         #   if container is not None:
         #       element = container.text
        #       element = element.replace(",", "")
         #       csv.write(element + "\n")
        #csv.write("\n")


csv.close()