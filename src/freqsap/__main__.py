import argparse
import csv
import sys
from freqsap.accession import Accession
from freqsap.report import ReferenceSNPReport
from freqsap.uniprot import UniProt
from freqsap.ebi import EBI
from freqsap.dbsnp import DBSNP
from freqsap.interfaces import ProteinVariantAPI, VariantFrequencyAPI


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Query protein variants and their frequencies from various databases.'
    )
    
    parser.add_argument(
        'accession',
        type=str,
        help='Protein accession identifier to query'
    )
    
    parser.add_argument(
        'output',
        type=str,
        help='Path to output file for results'
    )
    
    parser.add_argument(
        '--protein-api',
        type=str,
        choices=['uniprot', 'ebi'],
        default='ebi',
        help='Protein variant API to use (default: ebi)'
    )
    
    parser.add_argument(
        '--frequency-api',
        type=str,
        choices=['dbsnp'],
        default='dbsnp',
        help='Variant frequency API to use (default: dbsnp)'
    )
    
    return parser.parse_args()


def get_protein_api(api_name: str) -> ProteinVariantAPI:
    """Instantiate the chosen protein API."""
    apis = {
        'uniprot': UniProt,
        'ebi': EBI
    }
    return apis[api_name]()


def get_frequency_api(api_name: str) -> VariantFrequencyAPI:
    """Instantiate the chosen frequency API."""
    apis = {
        'dbsnp': DBSNP
    }
    return apis[api_name]()


def write_reports(reports: list[ReferenceSNPReport], output_path: str):
    """Write all reports to the output file."""

    header = reports[0].header()
    for report in reports:
        other = report.header()
        if header < other:
            header.extend(other[len(header):])

    with open(output_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter='\t', extrasaction='ignore')
        writer.writeheader()

        for report in reports:
            writer.writerows(report.rows())

def check_apis(args, protein_api, frequency_api):
    if not protein_api.available():
        print(f"Error: {args.protein_api} API is not available", file=sys.stderr)
        sys.exit(1)
    
    if not frequency_api.available():
        print(f"Error: {args.frequency_api} API is not available", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the freqsap application."""
    args = parse_args()
    
    # Instantiate chosen APIs
    protein_api = get_protein_api(args.protein_api)
    frequency_api = get_frequency_api(args.frequency_api)
    
    # Check if APIs are available
    check_apis(args, protein_api, frequency_api)
    
    # Query protein variants
    accession = Accession(args.accession)
    protein = protein_api.get(accession)
    
    # Collect frequency reports for all variants
    reports: list[ReferenceSNPReport] = list(filter(None, [frequency_api.get(variation) for variation in protein.variations]))

    
    # Write reports to output file
    write_reports(reports, args.output)
    
    print(f"Successfully processed {len(reports)} variants and wrote results to {args.output}")

if __name__ == '__main__':
    main()
