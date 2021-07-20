import requests
import time

class Medium:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['medium']['rate_limit'] / 1000
        # https://medium.com/@{username}
        self.format = config['plateform']['medium']['format']
        self.permutations_list = permutations_list
        # medias
        self.type = config['plateform']['medium']['type']

    # Generate all potential medium usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        medium_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to medium")
            
            # If the account exists
            if r.status_code == 200:
                medium_usernames["accounts"].append({"value": username})

            time.sleep(self.delay)
        
        return medium_usernames