from collections import deque
from locations import location
# time = minutes after 12 AM

def dist(loc1, loc2): # distance between two coordinates -- * 70 because small values
    return 70 * (abs(loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1]))

def weight_path(locations, start_loc, end_loc, time, hungry):
    # find the weight of the distance
    dist_weight = dist(start_loc.loc, end_loc.loc) * 50
    time_weight = 0
    # return -1 if the open time is later than the time
    if (time <= end_loc.open_time):
        return -1
    # return -2 if the close time is earlier than the time
    if (time + end_loc.avg_time >= end_loc.close_time):
        return -2
    # reduce weight if the person is hungry
    if hungry and 'food' in end_loc.category:
      dist_weight = dist_weight//5
    # if the person is hungry and the desired location is not a restaurant, increase the weight
    if not hungry and 'food' in end_loc.category or hungry and 'food' not in end_loc.category:
      dist_weight = dist_weight*5
    return dist_weight + time_weight

def remove_from_dict(dict, n):
    # used to remove every instance of a location from the location dictionary
    result = {}
    currentList = []
    x = n[0]
    for key, value in dict.items():
        if key == x:
          continue
        else:
          for loc in value:
            if loc != x:
              currentList.append(loc)
        result[key] = currentList.copy()
        currentList = []
    for loc in n:
      for key, value in list(result.items()).copy():
        if key == loc:
          result.pop(key)
          continue
        if loc in value:
          result[key].remove(loc)
    return result

def nearest_n(locations, loc, n):
    # return the n nearest locations to the loc.
    nearest = []
    for l in locations:
        if l != loc:
            nearest.append((dist(loc.loc, l.loc), l))
    nearest = sorted(nearest, key=lambda t: t[0])
    if n > len(nearest):
      n = len(nearest)
    return [l for d, l in nearest[:n]]

def create_nodes(locations, n):
  # creates dictionary of locations
  output = {}
  for loc in locations:
    output[loc] = nearest_n(locations, loc, n)
  return output

def find_paths(start, graph, n):
    # finds all possible paths of length n
    paths = []
    queue = deque([(start, [start])])
    while queue:
        vertex, path = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor in path:
                continue
            new_path = path + [neighbor]
            paths.append(new_path)
            queue.append((neighbor, new_path))
    return [path for path in paths if len(path) == n+1]

def best_path(start, graph, n, start_time, downtime):
  ## add option to specify how long of breaks they want in between stuff, right now it does everything back to back
  weights = []
  last_time_eaten = start_time
  hungry = True
  time = start_time
  temp_weight = 0
  temp_downtime = downtime
  arrival_times = []
  breaks = False
  for path in find_paths(start, graph, n):
    # reset all variables
    arrival_times = []
    last_time_eaten = start_time
    hungry = True
    time = start_time
    temp_weight = 0
    temp_downtime = downtime
    breaks = False
    for i in range(len(path)-1):
      # if it's been two hours since they've last eaten, make 'hungry' boolean true
      if time >= last_time_eaten + 120:
        hungry = True
      # define the two locations to weigh
      start_loc = path[i]
      end_loc = path[i+1]
      # make the weight between the paths
      weight = weight_path(graph, start_loc, end_loc, time, hungry)
      # if the times don't work, see if there's available downtime to use
      # if there is, use the downtime, if not, break the loop to not continue the path
      if weight == -1:
        if end_loc.open_time - time > temp_downtime:
          breaks = True
        else:
          temp_downtime -= (end_loc.open_time - time)
          time = end_loc.open_time
      # if time is past closing time downtime can't be used -- path doesn't work
      if weight == -2:
        breaks = True
      # add this weight to the path's weight
      temp_weight += weight
      # if the place was a restaurant, make the 'hungry' boolean false and reset the last time eaten
      if 'food' in end_loc.category:
        hungry = False
        last_time_eaten = time
      # add what time you arrived to the location
      arrival_times.append(time)
      time += path[i+1].avg_time
    # if the times work, add everything to the weights list
    if not breaks:
        weights.append((temp_weight, path, time, downtime - temp_downtime, arrival_times.copy()))
  n = 0
  output = []
  # output the 3 lowest weighted paths
  for v, path, time, downtime_used, arrival_times in sorted(weights, key=lambda weights: weights[0]):
    if n >= 3:
      break
    output.append((v, path, time, downtime_used, arrival_times))
    n += 1
  return output

