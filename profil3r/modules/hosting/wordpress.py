import requests
import time

class WordPress:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['wordpress']['rate_limit'] / 1000
        # https://{username}.wordpress.com
        self.format = config['plateform']['wordpress']['format']
        # wordpress usernames are not case sensitive
        self.permutations_list = permutations_list
        # hosting
        self.type = config['plateform']['wordpress']['type']

    # Generate all potential wordpress usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        wordpress_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to wordpress")
            
            # If the account exists
            if "Do you want to register" not in r.text:
                wordpress_usernames["accounts"].append({"value": username})

            time.sleep(self.delay)
        
        return wordpress_usernames