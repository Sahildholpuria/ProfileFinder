from profil3r.modules.collaborative.wikipedia import Wikipedia

# Wikipedia
def wikipedia(self):
    self.result["wikipedia"] = Wikipedia(self.config, self.permutations_list).search()
    # print results
    self.print_results("wikipedia")