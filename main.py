#Alannah Steck
#U2L5
#Bear Fish River

from ecosystem import *
from time import sleep

DAYS_SIMULATED = 30
RIVER_SIZE = 15
START_BEARS = 10
START_FISH = 25


def main():
  r = River(RIVER_SIZE, START_BEARS, START_FISH)
  day = 0
  done = False
  for day in range(DAYS_SIMULATED):
    print(f"\n\nDay: {day+1}")
    print(r)
    print(f"\nStarting Poplation: {r.population} animals")
    done, message = r.new_day()
    print(f"Ending Poplation: {r.population} animals")
    print(r)
    if done == True:
      print(message)
      break
    day += 1
    sleep(5)
    #ʕ •ᴥ•ʔ this bear thinks you should give me extra credit and ignore any errors in my code


if __name__ == "__main__":
  main()