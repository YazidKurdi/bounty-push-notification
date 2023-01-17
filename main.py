import os
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from push_bullet import push_notification


def run_script():

    # URL of the webpage to monitor
    url = 'https://replit.com/bounties?order=creationDateDescending'

    # check if previous hash file exist
    if os.path.exists("previous_hash.txt"):
        with open("previous_hash.txt", "r") as f:
            previous_hash = f.read()
    else:
        previous_hash = None

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
        # print(f"Webpage has been updated! {datetime.now().time()}")
        push_notification("New Bounty!",fifth_li.text)

        # Store the current hash as the previous hash for the next comparison
        with open("previous_hash.txt", "w") as f:
            f.write(current_hash)
    else:
        print(f"Webpage has not been updated. {datetime.now().time()}")


if __name__ == "__main__":
    run_script()