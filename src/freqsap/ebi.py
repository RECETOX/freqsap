import requests
from freqsap.accession import Accession
from freqsap.exceptions import AccessionNotFound
from freqsap.interfaces import ProteinVariantAPI
from freqsap.protein import Protein


class EBI(ProteinVariantAPI):
    def __init__(self):
        pass

    def available(self) -> bool:
        r = requests.get("https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100", headers={ "Accept" : "application/json"})
        responseBody = r.text
        expected_response = '{"requestedURL":"https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100","errorMessage":["At least one of these request parameters is required: accession, disease, omim, evidence, taxid, dbtype or dbid"]}'
        return responseBody == expected_response
    
    def get(self, accession: Accession) -> Protein:
        requestURL = f"https://www.ebi.ac.uk/proteins/api/proteins/{accession}"
        r = requests.get(requestURL, headers={ "Accept" : "application/xml"})
        if not r.ok:
            if r.reason == 'Not Found' and r.status_code == 404:
                raise AccessionNotFound(message=f"Accession {accession} not found.")
            r.raise_for_status()

        return Protein(accession, [])
