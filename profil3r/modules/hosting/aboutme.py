import requests
from bs4 import BeautifulSoup
import time

class AboutMe:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['aboutme']['rate_limit'] / 1000
        # https://about.me/{username}
        self.format = config['plateform']['aboutme']['format']
        self.permutations_list = permutations_list
        # hosting
        self.type = config['plateform']['aboutme']['type']

    # Generate all potential aboutme usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        aboutme_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to aboutme")
            
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
                    user_username = str(soup.find_all(class_="name")[0].get_text()).strip() if soup.find_all(class_="name") else None
                    user_location = str(soup.find_all(class_="location")[1].get_text()).strip() if soup.find_all(class_="location") else None
                    user_role = str(soup.find_all(class_="role")[0].get_text()).strip() if soup.find_all(class_="role") else None
                    user_description = str(soup.find_all(class_="short-bio")[0].get_text()).strip() if soup.find_all(class_="short-bio") else None

                    account["username"] = {"name": "Username", "value": user_username}
                    account["location"] = {"name": "Location", "value": user_location}
                    account["role"] = {"name": "Role", "value": user_role}
                    account["description"] = {"name": "Description", "value": user_description}
                except:
                    pass
                
                # Append the account to the accounts table
                aboutme_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return aboutme_usernames