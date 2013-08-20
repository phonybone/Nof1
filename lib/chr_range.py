class ChrException(Exception): pass
class ChrIndexError(ChrException, IndexError): pass

from common_equality_mixin import CommonEqualityMixin, CommonInequalityMixin

class ChrRange(CommonEqualityMixin, CommonInequalityMixin):
    def __init__(self, chr, start, stop):
        self.chr=chr.lower()
        self.start=int(start)
        self.stop=int(stop)

        if not start <= stop:
            raise ChrIndexError('%s: start > stop' % self)
        if not self.chr.startswith('chr'):
            raise ChrException('bad chr: %s' % self.chr)
        n_part=self.chr[3:]



        try:
            n_chr=int(n_part)
            if n_chr < 1 or n_chr > 23:
                raise ChrIndexError('%s: chr out of range' % self)
            self.n_chr=n_chr
        except ValueError, e:
            bad_chr=e.message.split(':')[1].strip().upper()[1:-1]
            if bad_chr=='x':
                self.n_char=24
                self.chr='chrX'
            elif bad_chr=='y':
                self.n_char=25
                self.chr='chrY'
            else:
                raise ChrIndexError('%s: chr out of range ("%s")' % (self, bad_chr))
                


    def __str__(self):
#        return '%s: [%8d - %-8d]' % (self.chr, self.start, self.stop)
        return '\t'.join([self.chr, str(self.start), str(self.stop)])


    def __lt__(self, other):
        if self._CompatibleClassMixin__cmp_types(other):
            if self.n_chr != other.n_chr:
                return self.n_chr < other.n_chr
            else:
                return self.start < other.start
        raise TypeError("Incompatible types")

    def overlaps(s,o):
        if s.chr != o.chr: return False
        return ((s.start >= o.start) and (s.start <= o.stop)) or \
            ((o.start >= s.start) and (o.start <= s.stop))

