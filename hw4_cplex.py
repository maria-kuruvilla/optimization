"""
import text files about parcels,perimeters and adjacencies and output a modified cplex LP formulation for max compactness/
min perimeter
"""
#imports 

import csv
import numpy as np
import pdb

#create empty lists
parcels_list=[]
parcels_price=[]
parcels_area=[]
parcels_perimeter=[]
parcel_length = 100
m = 100
in_dir = '../../data/optimization/'
in_fn = in_dir + 'Parcels_HW4.txt'
with open(in_fn,'r') as parcels:
    for line in parcels:
        parcels_list.append(line.rstrip('\n').split(',')[0])
        parcels_area.append(line.rstrip('\n').split(',')[1])
        parcels_price.append(line.rstrip('\n').split(',')[2])
        parcels_perimeter.append(line.rstrip('\n').split(',')[3])


parcels_data = np.column_stack((parcels_list,parcels_area,parcels_price, parcels_perimeter)) 

#create empty lists
adjacency_list1=[]
adjacency_list2=[]
adjacency_list3=[]

in_fn2 = in_dir + 'Adjacency_HW4.txt'
with open(in_fn2,'r') as adjacency:
    for line in adjacency:
        adjacency_list1.append(line.rstrip('\n').split(',')[0])
        adjacency_list2.append(line.rstrip('\n').split(',')[1])
        adjacency_list3.append(line.rstrip('\n').split(',')[2])
        
adjacency_data = np.column_stack((adjacency_list1,adjacency_list2,adjacency_list3)) 

objective = 'area: '
objective2 = '' #empty string
budget = 'budget:'
core = 'core: x_23 = 1' 
parcel_list2 = 'arcs: '
cycles = []
const1 =[] 
const2 = []

for i in range(parcel_length):
    if i==parcel_length-1:
        objective += parcels_data[i,1]+' x_'+parcels_data[i,0] + '>= 290.62'
        objective2 += parcels_data[i,3]+' x_'+parcels_data[i,0]
        
        parcel_list2 += '-' + ' x'+parcels_data[i,0] + '+'
    elif (i%5 == 0) and (i !=0) :
        objective += parcels_data[i,1]+' x_'+parcels_data[i,0]+ '+' +'\r\n'
        objective2 += parcels_data[i,3]+' x_'+parcels_data[i,0]+ '+' +'\r\n'
        
        parcel_list2 += '-' + ' x_'+parcels_data[i,0] + '\r\n'
    else:
        objective += parcels_data[i,1]+' x_'+parcels_data[i,0]+ '+'
        objective2 += parcels_data[i,3]+' x_'+parcels_data[i,0]+ '+'
        
        parcel_list2 += '-' + ' x_'+parcels_data[i,0]

