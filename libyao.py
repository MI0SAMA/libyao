#!/usr/bin/env python
import sys
import numpy
import numpy as np
import ase.io.vasp

#For POSCAR
def read_poscar(file_inp):
    f = open(file_inp, 'r')
    lines = f.readlines()
    f.close()
    ele_name  = lines[5].strip().split() #use strip just in case
    ele_num = [int(i) for i in lines[6].strip().split()] #chang str to int (how does the loop work here)
    dic_ele = {ele_name[i]:ele_num[i] for i in range(len(ele_name))}    
    dic_ele2 = {}
    for ele in ele_name:
        dic_ele2[ele] = []
        indice  = ele_name.index(ele) #the ordinal number of element
        n_start = sum(ele_num[i] for i in range(0, indice+1)) - dic_ele.get(ele) + 1
        n_end = sum(ele_num[i] for i in range(0, indice+1)) + 1
        dic_ele2[ele].append(range(n_start, n_end))
    return lines, ele_name, ele_num, dic_ele, dic_ele2 #dic_ele: kinds and number of ele, dic_ele2: kinds and lines

def sort_poscar(axis,file_inp):
    lines, ele_name, ele_num, dic_ele, dic_ele2 = read_poscar(file_inp)
    def sort_poscar_pre(ele,axis):
        axis_dic = {'x':0, 'y':1, 'z':2}
        #lines, ele_name, ele_num, dic_ele, dic_ele2 = read_poscar(file_inp)
        coord_list = []
        pos_list = []
        fix_dic = {}
        #judge if atoms are fixed
        if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
            start_line = 8
        else:
            start_line= 7
        for j in dic_ele2.get(ele)[0]: #get lines one type of atom belongs to
            coord_list = lines[j+start_line].strip().split()[0:3]
            fix_list = lines[j+start_line].strip().split()[3:]
            pos_list.append(coord_list) #the position agained 
            dic_key = '-'.join(coord_list) 
            fix_dic[dic_key] = fix_list
        array_2d = numpy.array(pos_list) #get a two dimensional array
        array_sorted = array_2d[numpy.argsort(array_2d[:,axis_dic[axis]])] #get the second row and sort the array by that
        coord_sorted = []
        for k in array_sorted:
            coord = '  '.join(k) #turn a two dimensional array into a list 
            fix_inf = '  '.join(fix_dic.get('-'.join(k))) #find the fixed information from fix_dic
            coord_sorted.append(coord + '  ' + fix_inf )
        return coord_sorted
    file_out = file_inp + '_sorted'
    f = open(file_inp)
    #head of new poscar
    lines =  f.readlines()
    f.close()
    if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
        end_line = 9
    else:
        end_line = 8
    f_out = open(file_out, 'w')
    f_out.truncate()
    for i in range(0,end_line):
        f_out.write(lines[i].rstrip()+'\n') #rstrip will keep the space of every line
    #coordinate of new poscar
    f_out.write('    ') #make it tidy
    for i in ele_name:
        f_out.write('\n    '.join(sort_poscar_pre(i, axis)))
        f_out.write('\n    ')
    f_out.close()    

def fix_poscar(fix_inp,atom_inp,file_inp):
    lines, ele_name, ele_num, dic_ele, dic_ele2 = read_poscar(file_inp)
    atom_list = []
    atom_list_new = []
    atom_lines = atom_inp.split(',')
    for i in range(len(atom_lines)):
        atom_list.append(atom_lines[i].split('-')) # gain a list like [['1', '12'], ['36']]
    for i in range(len(atom_list)):
        if len(atom_list[i]) == 1:
            atom_list_new.append(int(atom_list[i][0]))
        elif len(atom_list[i]) == 2:
            for i in range(int(atom_list[i][0]),int(atom_list[i][1])+1):# turn the 1-12 input to a range
                atom_list_new.append(i)
    if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
        start_line = 8
    else:
        start_line= 7
    coord_list = []
    pos_list = []
    for i in ele_name:
        for j in dic_ele2.get(i)[0]:
            if j in atom_list_new:
                coord_list = lines[j+start_line].strip().split()[0:3]
                coord_list = coord_list + (fix_inp.strip().split(','))
            else:
                coord_list = lines[j+start_line].strip().split()[0:3]
                coord_list = coord_list + lines[j+start_line].strip().split()[3:]
            pos_list.append(coord_list)
    coord_fixed = []
    for i in range(len(pos_list)):
       coord_fixed.append('  '.join(str(j) for j in pos_list[i])) # an empty list can't be called, use append instead
    file_out = file_inp + '_fixed'
    f_out = open(file_out, 'w')
    f_out.truncate()
    for i in range(0,7):
        f_out.write(lines[i].rstrip()+'\n')
    f_out.write("Selective Dynamics"+'\n')
    f_out.write("Direct"+'\n')
    f_out.write('    ')
    f_out.write('\n    '.join(coord_fixed))
    f_out.write('\n    ')
    f_out.close()

