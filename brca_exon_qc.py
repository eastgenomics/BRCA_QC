#!/usr/bin/python3
"""
Script created to run on the BRCA reports and created an aggreagated exon QC.


Adriana Toutoudaki (March 2020), contact: adriana.toutoudaki@addenbrookes.nhs.uk
"""

import os
import argparse
import pandas as pd


def parse_arguments():
    """
    Parses specified arguments
    """
    parser = argparse.ArgumentParser(description='Quick QC for BRCA samples')
    parser.add_argument('run', help='Clinical pool run name i.e. CP0379A')
    parser.add_argument('-f', help='runfolder path if different from /mnt/storage/data/NGS/CP/')
    arguments = parser.parse_args()

    return arguments

def parse_file(file, path):
    """
    Adds CP folder path to sample file path and reads in QC tab in dataframe.
    """
    filepath = path + file

    data = pd.read_excel(filepath, sheet_name="QC", skiprows=[0, 1, 2], usecols="A:D")

    return data

def count_fails(data, gene):
    """
    Identifies which exons have failed with Minimum depth of coverage of less than 30.

    :param data: takes in a a BRCA dataframe for each sample
    :param gene: specify BRCA1 or BRCA2
    :return: a dictionary with exons as keys and value 0 for passed exons, 0 for failed exons.
    """

    if gene == "BRCA1":
        start = 0
        end = 21
    elif gene == "BRCA2":
        start = 23
        end = 48

    exon_numbers = {}


    for i in range(start, end):
        min_depth = int(data.loc[i]["Min depth"])
        exon = data.loc[i]["Name"]
        if min_depth < 30:
            exon_numbers[exon] = 1
        else:
            exon_numbers[exon] = 0

    return exon_numbers


def color_positive_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for positive
    strings, black otherwise.
    """
    color = 'red' if val > 0 else 'black'
    return 'color: %s' % color

def _color_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'background-color: red'` for intergers > 0,
    background stays white otherwise.
    """
    color = 'red' if val > 0 else 'white'
    return 'background-color: %s' % color


def main(args):

    # if -f isn't specified, it will analyse a folder in /mnt/storage/data/NGS/CP/
    if args.f is None:
        path = '/mnt/storage/data/NGS/CP/' + args.run + '/'
    else:
        path = args.f + args.run + '/'

    # Identify all samples in the runfolder requested
    path_files = os.listdir(path)

    samples = [sample for sample in path_files if sample.endswith(".xls")]



    # Exon names as present in the C01 reports
    brca_exons = ['BRCA1_exon2', 'BRCA1_exon3', 'BRCA1_exon5', 'BRCA1_exon6',
                  'BRCA1_exon7', 'BRCA1_exon8', 'BRCA1_exon9',
                  'BRCA1_exon10', 'BRCA1_exon11', 'BRCA1_exon12',
                  'BRCA1_exon13', 'BRCA1_exon14',
                  'BRCA1_exon15', 'BRCA1_exon16', 'BRCA1_exon17',
                  'BRCA1_exon18', 'BRCA1_exon19', 'BRCA1_exon20',
                  'BRCA1_exon21', 'BRCA1_exon22', 'BRCA1_exon23',
                  'BRCA2_exon2', 'BRCA2_exon3', 'BRCA2_exon4',
                  'BRCA2_exon5', 'BRCA2_exon6', 'BRCA2_exon7',
                  'BRCA2_exon8', 'BRCA2_exon9', 'BRCA2_exon10',
                  'BRCA2_exon11', 'BRCA2_exon12', 'BRCA2_exon13',
                  'BRCA2_exon14', 'BRCA2_exon15', 'BRCA2_exon16',
                  'BRCA2_exon17', 'BRCA2_exon18', 'BRCA2_exon19',
                  'BRCA2_exon20', 'BRCA2_exon21', 'BRCA2_exon22',
                  'BRCA2_exon23', 'BRCA2_exon24', 'BRCA2_exon25',
                  'BRCA2_exon26']

    # Creates a list of the brca samples in the runfolder
    brca_samples = []
    for sample in samples:
        if sample.startswith("C01") and (sample.endswith("b.xls") or sample.endswith("bW.xls")):
            brca_samples.append(sample)

    # Copy of the brca list to append a Total column and create an empty dataframe
    columns = brca_samples.copy()
    columns.append("Total")
    report = pd.DataFrame(index=brca_exons, columns=columns)

    # For each brca samples, parse the report, count the failed exons in brca1 and brca2
    for sample in brca_samples:

        data = parse_file(sample, path)
        brca1_fails = count_fails(data, "BRCA1",)
        brca2_fails = count_fails(data, "BRCA2", )

        # Annotate the reports using the failed exon dictionaries above
        for key in brca1_fails.keys():
            report.loc[key][sample] = brca1_fails[key]

        for key in brca2_fails.keys():
            report.loc[key][sample] = brca2_fails[key]

    # Calculate the total amount of times an exon has failed per run
    report["Total"] = report.sum(axis=1)

    # Apply colour highlighting
    new_report = report.style.applymap(_color_red)

    # Write the dataframe into a spreasheet
    outfile = str(args.run) + '_brcaQC.xlsx'
    writer = pd.ExcelWriter(outfile, engine='xlsxwriter')
    new_report.to_excel(writer, sheet_name='Run exon qc', startrow=1)
    worksheet = writer.sheets['Run exon qc']

    # Add a line with the total number of brca samples and other samples in the run
    worksheet.write(0, 0, 'BRCA Samples')
    worksheet.write(0, 1, len(brca_samples))
    worksheet.write(0, 2, 'Other Samples')
    worksheet.write(0, 3, (len(samples)-len(brca_samples)))

    # Set the column width to fit sample names
    worksheet.set_column('A:AZ', 18)

    writer.save()


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
