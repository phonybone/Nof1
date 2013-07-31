export BOWTIE2_INDEXES=/local/src/bowtie2-2.0.5/indexes

index=hg19
threads=16
THREADS="-p ${threads}"
input=1047-COPD

1047-COPD_1.100K.fastq

INPUT="-1 ${input}_1.fastq -2 ${input}_2.fastq"
OUTPUT="-S ${input}.bt2.sam"
fuse_opt='-qupto 100000'

echo bowtie2 ${index} -q ${THREADS} ${INPUT} ${OUTPUT}
time bowtie2 ${index} -q ${THREADS} ${INPUT} ${OUTPUT}

