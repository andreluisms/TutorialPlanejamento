"""
The "travel from home to the park" example from my lectures.
Author: Dana Nau <nau@cs.umd.edu>, May 31, 2013
This file should work correctly in both Python 2.7 and Python 3.2.
"""

import pyhop

speed={'walk':3, 'taxi': 60, 'scooter': 30, 'bike': 10}

def taxi_rate(dist):
    return (1.5 + 0.5 * dist)

def travel_time(dist, mode):
    return dist/speed[mode]


def walk(state,a,x,y):
    if state.loc[a] == x:
        state.loc[a] = y
        state.time = state.time - travel_time(state.dist[x][y], 'walk') 
        return state
    else: return False

def pedal(state,a,x,y):
    if state.loc[a] == x:
        state.loc[a] = y
        state.time = state.time - travel_time(state.dist[x][y], 'bike')
        return state
    else: return False


def call_taxi(state,a,x):
    state.loc['taxi'] = x
    return state
    
def ride_taxi(state,a,x,y):
    if state.loc['taxi']==x and state.loc[a]==x:
        state.loc['taxi'] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        state.time = state.time - travel_time(state.dist[x][y], 'taxi')
        return state
    else: return False

def ride_scooter(state,a,x,y):
    if state.loc['scooter']==x and state.loc[a]==x:
        state.loc['scooter'] = y
        state.loc[a] = y
        state.time = state.time - travel_time(state.dist[x][y], 'scooter')
        return state
    else: return False

def pay_driver(state,a):
    if state.cash[a] >= state.owe[a]:
        state.cash[a] = state.cash[a] - state.owe[a]
        state.owe[a] = 0
        return state
    else: return False

def rent_scooter(state,a):
    if state.cash[a] >= 2:
        state.cash[a] = state.cash[a] - 2
        state.loc['scooter'] = 'scooterrental'
        return state
    else: return False

pyhop.declare_operators(walk, pedal, call_taxi, ride_taxi, ride_scooter, 
                        pay_driver, rent_scooter)
# print('')
# pyhop.print_operators()



def travel_by_foot(state,a,x,y):
    if state.dist[x][y] <= 2 and travel_time(state.dist[x][y], 'walk') <= state.time:
        return [('walk',a,x,y)]
    return False

def travel_by_bike(state,a,x,y):
    if state.dist[x][y] <= 10 and travel_time(state.dist[x][y], 'bike') <= state.time:
        return [('pedal',a,x,y)]
    return False

def travel_by_taxi(state,a,x,y):
    if state.cash[a] >= taxi_rate(state.dist[x][y]) and travel_time(state.dist[x][y], 'taxi') <= state.time:
        return [('call_taxi',a,x), ('ride_taxi',a,x,y), ('pay_driver',a)]
    return False

def travel_by_scooter(state,a,x,y):
    if state.cash[a] >= 2 and travel_time(state.dist[x][y], 'scooter') <= state.time:
        return [('travel',a, x, 'scooterrental'), ('rent_scooter',a), ('ride_scooter',a,'scooterrental',y), ]
    return False


pyhop.declare_methods('travel', travel_by_taxi, travel_by_foot, travel_by_bike, travel_by_scooter)
# print('')
# pyhop.print_methods()

state1 = pyhop.State('state1')
state1.loc = {'me':'home'}
state1.cash = {'me':20}
state1.owe = {'me':0}
state1.dist = {'home':{'park':8, 'scooterrental':1,'university':25}, 
                'park':{'home':8, 'scooterrental':7, 'university':15},
                'scooterrental':{'park':7, 'home':1, 'university':24}, 
                'university':{'park':15, 'home':25, 'scooterrental':24}}
state1.time = 0.2

# print("""
# ********************************************************************************
# Call pyhop.pyhop(state1,[('travel','me','home','park')]) with different verbosity levels
# ********************************************************************************
# """)

#print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
print(pyhop.pyhop(state1,[('travel','me','home','park')]))
#print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
#a = pyhop.pyhop(state1,[('travel','me','home','park')],verbose=1)

# print('- If verbose=2, Pyhop also prints a note at each recursive call:')
# pyhop.pyhop(state1,[('travel','me','home','park')],verbose=2)

# print('- If verbose=3, Pyhop also prints the intermediate states:')
#pyhop.pyhop(state1,[('travel','me','home','park')],verbose=3)