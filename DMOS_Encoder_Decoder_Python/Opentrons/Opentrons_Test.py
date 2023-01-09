# -*- coding: utf-8 -*-

import math

def get2DLocation(number, columns, initCol=1):
    ### Generates a list of indices using the row-wise scheme
    coldef = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    locations = []
    row = 1
    col = 1
    
    nl = 0
    
    maxr = math.ceil(number/columns)+1
    
    for n in range(1,maxr):
        for k in range(columns):
            if nl < number:
                loc = coldef[n-1] + str(k+initCol)
                locations.append(loc)
                nl += 1
            else:
                break
    
    return locations


def readDMOSfile(filename):
    
    f = open(filename, 'r')
    content = f.readlines()
    f.close()
    
    address = 0
    ListMutations = []
    for line in content:
        
        if 'word' in line:
            address = int( line[10:] )-1
        if 'HEX' in line:
            m1 =  int(line[4],16)
            m2 =  int(line[5],16)
            m3 =  int(line[6],16)
            m4 =  int(line[7],16)
            symbols=[m1,m2,m3,m4]
            ListMutations.append(symbols)
         
    return ListMutations
            
        
    
        
           
        



#ListMutations=readDMOSfile('../DMOS_Hex.txt')

# set1= [ [], [4], [3], [3,4], [2], [2,4], [2,3], [2,3,4], [1], [1,4], [1,3], [1,3,4], [1,2], [1,2,4], [1,2,3], [1,2,3,4]]
# set2= [ [], [8], [7], [7,8], [6], [6,8], [6,7], [6,7,8], [5], [5,8], [5,7], [5,7,8], [5,6], [5,6,8], [5,6,7], [5,6,7,8]]
# set3= [ [], [12], [11], [11,12], [10], [10,12], [10,11], [10,11,12], [9], [9,12], [9,11], [9,11,12], [9,10], [9,10,12], [9,10,11], [9,10,11,12]]
# set4= [ [], [16], [15], [15,16], [14], [14,16], [14,15], [14,15,16], [13], [13,16], [13,15], [13,15,16], [13,14], [13,14,16], [13,14,15], [13,14,15,16]]



number=16
columns=12

locations = get2DLocation(number, columns,1)
print(locations)


# symbLocation = 0 

# tips = 0

# for k in range(16):
#     print("Moving to Set 1, symbol ", k, "Location", symbLocation)
#     for loc in set1[k]:
#         lib = locations[loc-1]
#         tips += 1
#         print (lib)
#     symbLocation += 1

# for k in range(16):
#     print("Moving to Set 2, symbol ", k, "Location", symbLocation)
#     for loc in set2[k]:
#         lib = locations[loc-1]
#         tips += 1
#         print (lib)
#     symbLocation += 1

# for k in range(16):
#     print("Moving to Set 3, symbol ", k, "Location", symbLocation)
#     for loc in set3[k]:
#         lib = locations[loc-1]
#         tips += 1
#         print (lib)
#     symbLocation += 1

# for k in range(16):
#     print("Moving to Set 4, symbol ", k, "Location", symbLocation)
#     for loc in set4[k]:
#         lib = locations[loc-1]
#         tips += 1
#         print (lib)
#     symbLocation += 1

# print ("Total tips:", tips)



# print(locations)