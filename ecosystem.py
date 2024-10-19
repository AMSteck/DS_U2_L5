import random
from colorama import Fore
G = Fore.GREEN
B = Fore.LIGHTBLUE_EX
C = Fore.LIGHTCYAN_EX
W = Fore.RESET
class River:
  def __init__(self, size, num_bears, num_fish):
    self.river = [[" "]*size for i in range(size)]
    self.size = size
    self.num_bears = num_bears
    self.num_fish = num_fish
    self.animals = []
    self.population = 0

  def __str__(self): 
    output = f"{G}෴⚘෴⚘𓋼𓍊෴𓍊𓋼෴⚘𓍊𓋼෴𓆑෴⚘෴⚘𓋼𓍊෴𓍊𓋼෴⚘𓍊𓋼෴𓆑\n"
    output +=f"{C}𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃{B}\n\n"
    for row in self.river:
      for spot in row:
        output += f"𓂃{spot}"
      output+="\n"
    output +=f"\n{C}𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃𓂃\n"
    output += f"{G}෴⚘෴⚘𓋼𓍊෴𓍊𓋼෴⚘𓍊𓋼෴𓆑෴⚘෴⚘𓋼𓍊෴𓍊𓋼෴⚘𓍊𓋼෴𓆑{W}\n"
    return output

  def place_baby(self, species):
    empty = False
    while empty == False:
      xAxis = random.randint(0,self.size-1)
      yAxis = random.randint(0,self.size-1)
      if self.river[xAxis][yAxis] == " ":
        taken = False
        for animal in self.animals:
          if animal.x == xAxis and animal.y == yAxis:
            taken = True
        if taken == False:
          empty = True
          
    if species == Fish:
      X = Fish(xAxis,yAxis)
      self.num_fish += 1
    else:
      X = Bear(xAxis,yAxis)
      self.num_bears += 1
    self.animals.append(X)
    self.population += 1

  def animal_death(self, dyingAnimal):
    if dyingAnimal in self.animals:
      self.animals.remove(dyingAnimal)
    if dyingAnimal in self.river:
      self.river[animal.x][animal.y] = " "
    self.population -= 1
    if type(dyingAnimal) == Bear:
      self.num_bears -= 1
    else:
      self.num_fish -= 1


  def __getitem__(self, i):
    return self.river[i]

  def __initial_population(self): #do this thingy ma-bob first ////// create # of bears and fish, put in river. should probably be in new day method
    for bear in range(self.num_bears):
      xAxis = random.randint(0,self.size-1)
      yAxis = random.randint(0,self.size-1)
      B = Bear(xAxis,yAxis)
      self.animals.append(B)
      self.population += 1
    for fishy in range(self.num_fish):
      xAxis = random.randint(0,self.size-1)
      yAxis = random.randint(0,self.size-1)
      F = Fish(xAxis,yAxis)
      self.animals.append(F)
      self.population += 1

  def redraw_cells(self):
    for row in range(len(self.river)):
      for spot in range(len(self.river)):
        self.river[row][spot] = " "
    for animal in self.animals:
      self.river[animal.x][animal.y] = animal


  def new_day(self): #do this thingy ma-bob later
    if self.population == 0: #if inital population
      self.__initial_population()
    
    random.shuffle(self.animals) #shuffle list
    for animal in self.animals: # setting things up for the day
      animal.bred_today = False
      if type(animal) == Bear:
        animal.starve(self)
      animal.move(self.size, self)
      

    self.redraw_cells()
    if self.population >= self.size * self.size:
      return True, "The river is full."
    else:
      return False, None


class Animal:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.bred_today = False

  def move(self,riverSize, cur_riv):
    possibleMove = False
    while possibleMove == False:
      movementOpts  = ["north","north east","east","south east","south","south west","west","north west"]
      movement = {"north":(0,-1),"north east":(1,-1), "east":(1,0), "south east":(1,1),"south":(0,1),"south west":(-1,1), "west":(-1,0),"north west":(-1,-1)}
      direction = random.choice(movementOpts)
      xChange = movement[direction][0]
      yChange = movement[direction][1]
      newX = self.x + xChange
      newY = self.y + yChange
      if newX >= 0 and newX <= riverSize-1 and newY >= 0 and newY <= riverSize-1:
        possibleMove = True

    spot = cur_riv[newY][newX]
    if spot == " ":
      self.x = newX
      self.y = newY
    else:
      action = self.collision(spot, cur_riv)
      if action == "breed":
        cur_riv.place_baby(type(self)) 
      spot = cur_riv[newY][newX]
      if spot == " ":
        self.x = newX
        self.y = newY
        


  def collision(self, animalTwo, cur_riv):
    if type(animalTwo) == type(self):
      #breed
      if self.bred_today == False and animalTwo.bred_today == False:
        self.bred_today = True
        animalTwo.bred_today = True
        return "breed"
      else:
        print("An animal was excluded from breeding.")
    else:
      if type(self) == Fish:
        if self.life == False:
          pass
        else:
          animalTwo.consume(self, cur_riv) #consume fihs
      else:
        if animalTwo.life == False:
          pass
        else:
          self.consume(animalTwo,cur_riv)

  def death(self, cur_riv):
    cur_riv.animal_death(self)
   #calls river’s death method - send the animal object




class Fish(Animal): 
  def __init__(self,x,y):
    super().__init__(x,y)
    self.life = True

  def __str__(self):
    return "🐟"

class Bear(Animal):
  def __init__(self,x,y):
    super().__init__(x,y)
    self.max_lives = 9
    self.lives = self.max_lives
    self.eaten_today = False
  
  def __str__(self):
    return "🐻"

  def starve(self,cur_riv):
    if self.eaten_today == False:
      self.lives -= 1
    if self.lives == 0:
      print("An animal starved to death.")
      self.death(cur_riv)

  def consume(self, animal, cur_riv):
    print("An animal was consumed.")
    self.lives = self.max_lives
    animal.death(cur_riv)
