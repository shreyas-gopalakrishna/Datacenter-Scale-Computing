from __future__ import print_function
import requests
import json

addr = 'http://localhost:5000'

# prepare headers for http request
headers = {'content-type': 'image/png'}
img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
# send http request with image and receive response
image_url = addr + '/api/image'
response = requests.post(image_url, data=img, headers=headers)
# decode response
print("Response is", response)
print(json.loads(response.text))