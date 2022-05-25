#!/bin/sh
#===== Advanced setting =====#
path_POTCAR=~/example/potpaw_PBE
path_INCAR=~/example/INCAR_example
export vaspcode_bremen="?home?kiyou?PROGRAM?mpich2-1.4.1p1_intel14.0?bin?mpiexec -machinefile .?machines.LINUX -launcher rsh -launcher-exec ?usr?bin?rsh -n \$N ?home?kiyou?PROGRAM?VASP.5.3.3-mpich2-1.4.1p1_intel14.0_fftw3.33?src?vasp.5.3?vasp"
export vaspcode_sapporo="?usr?local?mpich2-1.4.1p1-ifort14.0?bin?mpiexec -machinefile .?machines.LINUX -launcher rsh -launcher-exec ?usr?bin?rsh -n \$N ?home?program_packages?VASP.5.3.3-mpich2_1.41p1-ifort14.0-fftw3.33?src?vasp.5.3?vasp "
export vaspcode_dubai="?home?kiyou?PROGRAM?mpich2-1.4.1p1_intel14.0?bin?mpiexec -machinefile .?machines.LINUX -launcher rsh -launcher-exec ?usr?bin?rsh -n \$N ?home?kiyou?PROGRAM?VASP.5.3.3-mpich2-1.4.1p1_intel14.0_fftw3.33?src?vasp.5.3?vasp "
export vaspcode_osaka="?home?kiyou?PROGRAM?mpich2-1.4.1p1_intel14.0?bin?mpiexec -machinefile .?machines.LINUX -launcher rsh -launcher-exec ?usr?bin?rsh -n \$N ?home?kiyou?PROGRAM?VASP.5.3.3-mpich2-1.4.1p1_intel14.0_fftw3.33?src?vasp.5.3?vasp "
export vaspcode_macau="?home?yao?PROGRAM?mpich2-1.4.1p1-ifort14.0?bin?mpiexec -machinefile .?machines.LINUX -launcher rsh -launcher-exec ?usr?bin?rsh -n \$N ?home?yao?PROGRAM?VASP.5.3.3-mpich2_1.41p1-ifort14.0-fftw3.33?src?vasp.5.3?vasp"
#===== Test code =====#
if [ ! -d '${path_POTCAR}' ];then
echo "---       POTCAR directory is detected        ---"
else
echo "---    POTCAR directory isn't detected        ---"
fi
if [ ! -d '${path_INCAR}' ];then
echo "
---       INCAR directory is detected        ---
"
else
echo "---    INCAR directory isn't detected        ---"
fi
echo "###        Auto VASP INPUT file Creater       ###
### Please ensure the POSCAR file is already  ###
### Enter the input file you want to generate ###
###                 1.POTCAR                  ###
###                 2.KPOINTS                 ###
###                 3.INCAR                   ###
###                 4.Run Files               ###
###                 5.ALL Files               ###
###      Written by Yao with Linux shell      ###"
#===== Module code =====#
INCAR_cre(){
echo "---        Select the calculation type        ---
---      (relax,fre,NEB is supported now)     ---"
read incar_type
cp $path_INCAR/INCAR_$incar_type ./INCAR
###  Find out the largest ENMAX  ###
ele_num=($(awk -F ' ' '{print NF}' ./POSCAR|head -7|tail -1|awk '{printf "%d",$1}'))
for i in `seq 1 ${ele_num}`
do
ENMAX=($(grep ENMAX POTCAR | sed -n "${i}p" | awk '{print $3}' | tr -d ";" | awk '{print int($0)}' ))
if (( ${i}==1 )); then
all_ENMAX=$ENMAX
fi
if (( ${i}!=1 )); then
all_ENMAX=$all_ENMAX" "$ENMAX
fi
done
array_ENMAX=(`echo $all_ENMAX | tr ' ' ' '`)
#echo ${array_ENMAX[1]}
max_ENMAX=$[${array_ENMAX[0]}]
for (( i=0; i<$[${ele_num}]; i++ )) ; do
#for (( i=0; i<3; i++ )) ; do
if [ $[${array_ENMAX[$i]}] -gt $max_ENMAX ] ; then
max_ENMAX=$[${array_ENMAX[$i]}]
if [ $[${array_ENMAX[$i]}] -eq $max_ENMAX ] ; then
sum=(${array_ENMAX[$i]})
else
continue
fi
else
continue
fi
done
#echo $max_ENMAX
###  END  ###

###  Find out the largest EAUG  ###
for i in `seq 1 ${ele_num}`
do
EAUG=($(grep EAUG POTCAR | sed -n "${i}p" | awk '{print $3}' | tr -d ";" | awk '{print int($0)}' ))
if (( ${i}==1 )); then
all_EAUG=$EAUG
fi
if (( ${i}!=1 )); then
all_EAUG=$all_EAUG" "$EAUG
fi
done
array_EAUG=(`echo $all_EAUG | tr ' ' ' '`)
#echo ${array_EAUG[1]}
max_EAUG=$[${array_EAUG[0]}]

for (( i=0; i<$[${ele_num}]; i++ )) ; do
#for (( i=0; i<3; i++ )) ; do
if [ $[${array_EAUG[$i]}] -gt $max_EAUG ] ; then
max_EAUG=$[${array_EAUG[$i]}]
if [ $[${array_EAUG[$i]}] -eq $max_EAUG ] ; then
sum=(${array_EAUG[$i]})
else
continue
fi
else
continue
fi
done
#echo $max_EAUG
###  END  ###

sed -i "s/^.*ENCUT.*$/ENCUT  =      $max_ENMAX/" INCAR
sed -i "s/^.*ENAUG.*$/ENAUG  =      $max_EAUG/" INCAR

echo "
---         Get ENMAX, ENAUG from POTCAR      ---
---              INCAR CREATED                ---
"
}

