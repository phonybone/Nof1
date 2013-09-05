import csv, re

class VepPolyphenSIFTFilter(object):
    '''
    Filter the VEP output, looking for mutations that are either:
    polyphen: damaging
    SIFT:     deletarious
    '''
    def __init__(self, vep_output_fn):
        self.vep_output_fn=vep_output_fn
        self.vep_filtered_fn='%s.filtered' % vep_output_fn
        self.filters=[r'PolyPhen=possibly_damaging;SIFT=deleterious',
                      r'PolyPhen=probably_damaging;SIFT=deleterious',
                      ]
        self.filter_col=13
        self.col_delimiter='\t'

    def go(self):
        stats={'n_passed':0,
               'n_rejected': 0,
               'n_total': 0}

        with open(self.vep_output_fn, 'r') as input:
            with open(self.vep_filtered_fn, 'w') as output:
                reader=csv.reader(input, delimiter=self.col_delimiter)
                for row in reader:
                    try:
                        stats['n_total']+=1
                        pp_sift=row[self.filter_col].strip()
                        found=False
                        for regex in self.filters:
                            if re.search(regex, pp_sift):
                                output.write(self.col_delimiter.join(row)+'\n')
                                found=True
                                break
                        stats['n_passed' if found else 'n_rejected']+=1

                    except IndexError:
                        pass
        return stats
