import requests
from bs4 import BeautifulSoup
import time

class LessWrong:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['lesswrong']['rate_limit'] / 1000
        # https://www.lesswrong.com/users/{username}
        self.format = config['plateform']['lesswrong']['format']
        # LessWrong usernames are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # forum
        self.type = config['plateform']['lesswrong']['type']

    # Generate all potential lesswrong usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        lesswrong_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to lesswrong")
            
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
                    user_username = str(soup.find_all(class_="UsersProfile-usernameTitle")[0].get_text()) if soup.find_all(class_="UsersProfile-usernameTitle") else None
                    user_bio = str(soup.find_all(class_="UsersProfile-bio")[0].get_text()) if soup.find_all(class_="UsersProfile-bio") else None

                    account["username"] = {"name": "Username", "value": user_username}
                    account["bio"] = {"name": "Bio", "value": user_bio}
                except:
                    pass
                
                # Append the account to the accounts table
                lesswrong_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return lesswrong_usernames