for i in range(len(adjacency_data)):
    if i == len(adjacency_data)-1:
        parcel_list2 += 'y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '= -1 '
        cycles.append('cycles' + str(i) + ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + ' -w_' +  adjacency_data[i,0]  + '-' + str(m) + ' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '>= ' + str(-m+1) )
        objective2 += '-' +  str(2*float(adjacency_data[i,2])) + 'm_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1]
        const1.append('new_constraint1_' + str(i) + ': ' + 'x_' + adjacency_data[i,0] + ' + x_' + adjacency_data[i,1] + ' - m_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] + ' <= 1' )
        const2.append('new_constraint2_' + str(i) + ': ' + 'x_' + adjacency_data[i,0] + ' + x_' + adjacency_data[i,1] + ' -2 m_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] + ' >= 0' )
    elif (i%5 == 0) and (i !=0) :
        parcel_list2 += 'y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '+' + '\r\n'
        cycles.append('cycles' + str(i) + ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + ' -w_' +  adjacency_data[i,0]  + '-' + str(m) + ' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '>= ' + str(-m+1) )
        objective2 += '-' + str(2*float(adjacency_data[i,2])) + 'm_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] +'\r\n'
        const1.append('new_constraint1_' + str(i) + ': ' + 'x_' + adjacency_data[i,0] + ' + x_' + adjacency_data[i,1] + ' - m_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] + ' <= 1' )
        const2.append('new_constraint2_' + str(i) + ': ' + 'x_' + adjacency_data[i,0] + ' + x_' + adjacency_data[i,1] + ' -2 m_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] + ' >= 0' )
    else:
        parcel_list2 += 'y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '+'
        cycles.append('cycles' + str(i) + ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + ' -w_' +  adjacency_data[i,0]  + '-' + str(m) + ' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '>= ' + str(-m+1) )
        objective2 += '-' + str(2*float(adjacency_data[i,2])) + 'm_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1]
        const1.append('new_constraint1_' + str(i) + ': ' + 'x_' + adjacency_data[i,0] + ' + x_' + adjacency_data[i,1] + ' - m_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] + ' <= 1' )
        const2.append('new_constraint2_' + str(i) + ': ' + 'x_' + adjacency_data[i,0] + ' + x_' + adjacency_data[i,1] + ' -2 m_' + adjacency_data[i,0] +  '_' + adjacency_data[i,1] + ' >= 0' )



cycle_constraint = []
for i in range(parcel_length):
    incoming = []
    
    for j in range(len(adjacency_data)):
        if adjacency_data[j,1] == parcels_data[i,0]:
            incoming.append(adjacency_data[j,0])
    
    a = ''
    if len(incoming) == 0:
        cycle_constraint.append('cycle_constraint' + str(i) + ': ' + ' w_' + parcels_data[i,0]  + '= 0')
        
    for k in range(len(incoming)):
        
        if k == (len(incoming) - 1):
            cycle_constraint.append('cycle_constraint' + str(i) + ': ' + ' w_' + parcels_data[i,0] + a + '-' + ' z_' + incoming[k]  + '_' + parcels_data[i,0] + '= 0')
        else:
            a += '-' + ' z_' + incoming[k] + '_' + parcels_data[i,0]


adj_list=[]
adj_list3=[]
for i in range(parcel_length):
    b = []
    c = []
    
    for j in range(len(adjacency_data)):
        

        if adjacency_data[j,0]==parcels_data[i,0]:
            b.append(adjacency_data[j,1])
        if adjacency_data[j,1]==parcels_data[i,0]:
            c.append(adjacency_data[j,0])
    a = ''
    #if len(c) == 0:
     #   adj_list.append('parcel'+ parcels_data[i,0] + ': ' + '-x' + parcels_data[i,0] + ' <= 0')
    for k in range(len(c)):

        if k == (len(c) -1) :
            
            adj_list.append('neighboring_parcel'+ parcels_data[i,0] + ': ' + a  + '+' + ' y_' + c[k] + '_' + parcels_data[i,0] + '-' + str(k+1) + ' x_' + parcels_data[i,0] + ' <= 0')
        else:
            
            a +=  '+' + ' y_' + c[k] + '_' + parcels_data[i,0]
    
    aa = ''
    if (len(b) == 0) :
        #print('No adjacent parcels')
        adj_list3.append('parcel'+ parcels_data[i,0] + ':  -x_'+parcels_data[i,0] + '<= 0')
    for kk in range(len(b)):


        if kk == (len(b) - 1) :
            adj_list3.append('parcel'+ parcels_data[i,0] + ': ' + aa + '+ y_' + parcels_data[i,0] + '_' + b[kk]  + ' -x_'+parcels_data[i,0] + '<= 0')
        else :
            aa += '+' + ' y_'  + parcels_data[i,0] + '_'+ b[kk]

text_file = open("../../output/optimization/Output_HW4.cpx", "w")
text_file.writelines(['MIN','\r\n','OBJECTIVE:','\r\n',objective2,'\r\n','\r\n','Subject To:','\r\n',objective, '\r\n'])
for i in range(len(const1)):
    text_file.writelines([const1[i],'\r\n'])
for i in range(len(const2)):
    text_file.writelines([const2[i],'\r\n'])
text_file.writelines([parcel_list2,'\r\n'])
for i in range(len(cycles)):
    text_file.writelines([cycles[i],'\r\n'])
for i in range(len(cycle_constraint)):
    text_file.writelines([cycle_constraint[i],'\r\n'])
for i in range(len(adj_list)):
    text_file.writelines([adj_list[i],'\r\n'])
for i in range(len(adj_list3)):
    text_file.writelines([adj_list3[i],'\r\n'])
text_file.writelines([core,'\r\n'])
text_file.writelines(['Binary','\r\n'])
for i in range(parcel_length):
    text_file.writelines(['x_',parcels_data[i,0],'\r\n'])
for i in range(len(adjacency_data)):
    text_file.writelines(['y_',adjacency_data[i,0],'_',adjacency_data[i,1],'\r\n'])


text_file.writelines(['\r\n','End'])

text_file.close()
