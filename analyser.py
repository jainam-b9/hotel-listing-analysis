import pandas as pd
import json
import numpy as np


booking_data = None
expedia_data = None

with open('booking_data.json', 'r') as file:
    booking_data = file.read().replace('\n', '')
with open('expedia_data.json', 'r') as file:
    expedia_data = file.read().replace('\n', '')

expedia_data = pd.DataFrame.from_dict(json.loads(expedia_data))
booking_data = pd.DataFrame.from_dict(json.loads(booking_data))

expedia_data['rating'] = expedia_data['rating'].astype(float).fillna(0.0)
booking_data['rating'] = booking_data['rating'].astype(float).fillna(0.0)
expedia_data["price"] = expedia_data["price"].replace("[$,]", "", regex=True).astype(int)
booking_data["price"] = booking_data["price"].replace("[US$,]", "", regex=True).astype(int)

average_rating_on_expedia = expedia_data["rating"].mean()
average_rating_on_booking = booking_data["rating"].mean()

print(f'''average hotel rating on booking {average_rating_on_booking}''')
print(f'''average hotel rating on expedia {average_rating_on_expedia}\n''')

## booking > expedia

#price comparison
average_price_on_expedia = expedia_data["price"].mean()
average_price_on_booking = booking_data["price"].mean()

print(f'''average hotel price on booking {average_price_on_booking}''')
print(f'''average hotel price on expedia {average_price_on_expedia}\n''')

percentile_price_on_expedia = expedia_data["price"].quantile([0.0, .5, .90, .95])
percentile_price_on_booking = booking_data["price"].quantile([0.0, .5, .90, .95])

print(f'''90 percentile hotel price on booking {percentile_price_on_booking[0.90]}''')
print(f'''90 percentile hotel price on expedia {percentile_price_on_expedia[0.90]}\n''')

print(f'''number of hotels listed on booking {expedia_data['name'].count()}''')
print(f'''number of hotels listed on expedia {booking_data['name'].count()}\n''')

## average rating and average price on expedia is greater than that of booking, while 90 percentile of both is very close
## from a customer pov expedia seems to be a better deal

expedia_data["review_count"] = expedia_data["review_count"].replace("[ reviews]", "", regex=True).replace("[,]", "", regex=True).astype(int)
booking_data["review_count"] = booking_data["review_count"].replace("[ reviews]", "", regex=True).replace("[ external reviews]", "", regex=True).replace("[,]", "", regex=True).astype(int)

expedia_data['rating_to_reviews'] = expedia_data['rating'] / expedia_data['review_count']
booking_data['rating_to_reviews'] = booking_data['rating'] / booking_data['review_count']
expedia_data['rating_to_reviews'] = expedia_data['rating_to_reviews'].replace([np.inf, -np.inf], np.nan)
booking_data['rating_to_reviews'] = booking_data['rating_to_reviews'].replace([np.inf, -np.inf], np.nan)

#price comparison
average_rating_to_reviews_on_expedia = expedia_data["rating_to_reviews"].mean()
average_rating_to_reviews_on_booking = booking_data["rating_to_reviews"].mean()

print(f'''rating to reviews on booking {average_rating_to_reviews_on_booking}''')
print(f'''rating to reviews on expedia {average_rating_to_reviews_on_expedia}\n''')
# looks consistent across both the websites

expedia_data['rating_to_price'] = expedia_data['rating'] / expedia_data['price']
booking_data['rating_to_price'] = booking_data['rating'] / booking_data['price']
expedia_data['rating_to_price'] = expedia_data['rating_to_price'].replace([np.inf, -np.inf], np.nan)
booking_data['rating_to_price'] = booking_data['rating_to_price'].replace([np.inf, -np.inf], np.nan)

#price comparison
average_rating_to_reviews_on_expedia = expedia_data["rating_to_price"].mean()
average_rating_to_reviews_on_booking = booking_data["rating_to_price"].mean()

print(f'''rating to price on booking {average_rating_to_reviews_on_booking}''')
print(f'''rating to price on expedia {average_rating_to_reviews_on_expedia}''')

#expedia having more rating to price ratio, better deals for the customers
