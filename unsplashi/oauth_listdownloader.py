#!usr/bin/python

from requests_oauthlib import OAuth1Session
import requests
import config


def getList(url):
	list1 = url.split('/')
	id = list1[-1]
	endpoint = "https://api.unsplash.com/collections/"
	actual_url = endpoint+id+"/photos"+"?"+"client_id="+config.client_id

	token = OAuth1Session(config.client_id,config.client_secret)
	r = token.get(actual_url)
	r_dict = r.json()

	for i in range(len(r_dict)):
			image_url=r_dict[i]['urls']['full']

			image = requests.get(image_url)

			with open('image'+str(i)+'.jpg','wb') as f:
				f.write(image.content)

if __name__ == '__main__':
	url = input("Give the collection URL with ID \nExample : https://unsplash.com/collections/2405765 \nURL:")
	getList(url)
