#!/bin/bash
#===== Advanced setting =====#
path_input=~/example/cp2k_input

#===== Test code =====#
if [ ! -d '${path_input}' ];then
echo "---      Input path is detected       ---"
else
echo "---      Input path isn't detected       ---"
fi
struc_input=$(ls *.cif)
if [ ! ${struc_input} ];then
echo "---    Structure file isn't detected     ---"
exit
else
echo "---    Structure file is detected     ---"
fi
echo "###        Auto cp2k INPUT file Creater       ###
###   Now only AIMD input file is supported   ###
###  Please ensure the .cif file is already   ###
### Enter the input file you want to generate ###
###           1.Basal .inp file               ###
###         2.Revise the .inp file            ###
###               3.Run Files                 ###
###              4.Quick start                ###
###        5.Append the restart setting       ###
###      Written by Yao with Linux shell      ###"
#===== Module code =====#
input_cre(){
cp $path_input/example.inp ./cp2k.inp
cell_length=($(grep _cell_length ${struc_input} | sed 's/\r//' | awk '{print $(NF)}'))
cell_angle=($(grep _cell_angle ${struc_input} | sed 's/\r//' | awk '{print $(NF)}'))
cell_length=${cell_length[@]}
cell_angle=${cell_angle[@]}
sed -i "/ABC/s/$/& ${cell_length}/g" ./cp2k.inp
sed -i "/ALPHA_BETA_GAMMA/s/$/& ${cell_angle}/g" ./cp2k.inp
element=($(grep Uiso ${struc_input} | awk '{print $NF}'|uniq))
for ele in ${element[@]}
do
tem=$(sed -e "s/ATOM/${ele}/" $path_input/element.inp)
echo "$tem" > ./ele_tem
sed -i "/&SUBSYS/r ./ele_tem" cp2k.inp
done
rm -f ./ele_tem
#fundamental setting for quick start
sed -i "/@SET PROJECT_name/s/$/& global/g" ./cp2k.inp
sed -i "/@SET STRUCTURE_file/s/$/& ${struc_input}/g" ./cp2k.inp
sed -i "/COORDINATE/s/$/& ${struc_input#*.}/g" ./cp2k.inp
sed -i "/@SET PERIODIC_para/s/$/& xyz/g" ./cp2k.inp
}

input_restart(){
ls *.restart
echo "---   Enter the restart file name   ---"
read name
sed -i "s/^.*@SET EXT_status.*$/@SET EXT_status 1/g" ./cp2k.inp
sed -i "s/^.*@SETEXT_file.*$/@SET EXT_file ${name}/g" ./cp2k.inp
}

input_revise(){
echo "--- Enter the step numbers, step time, temperature ---
---   Or press enter for default: 1500 0.5 298.15  ---"
read arg
para=(${arg// / })
if [ ! -n "${para}" ];then
echo "---              Use the default setting           ---"
sed -i "s/^.*@SET MDSTEP_num.*$/@SET MDSTEP_num 1500/g" ./cp2k.inp
sed -i "s/^.*@SET TIMESTEP_num.*$/@SET TIMESTEP_num 0.5/g" ./cp2k.inp
sed -i "s/^.*@SET TEMPERATURE_num.*$/@SET TEMPERATURE_num 298.15/g" ./cp2k.inp
else
sed -i "s/^.*@SET MDSTEP_num.*$/@SET MDSTEP_num ${para[0]}/g" ./cp2k.inp
sed -i "s/^.*@SET TIMESTEP_num.*$/@SET TIMESTEP_num ${para[1]}/g" ./cp2k.inp
sed -i "s/^.*@SET TEMPERATURE_num.*$/@SET TEMPERATURE_num ${para[2]}/g" ./cp2k.inp
fi
echo "--- Fix some atoms as '21 31 35..41' ---
---   Or press enter for not fixed   ---"
sed -i "s/^.*@SET FIX_status.*$/@SET FIX_status 0/g" ./cp2k.inp
read arg
para=(${arg// / })
if [ ! -n "${para}" ]; then
echo "---       No atom will be fixed      ---"
else
sed -i "s/^.*@SET FIX_status.*$/@SET FIX_status 1/g" ./cp2k.inp
sed -i "s/^.*LIST.*$/  LIST $para/g" ./cp2k.inp
fi
echo "--- Choose the THERMOSTAT 1:CSVR 2:NOSE ---"
read thermarg
if (( $thermarg == 1 )); then
sed -i "s/^.*@SET THERMO_para.*$/@SET THERMO_para CSVR/g" ./cp2k.inp
fi
if (( $thermarg == 2 )); then
sed -i "s/^.*@SET THERMO_para.*$/@SET THERMO_para NOSE/g" ./cp2k.inp
fi
}

go_cre(){
echo "---        Select the machine cluster        ---"
read name_machine
echo "---        Enter the total core numbers      ---"
read number_core
echo "---   Choose the used machine as:01..04 08   ---"
read number_machine
cat>go_cp2k.sh<<!
#!/bin/bash

N=n
cp2krun="/home/yao/PROGRAM/cp2k-8.1/tools/toolchain/install/openmpi-4.0.5/bin/mpirun -np \$N --hostfile ./slots --mca plm_rsh_agent rsh /home/yao/PROGRAM/cp2k-8.1/exe/local/cp2k.popt -i cp2k.inp"
\$cp2krun > cp2k.out < /dev/null
!
sed -i "3s/n/$number_core/g" ./go_cp2k.sh
if  [ ! -f  "./slots"  ]; then 
touch ./slots
else
rm -f ./slots
touch ./slots
fi
array_machine=(${number_machine// / })
#core=`expr $number_core / ${#array_machine[@]}`
for i in ${array_machine[@]}
do
if [[ "$i" =~ .*"..".* ]]; then
i=(${i//../ })
for a in $(seq ${i[0]} ${i[1]})
do
a=$(printf "%02d\n" $a)
line=$name_machine$a' slots='
echo $line >> ./slots
done
else
line=$name_machine$i' slots='
echo $line >> ./slots
fi
done
n=($(sed -n '$=' ./slots))
core=`expr $number_core / $n`
sed -i "s/$/&${core}/g" ./slots
}

#Main code
read inarg
case $inarg in 
1)
input_cre
;;
2)
input_revise
;;
3)
go_cre
;;
4)
input_cre
input_revise
go_cre
;;
5)
input_restart
;;
*)
echo "--- Input the correct number ---"
esac
echo "---                  DONE             ---"