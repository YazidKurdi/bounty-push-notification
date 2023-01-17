import os
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from push_bullet import push_notification
from github import Github

# Authenticate yourself
g = Github("YazidKurdi", os.getenv("GIT_API"))

# Find your repository and path of README.md
repo = g.get_user().get_repo("bounty-push-notification")

def run_script():

    # URL of the webpage to monitor
    url = 'https://replit.com/bounties?order=creationDateDescending'

    # check if previous hash file exist
    try:
        file = repo.get_contents("previous_hash.txt")
        previous_hash = file.decoded_content.decode()
    except:
        pass

    # Make an HTTP GET request to the webpage
    response = requests.get(url)

    # Extract the HTML content of the webpage
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the 5th <li> element on the page
    fifth_li = soup.find_all('li')[4].find("h3")

    # Calculate the hash of the HTML content
    hash_object = hashlib.sha1(fifth_li.encode())
    current_hash = hash_object.hexdigest()

    # Compare the current hash with the previous hash
    if current_hash != previous_hash:
        push_notification("New Bounty!",fifth_li.text)

        # The new contents of your README.md
        previous_hash = current_hash

        # Update README.md
        repo.update_file("previous_hash.txt", "commit message", previous_hash, file.sha)

    else:
        print(f"Webpage has not been updated. {datetime.now().time()}")


if __name__ == "__main__":
    run_script()