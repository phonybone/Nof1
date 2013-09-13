class VariantError(Exception):
    pass

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
        self.reported=False

        self.n_alignments=0
        self.n_wt=0
        self.n_mut=0
        self.n_spans=0
        
        # sanity check: length of seq:
        if var_type == 'SNP' or var_type == 'DEL':
            seq=ref_allele
        elif var_type == 'INS':
            seq=tum_seq2
        else:
            raise VariantError("Unknown var_type '%s'" % var_type)
        if len(seq) != self.stop-self.start+1:
            raise VariantError("Incorrect start/stop or seq length (%s): start=%s, stop=%s, seq='%s'" % \
                               (var_type, start, stop, seq))
        

    def is_expressed_in_seq(self, seq, pos):
        ''' 
        does an rnaseq read express the wt allele or something different? 
        returns ?
        '''
        # should put in a check to make sure the right chrom is being checked...

        # extract the portion of the seq in question:
        i=self.start - pos
        j=self.stop - pos
        expressed_seq=seq[i:j+1]

        if self.var_type == 'SNP' or self.var_type == 'INS':
            return expressed_seq == self.tum_seq2

        if self.var_type == 'INS':
            pass

        if self.var_type == 'DEL':
            return expressed_seq != self.ref_allele


        # this is redundant, as this error should have been caught in the constructor
        raise VariantError('variant: unknown type "%s"' % self.var_type)


    ref_types={
        'Frame_Shift_Del':   'auto',
        'Frame_Shift_Ins':   'auto',
        'In_Frame_Del':      'polyphen',
        'In_Frame_Ins':      'polyphen',
        'Missense_Mutation': 'polyphen',
        'Nonsense_Mutation': 'auto',
        'RNA':               'ignore',
        'Silent':            'ignore',
        'Splice_Site':       'auto'
        } 
    
    @property
    def ref_type(self):
        return ref_types[self.var_type]
