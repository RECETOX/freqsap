from __future__ import annotations
import argparse
import csv
import sys
from freqsap.accession import Accession
from freqsap.dbsnp import DBSNP
from freqsap.ebi import EBI
from freqsap.interfaces import ProteinVariantAPI
from freqsap.interfaces import VariantFrequencyAPI
from freqsap.report import ReferenceSNPReport
from freqsap.uniprot import UniProt


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Query protein variants and their frequencies from various databases.")

    parser.add_argument("accession", type=str, help="Protein accession identifier to query")

    parser.add_argument("output", type=str, help="Path to output file for results")

    parser.add_argument(
        "--protein-api",
        type=str,
        choices=["uniprot", "ebi"],
        default="ebi",
        help="Protein variant API to use (default: ebi)",
    )

    parser.add_argument(
        "--frequency-api",
        type=str,
        choices=["dbsnp"],
        default="dbsnp",
        help="Variant frequency API to use (default: dbsnp)",
    )

    parser.add_argument("--delimiter", type=str, default="\t", help="Delimiter for output file (default: tab)")

    return parser.parse_args()


def get_protein_api(api_name: str) -> ProteinVariantAPI:
    """Instantiate the chosen protein API."""
    apis = {"uniprot": UniProt, "ebi": EBI}
    return apis[api_name]()


def get_frequency_api(api_name: str) -> VariantFrequencyAPI:
    """Instantiate the chosen frequency API."""
    apis = {"dbsnp": DBSNP}
    return apis[api_name]()


def write_reports(reports: list[ReferenceSNPReport], output_path: str, delimiter: str) -> None:
    """Write all reports to the output file."""
    header = reports[0].header()
    for report in reports:
        other = report.header()
        if header < other:
            header.extend(other[len(header) :])

    with open(output_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=delimiter, extrasaction="ignore")
        writer.writeheader()

        for report in reports:
            writer.writerows(report.rows())


def check_apis(args, protein_api, frequency_api) -> None:
    if not protein_api.available():
        sys.exit(1)

    if not frequency_api.available():
        sys.exit(1)


def main() -> None:
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
    reports: list[ReferenceSNPReport] = list(
        filter(None, [frequency_api.get(variation) for variation in protein.variations]),
    )

    # Write reports to output file
    write_reports(reports, args.output, args.delimiter)



if __name__ == "__main__":
    main()
