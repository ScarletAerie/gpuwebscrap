#Goal: Check Video card gpus via streamlit on Newegg, Canada Computers (for now will add more later) that are in stock

from bs4 import BeautifulSoup
import requests 
import re
import streamlit as st


st.title("Computer Part Scraper")


st.write("This app performs webscraping for Computers part from companies such as: Canada Computers, Newegg, etc")

gpu_company =st.multiselect('Select Company you would like to search', ['Newegg', 'Canada Computers'])
gpu = st.text_input("What product do you want to search for? ")


if 'Newegg' in gpu_company:	
	
	if gpu:
		url = f"https://www.newegg.ca/p/pl?d={gpu}&N=4131"
		page = requests.get(url).text
		doc = BeautifulSoup(page, "html.parser")

		page_text = doc.find(class_="list-tool-pagination-text").strong
		pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

		items_found = {}

		for page in range(1, pages + 1):
			url = f"https://www.newegg.ca/p/pl?d={gpu}&N=4131&page={page}"
			page = requests.get(url).text
			doc = BeautifulSoup(page, "html.parser")

			div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
			items = div.find_all(text=re.compile(gpu))

			for item in items:
				parent = item.parent
				if parent.name != "a":
					continue

				link = parent['href']
				next_parent = item.find_parent(class_="item-container")
				try:
					price = next_parent.find(class_="price-current").find("strong").string
					items_found[item] = {"price": int(price.replace(",", "")), "link": link}
				except:
					pass

		sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
		for item in sorted_items:
	 		st.write(item[0])
	 		st.write(f"${item[1]['price']}")
	 		st.write(item[1]['link'])
	 		st.write("-------------------------------")
elif 'Canada Computers' in gpu_company:
	if gpu:
		url = f"https://www.canadacomputers.com/search/results_details.php?language=en&keywords={gpu}"

		page = requests.get(url).text

		doc = BeautifulSoup(page, "html.parser")
		div = doc.find("div",{"id": "product-list"})

		items = div.find_all(text=re.compile(gpu))

		items_found = {}

		for item in items:
			parent= item.parent
			if parent.name != "a":
				continue
			link = parent['href']	
			next_parent = item.find_parent(class_="px-0 col-12 productInfoSearch pt-2")
			
			try: 
				price = next_parent.find(class_="d-block mb-0 pq-hdr-product_price line-height").find("strong").string
				items_found[item] = {"price": int(price.replace(",", "")), "link": link}
			except:
				pass

			st.write(item)
			st.write(price)
			st.write(link)	


 
