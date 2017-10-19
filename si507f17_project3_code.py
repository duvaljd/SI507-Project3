from bs4 import BeautifulSoup
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!

stateNames_list = ["Arkansas", "California", "Michigan"]
stateAbbrs = {
'alabama':'al',
'alaska':'ak',
'arizona':'az',
'arkansas':'ar',
'california':'ca',
'colorado':'co',
'connecticut':'ct',
'delaware':'de',
'florida':'fl',
'georgia':'ga',
'hawaii':'hi',
'idaho':'id',
'illinois':'il',
'indiana':'in',
'iowa':'ia',
'kansas':'ks',
'kentucky':'ky',
'louisiana':'la',
'maine':'me',
'maryland':'md',
'massachusetts':'ma',
'michigan':'mi',
'minnesota':'mn',
'mississippi':'ms',
'missouri':'mo',
'montana':'mt',
'nebraska':'ne',
'nevada':'nv',
'new hampshire':'nh',
'new jersey':'nj',
'new mexico':'nm',
'new york':'ny',
'north carolina':'nc',
'north dakota':'nd',
'ohio':'oh',
'oklahoma':'ok',
'oregon':'or',
'pennsylvania':'pa',
'rhode island':'ri',
'south carolina':'sc',
'south dakota':'sd',
'tennessee':'tn',
'texas':'tx',
'utah':'ut',
'vermont':'vt',
'virginia':'va',
'washington':'wa',
'west virginia':'wv',
'wisconsin':'wi',
'wyoming':'wy',
'guam':'gu',
'puerto rico':'pr',
'virgin islands':'vi'}

######### PART 0 #########

# Write your code for Part 0 here.

def getAltText(url):
	try:
		data = open("page.html", "r").read()
	except:
		data = requests.get(url).text
		f = open("page.html", "w")
		f.write(data)
		f.close()

	page = BeautifulSoup(data, "html.parser")
	images = page.find_all("img")
	altText = []

	for pic in images:
		altText.append(pic.get("alt", "No alternative text provided!"))

	for text in altText:
		print("{}\n\n".format(text))

getAltText("http://newmantaylor.com/gallery.html")

######### PART 1 #########

# Get the main page data...
def getNPS_data(returnData = True, makeSoup = False):
	try:
		nps_data = open("nps_gov_data.html", "rb").read()
	except:
		nps_data = requests.get("https://www.nps.gov/index.htm").text
		f = open("nps_gov_data.html", "wb")
		f.write(nps_data.encode("utf-8"))
		f.close()

	if makeSoup == True:
		nps_soup = BeautifulSoup(nps_data, "html.parser")
		menuData_soup = nps_soup.find('ul', attrs={"class":["dropdown-menu", "SearchBar-keywordSearch"]})
		return menuData_soup

	elif returnData == True:
		return nps_data

def getState_data(state, returnData = True):
	try:
		state_data = open("{}_data.html".format(state).lower(), "rb").read()
	except:
		menuData_soup = getNPS_data(False, True)

		for link in menuData_soup.find_all("a"):
			if link.text.lower() == "{}".format(state).lower():
				print(link.get("href"))
				state_data = requests.get("https://www.nps.gov{}".format(link.get("href"))).text
				f = open("{}_data.html".format(state).lower(), "wb")
				f.write(state_data.encode("utf-8"))
				f.close

	if returnData == True:
		return state_data

ak_data = getState_data("Arkansas")
ca_data = getState_data("California")
mi_data =getState_data("Michigan")

######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...





## Define your class NationalSite here:

class NationalSite(object):

	def __init__(self, parkSoup):
		self.parkSoup = parkSoup
		self.location = parkSoup.h4.text
		self.name = parkSoup.h3.text
		self.type = parkSoup.h2.text
		self.description = parkSoup.p.text

	def __str__(self):
		return "{} | {}".format(self.name, self.location)

	def __contains__(self, inParkName):
		if str(inParkName).lower() in self.name.lower():
			return True

	def get_mailing_address(self):
		urlSoup = self.parkSoup.select_one("a[href*=basic]")
		data = requests.get(urlSoup.get("href")).text
		basicInfoSoup = BeautifulSoup(data, "html.parser")
		street = basicInfoSoup.find("span", itemprop = "streetAddress")
		locality = basicInfoSoup.find("span", itemprop = "addressLocality")
		region = basicInfoSoup.find("span", itemprop = "addressRegion")
		code = basicInfoSoup.find("span", itemprop = "postalCode")

		return(str("{} / {} / {} / {}").format(street.text, locality.text, region.text, code.text)) 

## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

f = open("sample_html_of_park.html",'r')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
sample_inst = NationalSite(soup_park_inst)
f.close()

sampleSite = NationalSite(soup_park_inst)

######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.




##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!

