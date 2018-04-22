import os
import sys
import csv


def convert_ourairport_to_csv(input_path, output_path):
    '''
    Takes in the airport.csv file from http://ourairports.com/data/ and outputs the local CSV
    that we use to populate our Location records

    The input file has these columns:
    "id","ident","type","name","latitude_deg"
    "longitude_deg","elevation_ft","continent", "iso_country","iso_region"
    "municipality","scheduled_service","gps_code","iata_code","local_code"
    "home_link","wikipedia_link","keywords"

    See below for the output columns.
    '''
    airport_reader = csv.reader(open(input_path))
    airport_writer = csv.writer(open(output_path, 'wb'))
    skipped_header = False
    for row in airport_reader:
        if not skipped_header:
            skipped_header = True
            continue
        if row[2] == 'closed':
            continue
        airport_writer.writerow([
            row[3],  # name
            row[2],  # type
            row[4],  # latitude
            row[5],  # longitude
            row[6],  # elevation
            row[8],  # ISO country
            row[9],  # ISO region
            row[10], # municipality
            row[12], # GPS code
            row[13], # IATA code
            row[14]  # local code
        ])


if __name__ == '__main__':
    convert_ourairport_to_csv(sys.argv[1], sys.argv[2])
