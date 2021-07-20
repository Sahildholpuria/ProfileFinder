import requests
from bs4 import BeautifulSoup
import time

class Twitter:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['tiktok']['rate_limit'] / 1000
        # https://twitter.com/{username}
        self.format = config['plateform']['twitter']['format']
        self.permutations_list = permutations_list

        # You can find more at https://github.com/zedeus/nitter/wiki/Instances
        self.nitter_URL = [
            "https://nitter.42l.fr/{}",
            "https://nitter.pussthecat.org/{}",
            "https://nitter.nixnet.services/{}",
            "https://nitter.tedomum.net/{}",
            "https://nitter.fdn.fr/{}",
            "https://nitter.kavin.rocks/{}",
            "https://tweet.lambda.dance/{}"
        ]

        #social
        self.type = config['plateform']['twitter']['type']

    # Generate all potential twitter usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    # Return a working nitter instance
    def get_nitter_instance(self):
        for nitter_instance in self.nitter_URL:
            # Test every nitter instance until we find a working one
            if requests.get(nitter_instance.format("pewdiepie")).status_code == 200:
                return nitter_instance

    def search(self):
        twitter_usernames = {
            "type": self.type,
            "accounts" : []
        }

        nitter_URL = self.get_nitter_instance()

        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                nitter_formatted_URL = nitter_URL.format(username.replace("https://twitter.com/", ""))
                r = requests.get(nitter_formatted_URL)
            except requests.ConnectionError:
                print("failed to connect to twitter")
            
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
                    user_full_name = str(soup.find_all(class_='profile-card-fullname')[0].get_text()).strip() if soup.find_all(class_='profile-card-fullname') else None
                    user_username = str(soup.find_all(class_='profile-card-username')[0].get_text()).strip() if soup.find_all(class_='profile-card-username') else None
                    user_bio = str(soup.find_all(class_='profile-bio')[0].get_text()).replace("\n", "").strip() if soup.find_all(class_='profile-bio') else None
                    user_tweets_count = str(soup.find_all(class_='profile-stat-num')[0].get_text().replace(",", "")).strip() if soup.find_all(class_='profile-stat-num') else None
                    user_following_count = str(soup.find_all(class_='profile-stat-num')[1].get_text().replace(",", "")) if soup.find_all(class_='profile-stat-num') else None
                    user_followers_count = str(soup.find_all(class_='profile-stat-num')[2].get_text().replace(",", "")).strip() if soup.find_all(class_='profile-stat-num') else None
                    user_likes_count = str(soup.find_all(class_='profile-stat-num')[3].get_text().replace(",", "")).strip() if soup.find_all(class_='profile-stat-num') else None

                    account["full_name"] = {"name": "Full Name", "value": user_full_name}
                    account["username"] = {"name": "Username", "value": user_username}
                    account["bio"] = {"name": "Bio", "value": user_bio}
                    account["tweets_count"] = {"name": "Tweets", "value": user_tweets_count}
                    account["following_count"] = {"name": "Following", "value": user_following_count}
                    account["followers_count"] = {"name": "Followers", "value": user_followers_count}
                    account["likes_count"] = {"name": "Likes", "value": user_likes_count}
                except:
                    pass
                
                # Append the account to the accounts table
                twitter_usernames["accounts"].append(account)

            time.sleep(self.delay)

        return twitter_usernames