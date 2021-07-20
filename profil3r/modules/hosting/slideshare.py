import requests
from bs4 import BeautifulSoup
import time

class SlideShare:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['slideshare']['rate_limit'] / 1000
        # https://slideshare.net/{username}
        self.format = config['plateform']['slideshare']['format']
        self.permutations_list = permutations_list
        # hosting
        self.type = config['plateform']['slideshare']['type']

    # Generate all potential slideshare usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        slideshare_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to slideshare")
            
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
                    user_username = str(soup.find_all("h1", {"itemprop":"name"})[0].get_text()).strip() if soup.find_all("h1", {"itemprop":"name"}) else None
                    user_slideshares_count = str(soup.find_all(class_="j-slideshare")[0].get_text()).strip().split(" ")[0] if soup.find_all(class_="j-slideshare") else None
                    user_followers_count = str(soup.find_all(class_="j-followers")[0].get_text()).strip().split(" ")[0] if soup.find_all(class_="j-followers") else None
                    user_location = str(soup.find_all(class_="location")[0].get_text()).strip() if soup.find_all(class_="location") else None
                    user_clipboards = str(soup.find_all(class_="user-clipboards")[0].get_text()).strip().split(" ")[0] if soup.find_all(class_="user-clipboards") else None
                    user_role = str(soup.find_all(class_="role")[0].get_text()).strip() if soup.find_all(class_="role") else None
                    user_description = str(soup.find_all(class_="description")[0].get_text()).strip().replace("\n", " ") if soup.find_all(class_="description") else None
                    user_website = str(soup.find_all(class_="web")[0].get_text().replace("\n", " ")).strip() if soup.find_all(class_="web") else None
                    user_twitter = str(soup.find_all(class_="twitter")[0]['href']).strip() if soup.find_all(class_="twitter") else None
                    user_linkedin = str(soup.find_all(class_="linkedin")[0]['href']).strip() if soup.find_all(class_="linkedin") else None

                    account["username"] = {"name": "Username", "value": user_username}
                    account["slideshares_count"] = {"name": "Slideshares", "value": user_slideshares_count}
                    account["followers_count"] = {"name": "Followers", "value": user_followers_count}
                    account["location"] = {"name": "Location", "value": user_location}
                    account["clipboards_count"] = {"name": "Clipboards", "value": user_clipboards}
                    account["role"] = {"name": "Role", "value": user_role}
                    account["description"] = {"name": "Description", "value": user_description}
                    account["website"] = {"name": "Website", "value": user_website}
                    account["twitter"] = {"name": "Twitter", "value": user_twitter}
                    account["linkedin"] = {"name": "Linkedin", "value": user_linkedin}

                except:
                    pass
                
                # Append the account to the accounts table
                slideshare_usernames["accounts"].append(account)

            time.sleep(self.delay)
        
        return slideshare_usernames