def move_poscar(file_inp, atom_inp, dis_inp):
    dis_list = [float(i) for i in dis_inp.split(',')]
    atom_lines = atom_inp.split(',')
    lines, ele_name, ele_num, dic_ele, dic_ele2 = read_poscar(file_inp)
    atom_list = []
    for i in range(len(atom_lines)):
        atom_list.append(atom_lines[i].split('-')) # gain a list like [['1', '12'], ['24', '36']]     
    if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
        start_line = 8
    else:
        start_line= 7
    for j in range(len(atom_list)):
        if len(atom_list[j]) == 1:
            line_num = int(atom_list[j][0]) + start_line #change list to int
            old_line = [float(i) for i in lines[line_num].strip().split()[0:3]]
            new_line = [0,0,0]
            for i in range(0,3):
                new_line[i] = old_line[i] + dis_list[i] #another way to realize the following command
            new_line = new_line + lines[line_num].strip().split()[3:]
            new_line = " ".join(str(i) for i in new_line) + '\n'#change the list containing float to a str
            lines[line_num] = new_line
        else:
            for k in range(int(atom_list[j][0])+start_line, int(atom_list[j][1])+start_line+1):#get the line number of the fixed atoms
                old_line = [float(i) for i in lines[k].strip().split()[0:3]]
                new_line = numpy.sum([old_line,dis_list],axis=0).tolist() #this list only have one element
                new_line = new_line + lines[k].strip().split()[3:]
                new_line = " ".join(str(i) for i in new_line) + '\n'#change the list containing float to a str
                lines[k] = new_line
    file_out = file_inp + '_moved'
    f_out = open(file_out, 'w')
    f_out.truncate()
    for i in range(0,start_line+1):
        f_out.write(lines[i].rstrip()+'\n')
    for i in range(start_line+1,len(lines)):
        f_out.write("    " + lines[i].strip()+'\n')
    f_out.close()

#For xyz file of water layer sturcture   
def read_water_angle(file_inp):
    f = open(file_inp, 'r')
    line = f.readlines()
    f.close()
    atom_num = int(line[0])
    step_num = int(len(line)/(atom_num+2))
    h_pos = []
    o_pos = []
    h_num, o_num = 0, 0
    for i in range(len(line)):
        if line[i].strip().split()[0] == 'H':
            h_pos.append(line[i].strip().split()) #a list caontain all position began by mark H
            h_num += 1
        elif line[i].strip().split()[0] == 'O':
            o_pos.append(line[i].strip().split()) #a list caontain all position of O began by mark O
            o_num += 1
    h_num, o_num = int(h_num/step_num), int(o_num/step_num)
    ang_list1, ang_list2, ang_list3, ang_list4 = [], [], [], [] #1 is H1 and O, 2 is H2 and O, 3 is mid
    for j in range(step_num):
        for i in range(j*o_num,(j+1)*o_num):
            #water_dic[i] = o_pos[i] + h_pos[2*i] + h_pos[2*i+1] # num: [O,x,y,z,H,x,y,z,H,x,y,z]
            #O-H1 bongding
            vec_oh1 = [float(h_pos[2*i][k+1]) - float(o_pos[i][k+1]) for k in range(3)]
            angle1 = vec_oh1[2]/numpy.sqrt(numpy.square(vec_oh1[0])+numpy.square(vec_oh1[1])+numpy.square(vec_oh1[2]))
            ang_list1.append(numpy.degrees(numpy.arcsin(angle1)))
            #O-H2 bongding
            vec_oh2 = [float(h_pos[2*i+1][k+1]) - float(o_pos[i][k+1]) for k in range(3)]
            angle2 = vec_oh2[2]/numpy.sqrt(numpy.square(vec_oh2[0])+numpy.square(vec_oh2[1])+numpy.square(vec_oh2[2]))
            ang_list2.append(numpy.degrees(numpy.arcsin(angle2)))
            #middle basis
            vec_mid = [(float(h_pos[2*i][k+1]) + float(h_pos[2*i+1][k+1]))/2 for k in range(3)]
            for x in range(3):
                vec_mid[x] = vec_mid[x] - float(o_pos[i][x+1])
            angle3 = vec_mid[2]/numpy.sqrt(numpy.square(vec_mid[0])+numpy.square(vec_mid[1])+numpy.square(vec_mid[2]))
            ang_list3.append(numpy.degrees(numpy.arcsin(angle3)))
            #O-H1 and O-H2 angle
            a=np.inner(np.array(vec_oh1),np.array(vec_oh2))
            b=np.linalg.norm(np.array(vec_oh1))*np.linalg.norm(np.array(vec_oh2))
            ang_list4.append(np.degrees(np.arccos(a/b)))
    return ang_list1, ang_list2, ang_list3, ang_list4

