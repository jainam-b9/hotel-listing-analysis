import time

from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.booking.com/searchresults.en-gb.html?ss=New+York&ssne=New+York&ssne_untouched=New+York&checkin=2024-08-29&checkout=2024-08-29&group_adults=1&no_rooms=1&group_children=0&selected_currency=USD"
# Load selenium webdriver with the url
driver = webdriver.Safari()
driver.get(url)
driver.maximize_window()

# Give some time for the browser to load the content
time.sleep(5)
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
        lastCount = lenOfPage
        time.sleep(5)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
# Get the website content from selenium browser window and load the # content in BeautifulSoup library to parse the content
soup = BeautifulSoup(driver.page_source, 'html')
driver.quit()

# Find all the hotel elements in the HTML document
hotels = soup.findAll('div', {'data-testid': 'property-card'})

hotels_data = []
# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('div', {'data-testid': 'title'})
    name = name_element.text.strip()

    # Extract the hotel location
    location_element = hotel.find('span', {'data-testid': 'address'})
    location = location_element.text.strip()

    # Extract the hotel price
    price_element = hotel.find('span', {'data-testid': 'price-and-discounted-price'})
    price = None
    if price_element is not None:
        price = price_element.text.strip()

    # Extract the star rating
    star_rating_element = hotel.find('div', {'class': 'a1f6e6bc06'})
    star_rating = 0
    if star_rating_element is not None:
        star_rating = len(hotel.find('div', {'class': 'a1f6e6bc06'}).contents)

    # Extract the hotel rating
    rating_element = hotel.find('div', {'class': 'd0522b0cca fd44f541d8'})
    rating = 0
    if rating_element is not None:
        rating = rating_element.text.strip().split(' ')[1]

    # Extract the review count
    review_element = hotel.find('div', {'class': 'e8acaa0d22 ab107395cb c60bada9e4'})
    review_count = 0
    if review_element is not None:
        review_count = review_element.text.strip()

    hotel_page_link_element = hotel.find('a', {'class': 'f0ebe87f68', 'data-testid': 'title-link'})
    hotel_page_link =  hotel_page_link_element['href']
    # Append hotes_data with info about hotel
    hotels_data.append({
        'name': name,
        'location': location,
        'price': price,
        'rating': rating,
        'star_rating': star_rating,
        'review_count': review_count,
        'hotel_page_link': hotel_page_link
    })

# with open('booking_data.json', 'r') as file:
#     booking_data = file.read().replace('\n', '')
#
# booking_data = json.loads(booking_data)
# hotel_data = {}
# final_hotel_list = []
# for dict in booking_data:
#     for key, value in dict.items():
#         if key == 'hotel_page_link':
#             url = value + '&no_rooms=1&origin=hp&sb_price_type=total&src=hotel&type=total&#group_recommendation'# Load selenium webdriver with the url
#             driver = webdriver.Safari()
#             driver.get(url)
#             driver.maximize_window()
#             # Give some time for the browser to load the content
#             time.sleep(5)
#             lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#             match=False
#             while(match==False):
#                     lastCount = lenOfPage
#                     lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#                     time.sleep(5)
#                     if lastCount==lenOfPage:
#                         match=True
#             # Get the website content from selenium browser window and load the # content in BeautifulSoup library to parse the content
#             time.sleep(2)
#             soup = BeautifulSoup(driver.page_source, 'html')
#             driver.quit()
#             rooms_available = soup.findAll(
#                 lambda t: t.name == 'option' and t.parent.attrs.get('data-component') == 'hotel/new-rooms-table/select-rooms'
#             )
#             hotel_data = dict.copy()
#             if rooms_available is not None:
#                 hotel_data['rooms_available'] = len(rooms_available)
#             else:
#                 hotel_data['rooms_available'] = 0
#             final_hotel_list.append(hotel_data)
#             time.sleep(1)
#             # print the HTML as text
#
# with open('booking_data.json', 'w') as f:
#     json.dump(final_hotel_list, f)
