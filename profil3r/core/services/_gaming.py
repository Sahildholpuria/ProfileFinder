from profil3r.modules.gaming.steam import Steam

# Steam
def steam(self):
    self.result["steam"] = Steam(self.config, self.permutations_list).search()
    # print results
    self.print_results("steam")