#!/bin/sh 
#echo `pwd`

#eval `scramv1 runtime -csh`
cd /afs/cern.ch/work/f/fdolek/public/dune
eval `scramv1 runtime -sh`

echo "my job started at"
echo `date`

./runlimit.sh


echo "my job completed at"
echo `date`
echo "BYE..."

# bsub -R "pool>3000" -q 1nd -o yesK_h1h1.log -J yesh1h1  batch.sh
