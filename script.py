import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime,timedelta
import sqlite3

chrome_path = "C:\webdriver\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("headless") 
driver = webdriver.Chrome(chrome_path , options = chrome_options , keep_alive = False) 
driver.get("http://www.casablanca-bourse.com/bourseweb/indice-ponderation.aspx?Cat=22&IdLink=298")

#codepath = """//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[4]/td[2]"""
#code = codepath[4].strip()
#code =driver.find_element_by_xpath(codepath)
#print(code) //*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[4]/td[2]
codelist = []
instrumentList = []
NbreList = []
CoursList = []
FacteurList = []
FacteurPlafList = []
Capitalist = []
poidList = []


def get_data(date_string):

	driver.execute_script(f"document.getElementById('Ponderation1_DateTimeControl1_TBCalendar').value = '{date_string}'")
	driver.find_element_by_id("Ponderation1_ImageButton1").click()

	time.sleep(3)

	for i in range(4,77):
		codepath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[4]/td[2]"""
		code = driver.find_element_by_xpath(codepath)
		codelist.append(code.text)


	for i in range(4,77):
		instrumentpath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[4]"""
		instrument = driver.find_element_by_xpath(instrumentpath)
		instrumentList.append(instrument.text)


	for i in range(4,77):
		Nbrepath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[6]"""
		Nbre = driver.find_element_by_xpath(Nbrepath)
		NbreList.append(Nbre.text)

	for i in range(4,77):
		Courspath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[8]"""
		Cours = driver.find_element_by_xpath(Courspath)
		CoursList.append(Cours.text)

	for i in range(4,77):
		Facteurpath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[10]"""
		Facteur = driver.find_element_by_xpath(Facteurpath)
		FacteurList.append(Facteur.text)

	for i in range(4,77):
		FacteurPlafpath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[12]"""
		FacteurPlaf = driver.find_element_by_xpath(FacteurPlafpath)
		FacteurPlafList.append(FacteurPlaf.text)	

	for i in range(4,77):
		Capitalpath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[14]"""
		Capital = driver.find_element_by_xpath(Capitalpath)
		Capitalist.append(Capital.text)	

	for i in range(4,77):
		poidPath = f"""//*[@id="Ponderation1_UpdatePanel1"]/table/tbody/tr[5]/td/table/tbody/tr[{i}]/td[14]"""
		poid = driver.find_element_by_xpath(poidPath)
		poidList.append(poid.text)	

	allinfo = list(
		zip(codelist , instrumentList, NbreList , CoursList , FacteurList , FacteurPlafList , Capitalist, poidList)
		)	
	df = pd.DataFrame(
		allinfo,
		columns = ["Code Isin", "Instrument","Nombre de titres","Cours","Facteur Flottant","Facteur de plafonnement", "Capitalisation flottante", "Poids"])

	d, m, y = date_string.split("/")
	df.to_csv(f"{d} {m} {y}.csv" , index =False)

	print("\n=======================")
	print(f"Séance du {date_string}")
	print("=======================\n")
	print(allinfo)

	return allinfo



def insert_into_db(data, db,date):
	conn = sqlite3.connect(db)
	curs = conn.cursor()
	for line in data:
		curs.execute("""INSERT INTO Test (Date,
			Code_Isin,
		    Instrument,
		    Nombre_de_titres,
		    Cours,
		    Facteur_flottant,
		    Facteur_de_plafonnement,
		    Capitalisation_flottante,
		    Poids)
		    VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)""", (
		    date, line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]
		    ))
		curs.execute("commit")


date_string = input("Entrer la date de début (format JJ/MM/AAAA): \n")
end_date_string = input("Entrer la date de fin (format JJ/MM/AAAA): \n")
day, month, year = date_string.split("/")
date = datetime(int(year), int(month), int(day))
day, month, year = end_date_string.split("/")
end_date = datetime(int(year), int(month), int(day))
end_date += timedelta(days = 1)
end_date_string = end_date.strftime("%d/%m/%Y")


while date_string != end_date_string :

	try:
		data = get_data(date_string)
		insert_into_db(data, "pfa.db",date_string)
		
	except Exception as err:
		print("\n=======================")
		print(f"Séance du {date_string}")
		print("=======================\n")
		print("UNE ERREUR EST SURVENUE !")
		print(err)

	date += timedelta(days = 1)
	date_string = date.strftime("%d/%m/%Y")

