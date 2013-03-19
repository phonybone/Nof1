class DrugcardBuilder(object):
    def __init__(self):
        pass

    def onbegin_dc(self, mo):
        raise NotImplementedError('onbegin_dc')

    def onattr_name(self, mo):
        raise NotImplementedError('onbegin_dc')

    def onvalue(self, mo):
        raise NotImplementedError('onbegin_dc')

    def onseq_desc(self, mo):
        raise NotImplementedError('onbegin_dc')

    def onseq(self, mo):
        raise NotImplementedError('onbegin_dc')

    def onend_dc(self, mo):
        raise NotImplementedError('onbegin_dc')

    def ondtnan(self, mo):
        raise NotImplementedError('onbegin_dc')
