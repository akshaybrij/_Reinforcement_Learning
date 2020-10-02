import os
import numpy as np
from PIL import Image
import pickle 
import cv2
import time

size = 10

class Grid:
    def __init__(self,size=10):
        self.x = np.random.randint(0,size)
        self.y = np.random.randint(0,size)
    
    def subtract(self,other):
        return (self.x - self.other.x,self.y-self.other.y)

    def isequal(self,other):
        if(self.x-self.other==0 and self.y-self.other.y ==0):
            return True
        else:
            return False

    def action(self,choice):
        if choice == 0:
            self.move(x=1,y=1)
        elif choice == 1:
            self.move(x=-1,y=-1)
        elif choice == 2:
            self.move(-1,1)
        elif choice == 3:
            self.move(1,-1)
        elif choice == 4:
            self.move(1,0)
        elif choice == 5:
            self.move(0,1)
        elif choice == 6:
            self.move(-1,0)
        elif choice == 7:
            self.move(0,-1)

    def move(self,x,y):
        if not x:
            self.x += np.random.randint(-1,1)
        else:
            self.x += x

        if not y:
            self.y += np.random.randint(-1,1)
        else:
            self.y += y

        if self.x < 0:
            self.x = 0
        if self.x >= size:
            self.x = size - 1 
        if self.y < 0:
            self.y = 0
        if self.y >= size:
            self.y = size - 1

episodes = 1000
move_penalty = -1
police_penalty = -100
gold_penalty = 50
show_every = 1000
gamma = 0.9
lr = 0.2

thief_key = 1
police_key = 2
gold_key = 3

d={1:(255,0,0),2:(0,255,0),3:(0,0,255)}

q_t = {}
print("s")
for a in range(-size,size+1):
    for b in range(-size,size+1):
        for c in range(-size,size+1):
            for d in range(-size,size+1):
                for e in range(-size,size+1):
                    for f in range(-size,size+1):
                        q_t[((a,b),(c,d),(e,f))] = [np.random.uniform(-8,0) for i in range(8)]

for e in range(episodes):
    police1 = Grid()
    police2 = Grid()
    theif = Grid()
    gold = Grid()
    print(e)
    show = True

    for i in range(200):
        dstate = (police1.subtract(thief),police2.subtrace(theif),gold.subtrace(thief))
        action = np.random.randint(0,8)
        thief.action(action)
        if theif.x == police1.x and theif.y == thief.y:
            reward = police_penalty  
        if thief.x == police2.x and thief.y == police2.y:
            reward = police_penalty  
        if thief.x == gold.x and thief.y == gold.y:
            reward = gold_penalty
        new_dstate = (police1.subtract(thief),police2.subtrace(thief),gold.subtract(thief))
        max_future_qval = np.max(q_t[new_dstate])
        current_qval = q_t[dstate][action]
        if reward == q_t[dstate][action]:
            new_q_val = reward
        else:
            new_q_val = (1-lr) * current_qval + lr*(reward + gamma*max_future_qval)
        q_t[dstate][action] = new_q_val


    if(show):
        env = np.zeros((size,size,3),dtype=np.uint8)
        env[gold.x][gold.y] = d[gold_key]
        env[police1.x][police1.y] = d[police_key]
        env[police2.x][police2.y] = d[police_key]
        env[thief.x][thief.y] = d[thief]

        image = Image.fromarray(env,'RGB')
        image = image.resize((300,300))

        cv2.imshow("Environment",np.array(image))

        if reward == gold_penalty and reward == police_penalty:
            break 


            

