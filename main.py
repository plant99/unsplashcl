import os
import click
import requests
import json

# File with api keys
import config

current_dir = os.getcwd()

API_URI = "https://api.unsplash.com"

@click.group()
def cli():
    pass

# Command to download image
@click.command()
@click.option('--save', '-s', default=current_dir, help="Save location of image")
@click.option('--name', '-n', default="", help="Name for image")
@click.argument('photo_id')
def get(photo_id, save, name):
    try:
        url = f"{API_URI}/photos/{photo_id}?client_id={config.client_id}"
        res = requests.get(url)

        if res.status_code == 200:
            download_url = res.json()["urls"]["regular"]
            img_data = requests.get(download_url).content
            
            if (name == ""):
                name = photo_id + ".jpg"
            
            else:
                name += ".jpg"
            
            img_location = save + "/" + name
            with open(img_location, 'wb') as f:
                f.write(img_data)
                
            click.secho("Successfully Downloaded Image!", fg="green")

        elif res.status_code == 404:
            click.secho('Invalid Photo ID', fg="red")
        
        elif res.status_code == 401:
            click.secho('Invalid client ID', fg="red")
        
        else:
            click.secho('Some error occurred', fg="red")
    
    # In case of no internet connection
    except:
        click.secho('Could not download image', fg="red")

cli.add_command(get)

if __name__ == '__main__':
    cli()