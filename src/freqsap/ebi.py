from typing import Generator
import requests
from freqsap.accession import Accession
from freqsap.exceptions import AccessionNotFound
from freqsap.interfaces import ProteinVariantAPI
from freqsap.protein import Protein
from freqsap.variation import Variation


class EBI(ProteinVariantAPI):
    def __init__(self):
        self._headers = { "Accept" : "application/json"}
        self._timeout = 3
        pass

    def _request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self._headers, timeout=self._timeout)

    def available(self) -> bool:
        expected_response = '{"requestedURL":"https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100","errorMessage":["At least one of these request parameters is required: accession, disease, omim, evidence, taxid, dbtype or dbid"]}'
        reponse = self._request("https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100").text

        return reponse == expected_response
    
    def get(self, accession: Accession) -> Protein:
        response = self._request(f"https://www.ebi.ac.uk/proteins/api/variation/{accession}")
        _check_response(accession, response)
        variations = list(_get_variants(response.json()))
        return Protein(accession, variations)

def _get_dbsnp_id(xrefs: list[dict]) -> str | None:
    for xref in xrefs:
        if xref.get('name') in ['dbSNP', 'gnomAD', 'TOPMed'] and xref.get('id', '').startswith('rs'):
            return xref['id']


def _check_response(accession: Accession, response: requests.Response):
    if not response.ok:
        if response.reason == 'Not Found' and response.status_code == 404:
            raise AccessionNotFound(message=f"Accession {accession} not found.")
        response.raise_for_status()

def _get_variants(response: dict) -> Generator[Variation]:
    variants = list(filter(lambda x: x.get('type') == 'VARIANT', response['features']))
    for var in variants:
        if ref := _get_dbsnp_id(var['xrefs']):
            yield Variation(ref, var['begin'])
    
