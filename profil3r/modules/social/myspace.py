import requests
from bs4 import BeautifulSoup
import time

class MySpace:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['myspace']['rate_limit'] / 1000
        # https://myspace.com/{username}
        self.format = config['plateform']['myspace']['format']
        self.permutations_list = permutations_list
        # social
        self.type = config['plateform']['myspace']['type']

    # Generate all potential myspace usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        myspace_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to myspace")
            
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
                    user_following_count = str(soup.find_all("div", {"id": "connectionsCount"})[0].find_all("span")[0].get_text().replace(",", "")) if soup.find_all("div", {"id": "connectionsCount"}) else None
                    user_followers_count = str(soup.find_all("div", {"id": "connectionsCount"})[0].find_all("span")[1].get_text().replace(",", "")) if soup.find_all("div", {"id": "connectionsCount"}) else None

                    account["following_count"] = {"name": "Following", "value": user_following_count}
                    account["followers_count"] = {"name": "Followers", "value": user_followers_count}
                except:
                    pass
                
                # Append the account to the accounts table
                myspace_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return myspace_usernames