def cal_poss(ang_list):
    pos_list = []
    for i in range(-85,91,2):
        num = 0
        for j in range(len(ang_list)):
            if float(ang_list[j]) > (i-5) and float(ang_list[j]) < i:
                num += 1
        num = float(num)/len(ang_list)
        pos_list.append(num)
    return pos_list

def save_angle(ang_list1, ang_list2, ang_list3):
    def ang_poss(ang_list):
        pos_list = []
        for i in range(-89,91,1):
            num = 0
            for j in range(len(ang_list)):
                if float(ang_list[j]) > (i-1) and float(ang_list[j]) < i:
                    num += 1
            num = float(num)/len(ang_list)
            pos_list.append(num)
        return pos_list
    #Write the angle file
    file_out = file_inp + '_angle'
    f_out = open(file_out, 'w')
    f_out.truncate()
    f_out.write('No.     O-H1_ang       O-H2_ang       Central_ang\n')
    for j in range(len(ang_list1)):
        f_out.write("{:0>2d}".format(j+1))
        for k in range(1,4):
            list = 'ang_list'+str(k)
            f_out.write('     '+str(format(eval(list)[j], '4f')))
        f_out.write('\n')
    f_out.close()
    #Write the possibility file
    file_out = file_inp + '_ang_poss'
    f_out = open(file_out, 'w')
    f_out.truncate()
    f_out.write('Range     O-H1_poss       O-H2_poss       Central_poss\n')
    poss_dic={}
    for i in range (1,4):
        list='ang_list'+str(i)
        poss_dic[list]=ang_poss(eval(list))
    #angle range (-89,91,1)
    for j in range(-89,91,1):
        f_out.write(str("{:0>2d}".format(j-1))+'~'+str("{:0>2d}".format(j)))
        for k in range(1,4):
            list_name = 'ang_list'+str(k)
            f_out.write('     '+str(format(poss_dic[list_name][j+89], '4f')))
        f_out.write('\n')
    f_out.close()

