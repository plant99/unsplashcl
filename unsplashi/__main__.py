import requests
import config

def getImage(url):
	list1 = url.split('/')
	id = list1[-1]
	endpoint = "https://api.unsplash.com/photos/"
	actual_url = endpoint+id+"?"+"client_id="+config.client_id
	
	r_data = requests.get(actual_url)
	r_dict=r_data.json()
	image_url=r_dict['urls']['full']

	image = requests.get(image_url)

	with open('image.jpg','wb') as f:
		f.write(image.content)

	print("Download Completed!")	

if __name__ == '__main__':
	url = input("Give the Image URL here: ")
	getImage(url)
