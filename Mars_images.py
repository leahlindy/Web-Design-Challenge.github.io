#Dependencies
import requests
from datetime import datetime
from api_key import nasa_key
import Martian_API

print(numerical_dates)

# use Insight API (Martian file) again for dates (for up-to-date images)
base_url= 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?'
image_src=[]

for sol in numerical_dates:
    earth_date = sol
    query_url = f'{base_url}sol={earth_date}&api_key={nasa_key}'
    mars_response = requests.get(query_url)
    mars_json=mars_response.json()
    try:
        image_link= mars_json['photos'][0]['img_src']
        image_src.append(image_link)
    except IndexError:
        pass

print(image_src)

# write image url to separate files
try:
    file1 = open("Resources/image_1.py","w") 
    file1.write(image_src[0])

    file2 = open("Resources/image_2.py","w") 
    file2.write(image_src[1])

    file3 = open("Resources/image_3.py","w") 
    file3.write(image_src[2])

    file4 = open("Resources/image_4.py","w") 
    file4.write(image_src[3])

    file5 = open("Resources/image_5.py","w") 
    file5.write(image_src[4])

    file6 = open("Resources/image_6.py","w") 
    file6.write(image_src[5])

    file7 = open("Resources/image_7.py","w") 
    file7.write(image_src[6])

except IndexError:
    pass

