#!usr/bin/python

from requests_oauthlib import OAuth1Session
import requests
import config


def getList(url):
	client_id = "a235801b84ae3057163a384548acbb74f82dfc72ee2e8e9580637271ea1a7858"
	client_secret = "40fdf55a363dce20ef5475cd65938cffa1b7ec82a7c7cb3a58eb77fa9405ac53"
	list1 = url.split('/')
	id = list1[-1]
	endpoint = "https://api.unsplash.com/collections/"
	actual_url = endpoint+id+"/photos"+"?"+"client_id="+client_id

	token = OAuth1Session(client_id,client_secret)
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
