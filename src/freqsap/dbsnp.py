import re
import requests
from freqsap.allele import Allele
from freqsap.report import ReferenceSNPReport
from freqsap.interfaces import VariantFrequencyAPI
from freqsap.study import Study
from freqsap.variation import Variation


class DBSNP(VariantFrequencyAPI):
    def get(self, variation: Variation) -> ReferenceSNPReport | None:
        freq_url = f"https://www.ncbi.nlm.nih.gov/snp/{variation}/download/frequency"
        r = requests.get(freq_url, headers={"Accept": "application/json"})

        sections = [re.split(r'\n+', x.strip()) for x in re.split(r'#Frequency Data Table', r.text)]
        
        if len(sections) < 2:
            print(variation)
            return None

        metadata_section = sections[0]
        studies_section = sections[1]

        metadata_section.pop()
        studies_section.pop(0)
        
        metadata: dict = {}
        for entry in metadata_section:
            key, value = entry.strip('#').split('\t')
            metadata[key] = value

        studies: list[Study] = []
        header = studies_section.pop(0).strip('#').split('\t')
        
        for entry in studies_section:
            tokens = entry.split('\t')

            if len(tokens) < 6:
                print(variation)
                return None

            source = tokens[0]
            population = tokens[1]
            group = tokens[2]
            size = tokens[3]
            ref = tokens[4]
            alts = tokens[5]

            ref_nucelotide, ref_frequency = ref.split('=')
            reference = Allele(ref_nucelotide, ref_frequency)
            alternatives: list[Allele] = []
            for alt in alts.split(','):
                alt_nucleotide, alt_frequency = alt.split('=')
                alternatives.append(Allele(alt_nucleotide, alt_frequency))

            study = Study(source, population, group, size, reference, alternatives)
            studies.append(study)

        return ReferenceSNPReport(variation, metadata, studies)

    def available(self) -> bool:
        # Placeholder implementation
        return True