#Convert one xyz file to poscar and creat supercell    
def convert_xyz(file_inp, file_out):
    xyz_file, out_file = file_inp, file_out
    def get_box(xyz_file):
        with open(xyz_file) as in_xyz:
            line1 = in_xyz.readlines()[1] 
            if 'Lattice="' in line1:  # Lattice="40.0 0.0 0.0 0.0 40.0 0.0 0.0 0.0 40.0"
                box =  line1.rstrip().split('"')[1].split()
                a = box[0:3]
                b = box[3:6]
                c = box[6:]
            else:
                print ("Are your system is a cubic lattice?")
                check = input('Please type y to input lattice length or other keys to input lattice constant: ')
                if  check == 'y' or check == 'Y':
                    a = [input('please enter a direction: '), '0.0', '0.0']
                    b = ['0.0', input('please enter b direction: '), '0.0']
                    c = ['0.0', '0.0',input('please enter c direction: ') ]
                else:
                    a = input('Lattice constant a, like:1 2 3: ').rstrip().split( )
                    b = input('Lattice constant b: ' ).rstrip().split( ) 
                    c = input('Lattice constant c: ').rstrip().split( ) 
                    for i in (a,b,c):
                        i=list(map(float, i))
        return a, b, c
    #Cell size
    #a = ['13.00000000', '0.0', '0.0'] 
    #b = ['-6.50000000', '11.25833025', '0.0'] 
    #c = ['0.0', '0.0', '26.138826']  
    def get_total_ele(xyz_file):
        ele_list = []
        with open(xyz_file) as in_xyz:
            in_file = in_xyz.readlines()[2:]
            for line in in_file:
                ele_list.append(line.rstrip().split()[0])
        return list(set(ele_list))
    def get_coordinations(ele):# get the coordination for one specifix element 
        line_list = []
        with open(xyz_file) as in_xyz:
            in_file = in_xyz.readlines()[2:]
            for line in in_file:
                line_s = line.rstrip().split()[0:4]
                if ele in line_s:
                    line_list.append(line_s)
        return line_list
    def get_num_ele(ele):#Get the number of each element 
        return len(get_coordinations(ele))
    poscar = open(out_file, 'w')
    poscar.write('Converted_POSCAR\n1.0\n')
    #--a,b,c input by hand or set in script--#
    for i in get_box(xyz_file):
    #for i in a,b,c:
        poscar.write('%s %s %s\n' %(i[0], i[1], i[2]))
    for i in get_total_ele(xyz_file):
        poscar.write(i+' ')
    poscar.write('\n')
    for i in get_total_ele(xyz_file):
        poscar.write(str(get_num_ele(i))+' ') 
    poscar.write('\nCartesian\n')
    for i in get_total_ele(xyz_file):
        for j in get_coordinations(i): 
            poscar.write('%s %s %s\n' %(j[1], j[2], j[3]))
    poscar.close() #!!!
    #--crystal size input by hand or set in script--#
    a=input('Supercell size like "3 3 3" >>').rstrip().split()
    #a=[1,1,1]
    x,y,z = [int(i) for i in a]
    try:
        cell = ase.io.vasp.read_vasp(out_file)
        ase.io.vasp.write_vasp(out_file+'_ex',cell*(x, y, z), direct=True,sort=True)
    except:
        print('Something maybe wrong when using ase')

#For 3*3*3 poscar of water layer sturcture
def read_water_angle_poscar(file_inp):
    lines, ele_name, ele_num, dic_ele, dic_ele2 = read_poscar(file_inp)
    pos_dic={}
    if lines[7].strip() == "Selective Dynamics" or lines[7].strip() == "S":
        start_line = 8
    else:
        start_line= 7
    for i in ele_name:
        pos_list=[]
        for j in dic_ele2.get(i)[0]: #get lines one type of atom belongs to
            coord_list = lines[j+start_line].strip().split()[0:3]
            pos_list.append(coord_list) #the position agained
            pos_dic[i]= pos_list
    #Calculate the distance between O and H
    a = lines[2].strip().split()
    b = lines[3].strip().split()
    c = lines[4].strip().split()
    axis = np.matrix((a,b,c),dtype=float).T #3*3array
    O_dic,H_dic={},{}
    H_list=[]
    num=0
    for i in pos_dic['H']:
        if 0.3<float(i[0])<0.7 and 0.3<float(i[1])<0.7:
            i = [float(k) for k in i]
            H_list.append(i)
    for i in pos_dic['O']:
        i = [float(k) for k in i]
        if 0.3333<i[0]<0.6666 and 0.3333<i[1]<0.6666:
            num +=1
            O_dic[num]=i
            H_dic[num]=[]
            """
            for j in H_list:
                dis=np.subtract(i,j,dtype=float)
                dis1=np.inner(dis,axis) #Attention!!!
                #dis1=[np.inner(dis,axis[0]),np.inner(dis,axis[1]),np.inner(dis,axis[2])]
                if np.linalg.norm(dis1) < 1.1:
                    H_dic[num].append(j)
                    #H_list.remove(j) 
                    #Attention to remove when loop in list, you should do as below
            """
            for j in range(len(H_list)-1,-1,-1):#Use reverse order
                dis=np.subtract(i,H_list[j],dtype=float)
                dis1=np.inner(dis,axis) #Attention to the inner function
                #dis1=[np.inner(dis,axis[0]),np.inner(dis,axis[1]),np.inner(dis,axis[2])]
                if np.linalg.norm(dis1) < 1.1:
                    H_dic[num].append(H_list[j])
                    del H_list[j]    
    #if len(O_dic) !=56:
        #print ('The number of O atoms is not 56')
    return O_dic,H_dic