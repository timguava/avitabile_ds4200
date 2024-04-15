import pandas as pd
import math

senate_per_row = [8,14,20,26,32]
senate_template = pd.DataFrame(columns=['r','theta','x','y'])
for i in range(len(senate_per_row)):
    for j in range(senate_per_row[i]):
        theta = math.pi * (j / (senate_per_row[i] - 1))
        x = (i+1) * math.cos(theta)
        y = (i+1) * math.sin(theta)
        senate_template.loc[len(senate_template.index)] = [i+1,theta,x,y]

senate_template = senate_template.sort_values(by=['theta','r'],ascending=False).reset_index(drop=True)


house_per_row = [0,0,0,15,20,25,30,35,40,45,50,55,60,65]
house_template = pd.DataFrame(columns=['r','theta','x','y'])
for i in range(len(house_per_row)):
    for j in range(house_per_row[i]):
        theta = math.pi * (j / (house_per_row[i] - 1))
        x = (i+1) * math.cos(theta)
        y = (i+1) * math.sin(theta)
        house_template.loc[len(house_template.index)] = [i+1,theta,x,y]

house_template = house_template.sort_values(by=['theta','r'],ascending=False).reset_index(drop=True)


senate_template.to_csv('senate_template.csv')
house_template.to_csv('house_template.csv')