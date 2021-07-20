from profil3r.modules.travel.tripadvisor import TripAdvisor

# TripAdvisor
def tripadvisor(self):
    self.result["tripadvisor"] = TripAdvisor(self.config, self.permutations_list).search()
    # print results
    self.print_results("tripadvisor")