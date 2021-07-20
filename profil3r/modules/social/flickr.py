import requests
from bs4 import BeautifulSoup
import time
import re

class Flickr:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['flickr']['rate_limit'] / 1000
        # https://flickr.com/photos/{username}
        self.format = config['plateform']['flickr']['format']
        self.permutations_list = permutations_list
        # social
        self.type = config['plateform']['flickr']['type']

    # Generate all potential flickr usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        flickr_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to flickr")
            
            # If the account exists
            if r.status_code == 200:
                # Account object
                account = {}

                # Get the username
                account["value"] = username
                
                # Parse HTML response content with beautiful soup 
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Scrape the user informations
                try:
                    user_username = str(soup.find_all("div", {"class": "title"})[0].find_all("h1")[0].get_text().strip()) if soup.find_all("div", {"class": "title"}) else None
                    user_pictures_count = str(soup.find_all("p", {"class": "photo-count"})[0].get_text().split(' ')[0].replace(',', '')) if soup.find_all("p", {"class": "photo-count"}) else None
                    
                    followers = str(soup.find_all("p", {"class": "followers"})[0].get_text()) if soup.find_all("p", {"class": "followers"}) else None
                    user_followers_count = followers.split(' ')[0]
                    user_following_count = followers.split(' ')[1].split('•')[1]

                    account["username"] = {"name": "Username", "value": user_username}
                    account["following_count"] = {"name": "Following", "value": user_following_count}
                    account["followers_count"] = {"name": "Followers", "value": user_followers_count}
                    account["pictures_count"] = {"name": "Pictures", "value": user_pictures_count}
                except:
                    pass
                
                # Append the account to the accounts table
                flickr_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return flickr_usernames