# convert sam->bam
input=1047-COPD.100K
input_ext=bam
INPUT="${input}.${input_ext}"

output=1047-COPD.100K
output_ext=sorted
OUT_PREFIX="${output}.${output_ext}"

CMD="samtools sort ${INPUT} ${OUT_PREFIX}"
echo ${CMD}
time ${CMD}
