import requests
from bs4 import BeautifulSoup
import re
import pandas
import matplotlib.pyplot as plt

def create_db_from_web():
	URL = "https://pokemondb.net/pokedex/all"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")
	poke_info=soup.find_all("a", class_="ent-name")

	index = []
	name_eng = []
	name_fr = []
	type1_list = []
	type2_list = []
	height_list = []
	weight_list = []
	gen_list = []

	for poke in poke_info:
		name = poke.getText()
		if name not in name_eng :
			page = requests.get("https://pokemondb.net/" + poke['href'])
			soup = BeautifulSoup(page.content, "html.parser")

			name_tables=soup.find_all(text=re.compile('French'))
			frname = name_tables[0].parent.parent.find("td").getText()

			poke_data=soup.find_all(text=re.compile('Pokédex data'))
			poke_data_all = poke_data[0].parent.parent
			num = poke_data_all.find("strong").getText()
			types = poke_data_all.find_all("a", class_="type-icon")
			type1 = types[0].getText()
			type2 = None
			if len(types) > 1:
				type2 = types[1].getText()

			h = poke_data_all.find_all(text=re.compile('Height'))[0]
			table=h.parent.parent
			value=table.find('td').getText()
			height=value.split('m')[0][:-1]

			w = poke_data_all.find_all(text=re.compile('Weight'))[0]
			table=w.parent.parent
			value=table.find('td').getText()
			weight=value.split('kg')[0][:-1]

			print(num)

			index.append(num)
			name_eng.append(name)
			name_fr.append(frname)
			type1_list.append(type1)
			type2_list.append(type2)
			height_list.append(height)
			weight_list.append(weight)

			i = int(num)
			if i <= 151 :
				gen_list.append(1)
			elif i <= 251 :
				gen_list.append(2)
			elif i <= 386 :
				gen_list.append(3)
			elif i <= 493 :
				gen_list.append(4)
			elif i <= 649 :
				gen_list.append(5)
			elif i <= 721 :
				gen_list.append(6)
			elif i <= 809 :
				gen_list.append(7)
			elif i <= 898 :
				gen_list.append(8)


	d = {'index':index, 'name_eng':name_eng, 'name_fr':name_fr, 'type1':type1_list, 'type2':type2_list, 'height':height_list, 'weight':weight_list, 'gen':gen_list}
	df = pandas.DataFrame(data=d)



df = pandas.read_csv('pokedb.csv')

plt.plot((list(df['weight'])))
plt.show()
#df.to_csv('pokedb.csv', index=False)
#df.to_json('pokedb.json',orient="records")