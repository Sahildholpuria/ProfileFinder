import requests
import time

class DeviantArt:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['deviantart']['rate_limit'] / 1000
        # https://www.deviantart.com/{username}
        self.format = config['plateform']['deviantart']['format']
        # deviantart usernames are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # entertainment
        self.type = config['plateform']['deviantart']['type']

    # Generate all potential deviantart usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        deviantart_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to deviantart")
            
            # If the account exists
            if r.status_code == 200:
                deviantart_usernames["accounts"].append({"value": username})

            time.sleep(self.delay)
        
        return deviantart_usernames