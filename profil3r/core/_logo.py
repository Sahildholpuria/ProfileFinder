from profil3r.core.colors import Colors

def print_logo(self):
    print(Colors.OKGREEN + Colors.BOLD + '''
   
 ____             __ _ _      _____ _           _           
|  _ \ _ __ ___  / _(_) | ___|  ___(_)_ __   __| | ___ _ __ 
| |_) | '__/ _ \| |_| | |/ _ \ |_  | | '_ \ / _` |/ _ \ '__|
|  __/| | | (_) |  _| | |  __/  _| | | | | | (_| |  __/ |   
|_|   |_|  \___/|_| |_|_|\___|_|   |_|_| |_|\__,_|\___|_|   
                                                            

                                       
''' + Colors.ENDC)

    print(Colors.HEADER + "Version {version} - Developped by Rog3rSm1th".format(version=self.version))
    print("You can buy me a coffee at : https://www.buymeacoffee.com/givocefo\n" + Colors.ENDC)