from profil3r.modules.medias.medium import Medium

# Medium
def medium(self):
    self.result["medium"] = Medium(self.config, self.permutations_list).search()
    # print results
    self.print_results("medium")