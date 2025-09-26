from typing import Optional
import requests, sys, json


from freqsap.accession import Accession
from freqsap.interfaces import ProteinVariantAPI
from freqsap.protein import Protein
from freqsap.variation import Variation


class UniProt(ProteinVariantAPI):
    def __init__(self):
        self._params = {"fields": ["accession", "xref_dbsnp"]}

        self._headers = {"accept": "application/json"}

    def get(self, accession: Accession) -> Protein:
        # Placeholder implementation
        response = self.query(accession)
        variations = [self.parse(feature) for feature in response["features"]]

        protein = Protein(accession, variations)
        return protein

    def query(self, accession: str):
        base_url = f"https://rest.uniprot.org/uniprotkb/{accession}"
        response = requests.get(base_url, headers=self._headers, params=self._params)

        if not response.ok:
            response.raise_for_status()
            sys.exit()

        return response.json()

    def parse(self, feature: dict) -> Optional[Variation]:
        if feature["type"] != "Natural variant":
            return None

        xrefs = feature["featureCrossReferences"]
        for ref in xrefs:
            if self.is_dbsnp(ref):
                return Variation(ref["id"])

        pass

    def is_dbsnp(self, xref: dict) -> bool:
        return xref.get("database") == "dbSNP" and xref.get("id", "").startswith("rs")

    def available(self) -> bool:
        return requests.get("https://rest.uniprot.org/uniprotkb/P68871", headers=self._headers, params=self._params).ok
