import requests
from freqsap.accession import Accession
from freqsap.exceptions import AccessionNotFound
from freqsap.interfaces import ProteinVariantAPI
from freqsap.protein import Protein


class EBI(ProteinVariantAPI):
    def __init__(self):
        self._headers = { "Accept" : "application/json"}
        self._timeout = 3
        pass

    def _request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self._headers, timeout=self._timeout)

    def available(self) -> bool:
        r = self._request("https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100")
        responseBody = r.text
        expected_response = '{"requestedURL":"https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100","errorMessage":["At least one of these request parameters is required: accession, disease, omim, evidence, taxid, dbtype or dbid"]}'
        return responseBody == expected_response
    
    def get(self, accession: Accession) -> Protein:
        response = self._request(f"https://www.ebi.ac.uk/proteins/api/proteins/{accession}")
        _check_response(accession, response)
        variants = _get_variants(response.json())

        return Protein(accession, [])

def _check_response(accession: Accession, response: requests.Response):
    if not response.ok:
        if response.reason == 'Not Found' and response.status_code == 404:
            raise AccessionNotFound(message=f"Accession {accession} not found.")
        response.raise_for_status()

def _get_variants(response: dict) -> list[dict]:
    return list(filter(lambda x: x.get('type') == 'VARIANT', response['features']))
