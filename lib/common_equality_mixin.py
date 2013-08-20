class CompatibleClassMixin(object):
    def __cmp_types(self, other):
        return type(other) is type(self) or \
            isinstance(self, other.__class__) or \
            isinstance(other, self.__class__)


class CommonEqualityMixin(CompatibleClassMixin):
    def __eq__(self, other):
        if self._CompatibleClassMixin__cmp_types(other):
            return self.__dict__ == other.__dict__
        raise TypeError("Incompatible types")

    def __ne__(self, other):
        return not self.__eq__(other)


class CommonInequalityMixin(CompatibleClassMixin):
    '''
    Consuming class must define __lt__ and __eq__
    '''
    def __lte__(self, other):
        return self.__lt__(other) or self.__eq__(other)
    def __gt__(self,other):
        return not self.__lte__(other)
    def __gte__(self,other):
        return not self.__lt__(other)
    
