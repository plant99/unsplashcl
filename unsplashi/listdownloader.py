import requests

def getList(url):
	client_id = "a235801b84ae3057163a384548acbb74f82dfc72ee2e8e9580637271ea1a7858"
	list1 = url.split('/')
	id = list1[-1]
	endpoint = "https://api.unsplash.com/collections/"
	actual_url = endpoint+id+"/photos"+"?"+"client_id="+client_id
	
	r_data = requests.get(actual_url)
	r_dict=r_data.json()
	for i in range(len(r_dict)):
		image_url=r_dict[i]['urls']['full']
		print(image_url)

		image = requests.get(image_url)

		with open('image'+str(i)+'.jpg','wb') as f:
			f.write(image.content)

	print("Download Completed !")

if __name__ == '__main__':
	url = input("Give the collection URL here: ")
	getList(url)
