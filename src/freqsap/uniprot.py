from __future__ import annotations
import sys
import requests
from freqsap.accession import Accession
from freqsap.interfaces import ProteinVariantAPI
from freqsap.protein import Protein
from freqsap.variation import Variation


class UniProt(ProteinVariantAPI):
    def __init__(self):
        self._params = {"fields": ["accession", "xref_dbsnp"]}
        self._headers = {"accept": "application/json"}
        self._timeout = 3

    def get(self, accession: Accession) -> Protein:
        response = self.query(accession)
        variations = [self.parse(feature) for feature in response["features"]]

        return Protein(accession, variations)

    def query(self, accession: str) -> dict:
        base_url = f"https://rest.uniprot.org/uniprotkb/{accession}"
        response = self.request(base_url)

        if not response.ok:
            response.raise_for_status()
            sys.exit()

        return response.json()

    def parse(self, feature: dict) -> Variation | None:
        if feature["type"] != "Natural variant":
            return None

        xrefs = feature["featureCrossReferences"]
        position = int(feature["location"]["start"]["value"])

        for ref in xrefs:
            if self.is_dbsnp(ref):
                return Variation(ref["id"], position=position)

        return None

    def request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self._headers, params=self._params, timeout=self._timeout)

    def is_dbsnp(self, xref: dict) -> bool:
        return xref.get("database") == "dbSNP" and xref.get("id", "").startswith("rs")

    def available(self) -> bool:
        return self.request("https://rest.uniprot.org/uniprotkb/P68871").ok
