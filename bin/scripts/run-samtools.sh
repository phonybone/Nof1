# convert sam->bam, sort bam
input=1047-COPD.100K
input_ext=bt2.sam
INPUT="${input}.${input_ext}"

output=1047-COPD.100K_2
output_ext=bam
OUTPUT="-o ${output}.${output_ext}"


#CMD="samtools view -bS ${OUTPUT} ${INPUT}"
CMD="samtools view -bSu ${INPUT} | samtools sort"
echo ${CMD}
#time ${CMD}

