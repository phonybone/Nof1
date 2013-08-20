
# bowtie2 (dry_run)
/local/bin/bowtie2 hg19 -p 2 -1 data/test_rnaseq/rawdata/1047-COPD.10K_1.fastq -2 data/test_rnaseq/rawdata/1047-COPD.10K_2.fastq -S d

# rnaseq_count (dry_run)
python /mnt/price1/vcassen/Nof1/bin/rnaseq_count.py data/test_rnaseq/rawdata/1047-COPD.10K.bt2.sam --out_fn data/test_rnaseq/rawdata/1047-COPD.10K.genes.count

# muts2vep (dry_run)
python /mnt/price1/vcassen/Nof1/bin/extract_trip_neg_details.py --in_fn data/trip_neg_Vic/triple_negativ_mut_seq --auto_fn data/trip_neg_Vic/triple_negativ_mut_seq.auto --poly_fn data/trip_neg_Vic/triple_negativ_mut_seq.poly

# vep (dry_run)
perl /mnt/price1/vcassen/Nof1/bin/variant_effect_predictor/variant_effect_predictor.pl -i data/trip_neg_Vic/triple_negativ_mut_seq.poly --cache --format guess --force_overwrite --poly p --sift p -o data/trip_neg_Vic/triple_negativ_mut_seq.vep.out

# filter_vep (dry_run)
python /mnt/price1/vcassen/Nof1/bin/filter_vep.py data/trip_neg_Vic/triple_negativ_mut_seq.vep.out

# combine rnaseq and vep (dry_run)
python /mnt/price1/vcassen/Nof1/bin/combine_rnaseq_vep.py \
 data/test_rnaseq/rawdata/1047-COPD.10K.genes.count \
 data/trip_neg_Vic/triple_negativ_mut_seq.auto \
 data/trip_neg_Vic/triple_negativ_mut_seq.vep.filtered \
 --out_fn /mnt/price1/vcassen/Nof1/data/1047-COPD.10K.genes.count.triple_negativ_mut_seq.auto.combined


