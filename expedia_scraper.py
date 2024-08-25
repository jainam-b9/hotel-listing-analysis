
import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver

# modify the url based from, to location and date of travel
url = "https://www.expedia.com/Hotel-Search?destination=New%20York%20%28and%20vicinity%29%2C%20New%20York%2C%20United%20States%20of%20America&regionId=178293&latLong=40.75668%2C-73.98647&flexibility=0_DAY&d1=2024-09-04&startDate=2024-09-04&d2=2024-09-05&endDate=2024-09-05&adults=1&rooms=1&theme=&userIntent=&semdtl=&useRewards=false&sort=RECOMMENDED"
# Load selenium webdriver with the url
driver = webdriver.Safari()
driver.get(url)
# Give some time for the browser to load the content
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    time.sleep(2)
    lastCount = lenOfPage
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True
soup = BeautifulSoup(driver.page_source, 'html')

# Get the website content from selenium browser window and load the # content in BeautifulSoup library to parse the content
driver.quit()
# Get all the data from response using the tags.
hotels = soup.find_all('div', attrs={'class': 'uitk-spacing uitk-spacing-margin-blockstart-three'})

hotels_data = []
# Loop over the hotel elements and extract the desired data
for hotel in hotels:
    # Extract the hotel name
    name_element = hotel.find('h3', {'class': 'uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start'})
    if name_element is not None:
        name = name_element.text.strip()

    # Extract the hotel location
    location_element = hotel.find('div', {'class': 'uitk-text uitk-text-spacing-half truncate-lines-2 uitk-type-300 uitk-text-default-theme'})
    if location_element is not None:
        location = location_element.text.strip()

    # Extract the hotel price
    price_element = hotel.find('div', {'class': 'uitk-text uitk-type-500 uitk-type-medium uitk-text-emphasis-theme'})
    if price_element is not None:
        price = price_element.text.strip()

    # Extract the star rating
    rating_element = hotel.find('span', {'class': 'uitk-badge-base-text', 'aria-hidden': 'true'})
    if rating_element is not None:
        rating = rating_element.text.strip()

    # Extract the review count
    rating_element = hotel.find('span', {'class': 'e8acaa0d22 ab107395cb c60bada9e4', 'aria-hidden': 'true'})
    if rating_element is not None:
        rating = rating_element.text.strip()

    # Extract the review count
    page_link_element = hotel.find('a', {'data-stid': 'open-hotel-information'})
    if page_link_element is not None:
        page_link = page_link_element['href']

    # Extract the review count
    review_element = hotel.find('span', {'class': 'uitk-text uitk-type-200 uitk-type-regular uitk-text-default-theme'})
    review_count = 0
    if review_element is not None:
        review_count = review_element.text.strip()
    # Append hotes_data with info about hotel
    hotels_data.append({
        'name': name,
        'location': location,
        'price': price,
        'rating': rating,
        'star_rating': 5,
        'review_count': review_count,
        'page_link': 'https://www.expedia.com'+page_link
    })

with open('expedia_data.json', 'w') as f:
    json.dump(hotels_data, f)



# with open('expedia_data.json', 'r') as file:
#     booking_data = file.read().replace('\n', '')
#
# booking_data = json.loads(booking_data)
# hotel_data = {}
# final_hotel_list = []
# for dict in booking_data:
#     for key, value in dict.items():
#         if key == 'page_link':
#             url = value
#             driver = webdriver.Safari()
#             driver.get(url)
#             driver.maximize_window()
#             # Give some time for the browser to load the content
#             myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.uitk-layout-flex.uitk-layout-flex-block-size-full-size.uitk-layout-flex-flex-direction-column.uitk-layout-flex-justify-content-space-between.uitk-card uitk-card-roundcorner-all.uitk-card-has-border.uitk-card-has-overflow.uitk-card-has-primary-theme')))
#
#             time.sleep(3)
#             lenOfPage = driver.execute_script("window.scrollTo(0, 1000);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#
#             # Get the website content from selenium browser window and load the # content in BeautifulSoup library to parse the content
#             soup = BeautifulSoup(driver.page_source, 'html')
#             driver.quit()
#             rooms_available = soup.findAll('div', {'class': 'uitk-layout-flex uitk-layout-flex-block-size-full-size uitk-layout-flex-flex-direction-column uitk-layout-flex-justify-content-space-between uitk-card uitk-card-roundcorner-all uitk-card-has-border uitk-card-has-overflow uitk-card-has-primary-theme'})
#             hotel_data = dict.copy()
#             if rooms_available is not None:
#                 hotel_data['rooms_available'] = len(rooms_available)
#             else:
#                 hotel_data['rooms_available'] = 0
#             final_hotel_list.append(hotel_data)
#             time.sleep(1)
            # print the HTML as text
#
# with open('expedia_data.json', 'w') as f:
#     json.dump(final_hotel_list, f)