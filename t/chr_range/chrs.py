from chr_range import ChrRange


'''
----5----1----5----2----5----3----5----4
c11:          ===========
c12:          ===========
c13:     ================
c14:          ================
c15      =====================
c16              ======  
c17                    ==========
c18                              =======
'''
c11=ChrRange('chr1', 10, 20)
c12=ChrRange('chr1', 10, 20)
c13=ChrRange('chr1',  5, 20)
c14=ChrRange('chr1', 10, 25)
c15=ChrRange('chr1',  5, 25)
c16=ChrRange('chr1', 12, 18)
c17=ChrRange('chr1', 19, 34)
c18=ChrRange('chr1', 35, 40)

c21=ChrRange('chr2', 10, 20)
c22=ChrRange('chr2', 15, 20)