def best_path2(start, graph, days, start_time, downtime):
  # does the best_path for each day
  output = []
  path_length = len(graph)//days
  for i in range(days):
    # loops best_path for each day
    path_ = best_path(start, graph, path_length, start_time, downtime)
    # if the path doesn't work, end loop and return output
    if not path_:
      break
    else:
      path = path_[0]
    output.append(path)
    graph = remove_from_dict(graph, path[1][1:])
  return output

  
# Chicago Skyline
chicago_skyline = location("Chicago Skyline", (41.8781, -87.6298), 360, 1080, 60, 0, ["attraction"], 1)

# Art Institute of Chicago
art_institute = location("Art Institute of Chicago", (41.8796, -87.6237), 360, 1080, 120, 25, ["museum"], 2)

# Willis Tower
willis_tower = location("Willis Tower", (41.8786, -87.6359), 360, 1080, 60, 25, ["attraction"], 3)

# Millennium Park
millennium_park = location("Millennium Park", (41.8825, -87.6228), 360, 1080, 120, 0, ["park"], 4)

# Navy Pier
navy_pier = location("Navy Pier", (41.8902, -87.6075), 360, 1080, 120, 0, ["attraction"], 5)

# The Field Museum
field_museum = location("The Field Museum", (41.8661, -87.6167), 360, 1080, 120, 25, ["museum"], 6)

# Shedd Aquarium
shedd_aquarium = location("Shedd Aquarium", (41.8676, -87.6157), 360, 1080, 120, 39, ["aquarium"], 7)

# The Art of Pizza
the_art_of_pizza = location("The Art of Pizza", (41.9396, -87.6554), 420, 1020, 45, 15, ["pizza", "food"], 8)

# The Chicago Theatre
the_chicago_theatre = location("The Chicago Theatre", (41.8847, -87.6366), 360, 1080, 60, 80, ["theater"], 9)

# The Lincoln Park Zoo
the_lincoln_park_zoo = location("The Lincoln Park Zoo", (41.9213, -87.6375), 360, 1080, 120, 0, ["zoo", "park"], 10)

# Create a list of the locations
locations = [chicago_skyline, art_institute, willis_tower, millennium_park, navy_pier, field_museum, shedd_aquarium, the_art_of_pizza, the_chicago_theatre, the_lincoln_park_zoo]

# Create a dictionary representing the graph of locations where the keys are the location objects and the values are lists of the 4 nearest location objects to each key
# The Wildberry Pancakes and Cafe (breakfast)
wildberry_pancakes = location("The Wildberry Pancakes and Cafe", (41.8868, -87.6261), 360, 1080, 60, 15, ["breakfast", "food"], 11)

# Yolk (breakfast)
yolk = location("Yolk", (41.8899, -87.6341), 360, 1080, 60, 15, ["breakfast", "food"], 12)

# Portillo's (lunch)
portillos = location("Portillo's", (41.8793, -87.6298), 360, 1080, 60, 15, ["lunch", "food"], 13)

# Giordano's (lunch)
giordanos = location("Giordano's", (41.8848, -87.6276), 360, 1080, 60, 15, ["lunch", "food"], 14)

# Lou Malnati's (dinner)
lou_malnatis = location("Lou Malnati's", (41.8899, -87.6341), 360, 1080, 60, 15, ["dinner", "food"], 15)

# Al's Beef (dinner)
als_beef = location("Al's Beef", (41.8778, -87.6256), 360, 1080, 60, 15, ["dinner", "food"], 16)

restaurants = [wildberry_pancakes, yolk, portillos, giordanos, lou_malnatis, als_beef]

graph_chicago = create_nodes(locations + restaurants, 7)
p = {}
x = best_path2(willis_tower, graph_chicago, 3, 540, 180)
for path in x:
    print('weight=', path[0])
    p = remove_from_dict(graph_chicago, path[1])
    for loc in path[1]:
      print('loc =', loc)
    print('downtime used =', path[3])
    print('finishing time =', path[2])
    print('arrival times =', path[4])
    print('\n')

   
