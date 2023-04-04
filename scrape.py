from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_store_details(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'lxml')
    name = []
    store_address=[]
    contact_number = []
    time = []
    location = []

    #Scraping the store name
    tags = soup.find('div', class_='col-md-12 col-lg-4 col-block')
    store_name =tags.find('h1', class_='card-header heading')
    name.append(store_name.text)
    #print(f'store_name : {name}')

    #scraping the store address
    address = tags.find('li', class_='info-card info-address').find('div', class_='info-text')
    for text in address:
        street1 = text.text
        store_address.append(street1)
        pass
    for i in store_address:
        if i == '' or i ==' ':
            store_address.remove(i)
    result = ','.join(store_address)
    store_address.clear()
    store_address.append(result)
    #print(f'address : {store_address}')

    #scraping the store contact details
    contact = tags.find('a')
    contact_number.append((contact.text.strip()))
    #print(f'Contact : {contact_number}')

    #scraping the store timings 
    timings = soup.find('div', id='speakableBusinessHoursContent')
    hours = timings.find_all('span')
    for text in hours:
        time.append((text.text.strip()))
    result = ' '.join(time)
    time.clear()
    time.append(result)
    #print(f'timing : {time}')

    #scraping the store location co-ordinates
    loc = soup.find('div', id='speakablePluscodeContent').find('a')
    location.append(loc.text.strip())
    #print(f'co-ordinates : {location}')

    dictionary = {'Store_name':name, 'Contact_number':contact_number, 'Co-ordinates':location, 'Address':store_address, 'Timings':time}

    df = pd.DataFrame(dictionary)

    print(df)

    df.to_csv('retail_store_details.csv', index=False)


link = 'https://stores.lifestylestores.com/lifestyle-stores-shopping-centre-krishnaswamy-road-coimbatore-69223/Home?utm_source=locator&utm_medium=googleplaces'
get_store_details(link)