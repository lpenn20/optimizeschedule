class location:
  def __init__(self, name, loc, open_time, close_time, avg_time, cost, category, num = None):
    ## change avg_time to time_spent (they can give input of time they want to spend at places)
    self.name = name
    self.loc = loc
    self.open_time = open_time
    self.close_time = close_time
    self.avg_time = avg_time
    self.cost = cost
    self.category = category
    self.num = num
  def __str__(self):
    return f'{self.name}, {self.loc}, {self.open_time}, {self.close_time}, {self.avg_time}, {self.cost}, {self.category}'