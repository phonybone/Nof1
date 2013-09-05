class Variant(object):
    def __init__(self, symbol, entrez, center, build, chrom, start, stop, 
                 strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2):
        self.symbol=symbol
        self.entrez=entrez
        self.center=center
        self.build=build
        self.chrom=chrom
        self.start=int(start)
        self.stop=int(stop)
        self.strand=strand
        self.var_class=var_class
        self.var_type=var_type
        self.ref_allele=ref_allele
        self.tum_seq1=tum_seq1
        self.tum_seq2=tum_seq2
        self.n_alignments=0
