import requests
import config
import sys


def searchphotos(query):
	endpoint = "https://api.unsplash.com/search/photos"
	page = 0
	actual_url = endpoint+"?page="+str(page)+"&query="+query+"&"+"client_id="+config.client_id
	
	r_data = requests.get(actual_url)
	r_dict = r_data.json()
	default_pages = r_dict['total_pages']
	count = 0
	while(default_pages!=0):
		count += 10
		actual_url = endpoint+"?page="+str(page)+"&query="+query+"&"+"client_id="+config.client_id
		r_data = requests.get(actual_url)
		r_dict = r_data.json()
		if(count>100):
			break
		for i in range(10):
			image_url = r_dict['results'][i]['urls']['full']
			print(image_url)
			page += 1




if __name__ == '__main__':
	query = input("What do you want to search?")
	searchphotos(query)
