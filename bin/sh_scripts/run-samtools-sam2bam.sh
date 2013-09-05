# convert sam->bam
input=1047-COPD.100K
input_ext=bt2.sam
INPUT="${input}.${input_ext}"

output=1047-COPD.100K
output_ext=bam
OUTPUT="-o ${output}.${output_ext}"

CMD="samtools view -bS ${OUTPUT} ${INPUT}"
echo ${CMD}
time ${CMD}

