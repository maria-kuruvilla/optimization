"""
import text files about parcels and adjacencies and the output a cplex LP formulation
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

objective = '' #empty string
objective2 = '' #empty string
budget = 'budget:'
core = 'core: x_23 = 1' 
parcel_list2 = 'arcs: '
cycles = []
zwconstraint= []
zyconstraint= []

for i in range(parcel_length):
    if i==parcel_length-1:
        objective += parcels_data[i,1]+' x_'+parcels_data[i,0]
        objective2 += parcels_data[i,3]+' x_'+parcels_data[i,0]
        budget += parcels_data[i,2]+' x_'+parcels_data[i,0] + '<= 1000000'
        parcel_list2 += '-' + ' x'+parcels_data[i,0] + '+'
    elif (i%5 == 0) and (i !=0) :
        objective += parcels_data[i,1]+' x_'+parcels_data[i,0]+ '+' +'\r\n'
        objective2 += parcels_data[i,3]+' x_'+parcels_data[i,0]+ '+' +'\r\n'
        budget += parcels_data[i,2]+' x_'+parcels_data[i,0]+ '+' + '\r\n'
        parcel_list2 += '-' + ' x_'+parcels_data[i,0] + '\r\n'
    else:
        objective += parcels_data[i,1]+' x_'+parcels_data[i,0]+ '+'
        objective2 += parcels_data[i,3]+' x_'+parcels_data[i,0]+ '+'
        budget += parcels_data[i,2]+' x_'+parcels_data[i,0]+ '+'
        parcel_list2 += '-' + ' x_'+parcels_data[i,0]

for i in range(len(adjacency_data)):
    zyconstraint.append('zyconstraint' + str(i)+ ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '-' + str(m) +' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] +   '<= 0' )
    zwconstraint.append('zwconstraint' + str(i)+ ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '- w_' +  adjacency_data[i,0]+ '<= 1' )
    if i == len(adjacency_data)-1:
        parcel_list2 += 'y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '= -1 '
        cycles.append('cycles' + str(i) + ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + ' -w_' +  adjacency_data[i,0]  + '-' + str(m) + ' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '>= ' + str(-m+1) )
    elif (i%5 == 0) and (i !=0) :
        parcel_list2 += 'y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '+' + '\r\n'
        cycles.append('cycles' + str(i) + ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + ' -w_' +  adjacency_data[i,0]  + '-' + str(m) + ' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '>= ' + str(-m+1) )
    else:
        parcel_list2 += 'y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '+'
        cycles.append('cycles' + str(i) + ': ' + ' z_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + ' -w_' +  adjacency_data[i,0]  + '-' + str(m) + ' y_' + adjacency_data[i,0] + '_' + adjacency_data[i,1] + '>= ' + str(-m+1) )
    
adj_list=[]
adj_list2=[]
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

    lengthb = len(b)
    #print(lengthb)
    if lengthb==1:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' -x_'+parcels_data[i,0] + '<= 0')
    if lengthb==2:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+ '-x_'+parcels_data[i,0] + '<= 0')
    if lengthb==3:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+ '-x_'+parcels_data[i,0] + '<= 0')
    if lengthb==4:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+'+'+'y'+parcels_data[i,0]+'_'+b[3]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+'+'+' y_'+parcels_data[i,0]+'_'+b[3]+ '-x_'+parcels_data[i,0] + '<= 0')
    if lengthb==5:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+'+'+'y'+parcels_data[i,0]+'_'+b[3]+'+'+'y'+parcels_data[i,0]+'_'+b[4]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+'+'+' y_'+parcels_data[i,0]+'_'+b[3]+'+'+' y_'+parcels_data[i,0]+'_'+b[4]+ '-x_'+parcels_data[i,0] + '<= 0')
    if lengthb==6:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+'+'+'y'+parcels_data[i,0]+'_'+b[3]+'+'+'y'+parcels_data[i,0]+'_'+b[4]+'+'+'y'+parcels_data[i,0]+'_'+b[5]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+'+'+' y_'+parcels_data[i,0]+'_'+b[3]+'+'+' y_'+parcels_data[i,0]+'_'+b[4]+'+'+' y_'+parcels_data[i,0]+'_'+b[5]+ '-x_'+parcels_data[i,0] + '<= 0')

    if lengthb==7:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+'+'+'y'+parcels_data[i,0]+'_'+b[3]+'+'+'y'+parcels_data[i,0]+'_'+b[4]+'+'+'y'+parcels_data[i,0]+'_'+b[5]+'+'+'y'+parcels_data[i,0]+'_'+b[6]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+'+'+' y_'+parcels_data[i,0]+'_'+b[3]+'+'+' y_'+parcels_data[i,0]+'_'+b[4]+'+'+' y_'+parcels_data[i,0]+'_'+b[5]+'+'+' y_'+parcels_data[i,0]+'_'+b[6]+ '-x_'+parcels_data[i,0] + '<= 0')
    if lengthb==8:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+'+'+'y'+parcels_data[i,0]+'_'+b[3]+'+'+'y'+parcels_data[i,0]+'_'+b[4]+'+'+'y'+parcels_data[i,0]+'_'+b[5]+'+'+'y'+parcels_data[i,0]+'_'+b[6]+'+'+'y'+parcels_data[i,0]+'_'+b[7]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+'+'+' y_'+parcels_data[i,0]+'_'+b[3]+'+'+' y_'+parcels_data[i,0]+'_'+b[4]+'+'+' y_'+parcels_data[i,0]+'_'+b[5]+'+'+' y_'+parcels_data[i,0]+'_'+b[6]+'+'+' y_'+parcels_data[i,0]+'_'+b[7]+ '-x_'+parcels_data[i,0] + '<= 0')
    if lengthb==9:
        #adj_list.append(b[0]+': '+ 'y'+parcels_data[i,0]+'_'+b[1]+'+'+'y'+parcels_data[i,0]+'_'+b[2]+'+'+'y'+parcels_data[i,0]+'_'+b[3]+'+'+'y'+parcels_data[i,0]+'_'+b[4]+'+'+'y'+parcels_data[i,0]+'_'+b[5]+'+'+'y'+parcels_data[i,0]+'_'+b[6]+'+'+'y'+parcels_data[i,0]+'_'+b[7]+' <= ' +str(lengthb-1)+'x'+parcels_data[i,0])
        adj_list2.append(b[0]+': '+ ' y_'+parcels_data[i,0]+'_'+b[1]+'+'+' y_'+parcels_data[i,0]+'_'+b[2]+'+'+' y_'+parcels_data[i,0]+'_'+b[3]+'+'+' y_'+parcels_data[i,0]+'_'+b[4]+'+'+' y_'+parcels_data[i,0]+'_'+b[5]+'+'+' y_'+parcels_data[i,0]+'_'+b[6]+'+'+' y_'+parcels_data[i,0]+'_'+b[7]+' y_'+parcels_data[i,0]+'_'+b[8]+ '-x_'+parcels_data[i,0] + '<= 0')

    
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




text_file = open("../../output/optimization/Output_HW4.cpx", "w")
text_file.writelines(['MIN','\r\n','OBJECTIVE:','\r\n',objective2,'\r\n','\r\n','Subject To:','\r\n',budget,'\r\n'])
for i in range(len(adj_list)):
    text_file.writelines([adj_list[i],'\r\n'])
for i in range(len(adj_list3)):
    text_file.writelines([adj_list3[i],'\r\n'])
text_file.writelines([parcel_list2,'\r\n'])
for i in range(len(cycles)):
    text_file.writelines([cycles[i],'\r\n'])
for i in range(len(cycle_constraint)):
    text_file.writelines([cycle_constraint[i],'\r\n'])
"""
for i in range(len(zwconstraint)):
    text_file.writelines([zwconstraint[i],'\n'])
for i in range(len(zyconstraint)):
    text_file.writelines([zyconstraint[i],'\n'])
"""
text_file.writelines([core,'\r\n'])
text_file.writelines(['Binary','\r\n'])
for i in range(parcel_length):
    text_file.writelines(['x_',parcels_data[i,0],'\r\n'])
for i in range(len(adjacency_data)):
    text_file.writelines(['y_',adjacency_data[i,0],'_',adjacency_data[i,1],'\r\n'])


text_file.writelines(['\r\n','End'])
text_file.close()
