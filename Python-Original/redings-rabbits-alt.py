import random
import math

## Alternative version of "Reding's Rabbits" Natural Selection Simulator built on repl.it by Evan McCullough (2016)
## Alternative version adds in theoretical "climate shift" to compare favorability of traits in different climates/environments.
## Accessible and executable online at https://repl.it/@mr_mccullough/Redings-Rabbits-Alt

num_alb=10
num_brown=10
pct_dom = 50
pct_rec = 50
brown_death = 100
alb_death = 100
round_count = 1
alb_ct=1
ans_round = 0
shifted = False

pop = int(input("Enter a starting population size: "))
interval = int(input("Print out results every _ rounds: "))
brown_death = int(input("Please enter a brown rabbit mortality rate (%): "))
alb_death = int(input("Please enter an albino rabbit mortality rate (%): "))
num_alleles = pop * 2


while(num_alb>=2 and num_brown>=2):

  alleles = []
  rabbits = []

  #Distribute allele frequency over population
  num_brown = round((num_alleles*pct_dom)/100)
  num_alb = round((num_alleles*pct_rec)/100)

  # Picking the larger number of alleles in order to reduce run time. Not sure if this actually saves any time.
  largest_num = max(num_brown, num_alb)

  # Generating list of all alleles in the population. Theoretically alternates until the min(num_alb, num_brown) is reached, then it will only add the allele that occurs at greater frequency.
  for i in range(0,largest_num):
    if(i<num_brown):
      alleles.append('B')
    if(i<num_alb):
      alleles.append('b')

  for i in range(0, pop):
    curr_rab = [alleles.pop(random.randint(0,len(alleles)-1)), alleles.pop(random.randint(0,len(alleles)-1))]
    rabbits.append(curr_rab)

  albinos = []
  browns = []
  alb_kill_ct = 0
  brown_kill_ct = 0
  alb_ct = 0
  brown_ct = 0
  for rabbit in rabbits:
    #print("Alleles: ", rabbit[0], rabbit[1])
    if(rabbit[0]=='b' and rabbit[1]=='b'):
      alb_ct+=1
      albinos.append(rabbit)
    else:
      brown_ct+=1
      browns.append(rabbit)

  if(round_count%interval==0 or alb_ct==0):
    print("\nRound ", round_count, ":\n")
    print("Brown alleles- ", num_brown, " \nAlbino alleles- ", num_alb)
    print("Brown ct: ",len(browns), "Alb ct:", len(albinos))

  rec_tot = 0
  dom_tot = 0

  if(len(albinos)>1):
    alb_kill_ct = math.ceil(len(albinos)*(alb_death/100))
    for i in range(0, alb_kill_ct):
      #print("r", i, ";", alb_kill_ct)
      rabbits.remove(albinos.pop())
  elif(len(albinos)==1):
    alb_kill_ct=1
    rabbits.remove(albinos.pop())

  if(len(browns)>0):
    brown_kill_ct = math.ceil(len(browns)*(brown_death/100))
    for i in range(0, (brown_kill_ct)):
      rand_brown = random.choice(browns)
      rabbits.remove(rand_brown)
      browns.remove(rand_brown)

  # Go back through to get allele counts
  for rabbit in rabbits:
      if(rabbit[0]=='b'):
        rec_tot+=1
      else:
        dom_tot+=1
      if(rabbit[1]=='b'):
        rec_tot+=1
      else:
        dom_tot+=1

  if dom_tot != 0:
    pct_dom = ((dom_tot)/(dom_tot+rec_tot))*100
  pct_rec = ((rec_tot)/(dom_tot+rec_tot))*100
  num_brown = dom_tot
  num_alb = rec_tot

  if(round_count%interval==0 or alb_ct==0 or brown_ct==0):
    print("Brown Rabbits: ", brown_ct, "\nAlbino Rabbits: ", alb_ct, "\n", alb_kill_ct, " albinos die.\n", brown_kill_ct, " brown rabbits die.\nRemaining rabbits: ", len(rabbits))
    print("Dom alleles: ", dom_tot, "\nRec Alleles: ", rec_tot)
    print("Dom percent: ", pct_dom, "\nRec Percent: ", pct_rec)

  round_count+=1

  if(alb_ct==0 and rec_tot>=2 and shifted==False):
    ans = input("You are %d rounds in. There are no albino rabbits in the population, but there are enough alleles for another albino to theoretically be born. Institute climate shift? (Y/N) " %(round_count-1))
    if(ans.upper() == "Y"):
      shifted=True
      temp = alb_death
      alb_death = brown_death
      brown_death = temp
  #Nothing to see here


print(dom_tot)
if(rec_tot<=1):
  print("It took ", round_count-1, " rounds for all possibility for albino rabbits to disappear.")
elif(dom_tot<=1):
  print("The brown rabbit allele disappeared after %d generations." % (round_count-1))
