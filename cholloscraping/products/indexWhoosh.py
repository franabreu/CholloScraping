from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import os.path
from whoosh.index import create_in
from whoosh.fields import *

#Need all the categories available -  some examples at the moment
category_map = {
    'Motherboards':'&order=relevance&gtmTitle=Placas%20Base&idFamilies%5B%5D=3',
    'CPUs':'&order=relevance&gtmTitle=Procesadores%20para%20el%20PC&idFamilies%5B%5D=4',
    'HardDrives': '&order=relevance&gtmTitle=Discos%20Duros&idFamilies%5B%5D=5',
    'GraphicCards':'&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6',
    'RAM':'&order=relevance&gtmTitle=Memorias%20RAM&idFamilies%5B%5D=7',
    'Laptops':'&order=relevance&gtmTitle=Port%C3%A1tiles&idFamilies%5B%5D=1115',
    'GamingLaptops':'&order=relevance&gtmTitle=Port%C3%A1tiles%20Gaming&idFamilies%5B%5D=1115',
    'Smartphones':'&order=relevance&gtmTitle=M%C3%B3viles%20libres%20y%20Smartphones&idFamilies%5B%5D=1116',
    'TVs':'&order=relevance&gtmTitle=Televisores&idFamilies%5B%5D=1179'
}

#Temporal method until we can insert data in the Database
#Whoosh
def indexWhoosh(category):
    schema = Schema(brand=TEXT(stored=True), title=TEXT(stored=True), category=TEXT(stored=True, sortable=True), price=NUMERIC(Decimal,decimal_places=2,sortable=True))
    
    if not os.path.exists("whooshdir"):
        os.mkdir("whooshdir")
    ix = create_in("whooshdir",schema)
    writer = ix.writer()

    def scrapeAndIndexProductsByCategory(category):
        category_page = category_map[category]
        npages = 0
        i = 0
        #Max refreshes whenever a page has articles
        max = 1

        while i<max:
            #The first page index = 0
            #Ej: https://www.pccomponentes.com/listado/ajax?page=3&order=relevance&gtmTitle=Tarjetas%20Gr%C3%A1ficas&idFamilies%5B%5D=6
            actual_page = "https://www.pccomponentes.com/listado/ajax?page=" + str(i) + category_page
            req = Request(actual_page, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, "lxml")
            i = i+1
            l = soup.find_all("article", class_="tarjeta-articulo")
            if len(l)!=0:
                npages = npages+1
                print("Page: "+str(i-1))        
                max = max+1
                for a in l:
                    sku = a.find_all("meta", itemprop="sku")[0]["content"]
                    print("SKU: " + sku)

                    brand = a.find_all("meta", itemprop="brand")[0]["content"]
                    print("BRAND: " + brand)

                    image = a.find_all("img", itemprop="image")[0]["src"]
                    imageUrl = "https:" + str(image)
                    print("IMAGE: " + imageUrl)

                    name = a.find_all("a", itemprop="url")[0]["data-name"]
                    print("NAME: " + name)

                    category = a.find_all("a", itemprop="url")[0]["data-category"]
                    print("CATEGORY: " + category)

                    currentPrice = a.find_all("a", itemprop="url")[0]["data-price"]
                    print("CURRENT PRICE: " + currentPrice)

                    originalPrice = a.find_all("meta", itemprop="price")[0]["content"]
                    print("ORIGINAL PRICE: " + originalPrice)

                    writer.add_document(brand=brand, title=name, category=category, price=originalPrice)

                    print("-----------------------")
            else:
                print("There is no more products for this category, pages registered in total: {}".format(npages))
                print("-----------------------")

    scrapeAndIndexProductsByCategory(category)
    writer.commit()

def scrapeAndIndexAllProducts():
    start_time = time.perf_counter()
    start_cpu = time.process_time()

    for category in category_map:
        indexWhoosh(category)

    end_time = time.perf_counter()
    end_cpu = time.process_time()

    #Time spent in total
    print("Elapsed time: {0:.3f} (s)".format(end_time-start_time))
    #Time spent only CPU    
    print("CPU process time: {0:.3f} (s)".format(end_cpu-start_cpu))

scrapeAndIndexAllProducts()