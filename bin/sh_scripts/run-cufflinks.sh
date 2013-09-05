input=1047-COPD.100K
input_ext=sorted.bam
INPUT="${input}.${input_ext}"

output_dir="${input}.cuff"
OUTPUT_DIR="-o ${output_dir}"

threads=16
THREADS="-p ${threads}"

gtf=/local/src/bowtie2-2.0.5/indexes/Homo_sapiens.GRCh37.71.gtf
GTF="--GTF ${gtf}"
#GTF=

CMD="cufflinks ${OUTPUT_DIR} ${THREADS} ${GTF} ${INPUT}"
echo ${CMD}
#time ${CMD}


