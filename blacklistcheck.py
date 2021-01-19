from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from helpers import clean
from datetime import datetime
from time import sleep
from csv import DictReader

''' THIS SECTION GETS THE VEHICLE REGS '''

#sets the url to be loaded
url = "https://app.ibexres.com/legacy/accomreports/pax_manifest.php"

#sets the options for the selenium Chrome driver
options = webdriver.ChromeOptions() 
#sets chrome driver to use the default chrome profile - which is logged in to ibex.
options.add_argument("user-data-dir=Users/admin/Library/Application Support/Google/Chrome/Default") #Path to your chrome profile

#sets up the chome driver.
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

#calls the url
driver.get(url)

#waits until it detects that the iframe has been loaded. 
wait = WebDriverWait(driver, 20)
print("Guest manifest report is loading...")
wait.until((EC.presence_of_element_located((By.ID, "theFrame"))))

#switches the target of the driver to the iframe.
frame = driver.find_element_by_name('theFrame')
driver.switch_to.frame(frame)

#waits until the date selection form fields have loaded. 
wait.until((EC.presence_of_element_located((By.NAME, "button_search"))))

#selects the current year from the dropdown form and submits
select = Select(driver.find_element_by_name("dsf"))
select.select_by_value(str(datetime.now().day))
select = Select(driver.find_element_by_name("msf"))
select.select_by_value(str(datetime.now().month))
select = Select(driver.find_element_by_name("ysf"))
select.select_by_value(str(datetime.now().year))

select = Select(driver.find_element_by_name("dst"))
select.select_by_value("31")
select = Select(driver.find_element_by_name("mst"))
select.select_by_value("12")
select = Select(driver.find_element_by_name("yst"))
select.select_by_value("2021")

driver.find_element_by_name("button_search").click()

#waits until the results table has loaded. 
wait.until((EC.presence_of_element_located((By.XPATH,"//*[text()='Total Pax (Adults + Children):']"))))

#get the value vehreg fields - NOTE THIS IS WHERE IT'S LIKELY TO FALL OVER IF THE LAYOUT OF THE TABLE CHANGES.
vehicleregs = driver.find_elements_by_xpath("//*[@id='AutoNumber2']/tbody/tr[10]/td/table/tbody/tr/td[3]/font")

#initialises lists to hold the cleaned registrations
reglist = []
finallist = []

#parses the content of the scrape and splits out the vehicle reg string.  Then appends the reg string to the reglist
for item in vehicleregs:
    reglist.append(clean(item.text))


#clean the reglist
#split out and lists that were returned by the clean function.
for item in reglist:
    if isinstance(item, list):
        for registration in item:
             reglist.append(registration)

#copy valid items into finallist
for item in reglist:
    if not isinstance(item, list) and not item == "TBC" and not item =="NA" and not item == "" and not item == "VEHREGN" and not item == "N/A":
        finallist.append(item)

#finally, remove any duplicates from finallist by using the python dict technique.
finallist = list(dict.fromkeys(finallist))

''' THIS SECTION GETS THE EMAIL ADDRESSES '''

#sets the url to be loaded
url = "https://app.ibexres.com/legacy/accomreports/FindGuest.php"

#calls the url
driver.get(url)

#waits until it detects that the iframe has been loaded. 
sleep(5)
wait = WebDriverWait(driver, 20)
print("Find guest menu is loading...")
wait.until((EC.presence_of_element_located((By.ID, "theFrame"))))

#switches the target of the driver to the iframe.
frame = driver.find_element_by_name('theFrame')
driver.switch_to.frame(frame)

#waits until the date selection form fields have loaded. 
wait.until((EC.presence_of_element_located((By.NAME, "button_search"))))

#selects the current year from the dropdown form and submits
select = Select(driver.find_element_by_name("dsf"))
select.select_by_value(str(datetime.now().day))
select = Select(driver.find_element_by_name("msf"))
select.select_by_value(str(datetime.now().month))
select = Select(driver.find_element_by_name("ysf"))
select.select_by_value(str(datetime.now().year))

select = Select(driver.find_element_by_name("dst"))
select.select_by_value("31")
select = Select(driver.find_element_by_name("mst"))
select.select_by_value("12")
select = Select(driver.find_element_by_name("yst"))
select.select_by_value("2021")

driver.find_element_by_name("button_search").click()

#waits until the results table has loaded. 
wait.until((EC.presence_of_element_located((By.XPATH,"//*[@id='AutoNumber2']/tbody/tr[10]/td/table/tbody/tr[2]/td[1]"))))

#get the value email address fields - NOTE THIS IS WHERE IT'S LIKELY TO FALL OVER IF THE LAYOUT OF THE TABLE CHANGES.
ibexemailfields = driver.find_elements_by_xpath("//*[@id='AutoNumber2']/tbody/tr[10]/td/table/tbody/tr/td[4]/font")

#initialises lists to hold the email addresses
emails = []

#parses the content of the scrape and splits out the email address string.  Then appends the email string to the emails list
for item in ibexemailfields:
    emails.append(item.text)

#ends the selenium driver session and closes Chrome.
driver.close()

for item in emails:
    item = item.lower()

''' THIS SECTION LOADS THE BLACKLIST OF EMAIL ADDRESSES AND VEHICLE REGISTRATIONS NUMBERS '''

#initialise two lists - one to hold the reg blacklist and one to hold the email blacklist.  
regblacklist = []
emailblacklist = []

#open the csv which contains the blacklist and copy the relevant rows to the list variables.
with open('csv/blacklist.csv', encoding='utf-8') as csvfile:
    fieldnames = ["vehreg", "surname", "email", "postcode", "dateoflisting", "incidentdetails", "ourref", "global"]
    reader = DictReader(csvfile, fieldnames=fieldnames)
    for row in reader:
        if not row['vehreg'] == "": 
            regblacklist.append(row['vehreg'].upper())
        if not row['email'] == "":
            emailblacklist.append(row['email'].lower())

''' THIS SECTION CHECKS WHETHER THE VEHICLE REGISTRATION NUMBERS IN THE BLACKLIST ARE PRESENT IN THE IBEX DATA.'''

#initialize variable to count the number of reg matches.
regmatchcount = 0
emailmatchcount = 0

#check regs against blacklist
for item in regblacklist:
    if item in finallist:
        print(f"Blacklist item identified - {item}")
        regmatchcount += 1

#check emails against blacklist
for item in emailblacklist:
    if item in emails:
        print(f"Blacklist item identified - {item}")
        emailmatchcount += 1

#print results of blacklist check
print(f"{str(len(finallist))} registrations were checked.  {str(regmatchcount)} blacklisted registrations was/were found")
print(f"{str(len(emails))} emails were checked.  {str(emailmatchcount)} blacklisted email addresses was/were found")