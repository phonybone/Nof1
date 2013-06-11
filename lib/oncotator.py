import requests, csv, re

class Oncotator(object):
    url='http://www.broadinstitute.org/oncotator/'

    class NoMutationInfo(Exception):
        pass

    def fetch_mutation_info(self, mutations):
        res=requests.post(self.url, {'id_data':mutations, 'csrfmiddlewaretoken': 'b17dedfa1397d4943ee52e7a6aee0664'})
        if res.status_code != requests.codes.ok:
            res.raise_for_status()

        regex=r'href="/oncotator/(download/[a-zA-Z0-9]+)">Download Table'
        mg=re.search(regex, res.content)
        if not mg:
            raise Oncotator.NoMutationInfo

        url2=self.url+mg.group(1)
        print 'url2: %s' % url2
        res2=requests.get(url2)
        if res2.status_code != requests.codes.ok:
            res2.raise_for_status()
        return res2.content
            
        

#http://www.broadinstitute.org/oncotator/download/91d9a953091e761d713f0fbf22913657