KPOINTS_cre(){
cat>KPOINTS<<!
Automatic mesh
0
G
3 3 3
0.0 0.0 0.0
!
echo "---         Enter your KPOINTS as:3 3 3       ---"
read input
sed -i "4c ${input}" KPOINTS
echo "
---           GAMMA KPOINTS CREATED           ---
"
}

POTCAR_cre(){
ele_array=($(cat POSCAR|sed -n '6p'|tr -d '\n\r'))
ele_num=($(awk -F ' ' '{print NF}' POSCAR|head -7|tail -1|awk '{printf "%d",$1}'))
cp ${path_POTCAR}/${ele_array[0]}/POTCAR .
for ele in `seq 1 $[${ele_num}-1]`
do
cat ${path_POTCAR}/${ele_array[$ele]}/POTCAR >> ./POTCAR
done
echo "
---      Copy file from the appointed file    ---
---              POTCAR CREATED               ---
"
}

gofile_cre(){
echo "---        Select the machine cluster        ---
---   (bremen dubai osaka sapporo macau)     ---"
read name_machine
echo "---        Enter the total core numbers      ---"
read number_core
echo "---   Choose the used machine as:01..04 08   ---"
read number_machine

cat>go_$name_machine.sh<<!
#!/bin/bash

N=a
VASPCOMMAND="b"

                        cp POSCAR_old CONTCAR
                for num in 1 2 3 
                        do
                        cp CONTCAR POSCAR
                             \$VASPCOMMAND > vasp.\$num.log < /dev/null
                        cp OUTCAR OUTCAR_\$num
                        cp OSZICAR OSZICAR_\$num
                        cp CONTCAR CONTCAR_\$num
                        done
!
sed -i "3s/a/$number_core/g" go_$name_machine.sh
vaspcode=vaspcode_$name_machine
sed -i "4s/b/`eval echo '$'"$vaspcode"`/g" go_$name_machine.sh && sed -i "4s/?/\//g" go_$name_machine.sh
if  [ ! -f  "./machines.LINUX"  ]; then 
touch ./machines.LINUX
else
rm -f ./machines.LINUX
touch ./machines.LINUX
fi
array_machine=(${number_machine// / })
for i in ${array_machine[@]}
do
if [[ "$i" =~ .*"..".* ]]; then
i=(${i//../ })
for a in $(seq ${i[0]} ${i[1]})
do
a=$(printf "%02d\n" $a)
line=$name_machine'0'$a:
echo $line >> ./machines.LINUX
done
else
line=$name_machine$i:
echo $line >> ./machines.LINUX
fi
done
n=($(sed -n '$=' ./machines.LINUX))
core=`expr $number_core / $n`
sed -i "s/$/&${n}/g" ./machines.LINUX
}
#===== Main code =====#
#read -n1 arg
read arg
if (( ${arg}==4 )); then
gofile_cre
fi

if (( ${arg}==3 )); then
INCAR_cre
fi

if (( ${arg}==2 )); then
KPOINTS_cre
fi

if (( ${arg}==1 )); then
POTCAR_cre
fi

if (( ${arg}==5 )); then
POTCAR_cre
INCAR_cre
KPOINTS_cre
gofile_cre
cp POSCAR POSCAR_old
fi
