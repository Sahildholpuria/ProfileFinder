import requests
from bs4 import BeautifulSoup
import time

class Pornhub:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['pornhub']['rate_limit'] / 1000
        # https://pornhub.com/users/{username}
        self.format = config['plateform']['pornhub']['format']
        # pornhub usernames are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # porn
        self.type = config['plateform']['pornhub']['type']

    # Generate all potential pornhub usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        pornhub_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to pornhub")
            
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
                    user_followers = str(soup.find_all(class_="subViewsInfoContainer")[0].find_all(class_="number")[0].get_text()).strip() if soup.find_all(class_="subViewsInfoContainer") else None
                    user_friends = str(soup.find_all(class_="subViewsInfoContainer")[0].find_all(class_="number")[1].get_text()).strip() if soup.find_all(class_="subViewsInfoContainer") else None
                    user_watch_count = str(soup.find_all(class_="subViewsInfoContainer")[0].find_all(class_="number")[2].get_text()).strip() if soup.find_all(class_="subViewsInfoContainer") else None

                    account["followers"] = {"name": "Followers", "value": user_followers}
                    account["friends"] = {"name": "Friends", "value": user_friends}
                    account["watch_count"] = {"name": "Watched Videos", "value": user_watch_count}
                except:
                    pass
                
                # Append the account to the accounts table
                pornhub_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return pornhub_usernames