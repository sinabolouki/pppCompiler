#!/bin/zsh
for file in Samples/*.ppp;
do
  python parser.py -p "$file"
  filename=$(basename -- "$file")
  filename="${filename%.*}"
  llfilename="Samples/${filename}.ll"
  infilename="Samples/${filename}.in"
  outfilename="Samples/t${filename}.out"
  clang "$llfilename"
  ./a.out <"$infilename" >"$outfilename"
done


#python parser.py -p Samples/s1.ppp
#clang Samples/s1.ll
#./a.out < Samples/1.in  > Samples/test1.out
