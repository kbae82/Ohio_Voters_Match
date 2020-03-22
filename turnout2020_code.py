# --------------------------------------------------
# This script will fetch voter data file from the Ohio Secretary of State website
# and match them with the existing input file.
# As a result, a new CSV file (output.csv) will be generated.
# The data columns are row, name, birth_year, address, city, state, zip, and matched_voterid.
# (C) 2020 Kangyoon Bae
# kangyoon.bae@gmail.com
#

import csv
import json
from voter import Voter
from urllib.request import urlopen, Request
from urllib.error import URLError
from fuzzywuzzy import fuzz
from dateutil.parser import parse

# Data source URLs
URL_INPUT_CSV = 'https://drive.google.com/uc?export=download&id=1jAAgd5js_PtdFONuQFGXnni-Bdx0oEg4'
URL_DATA_SRC_CSV = 'https://www6.ohiosos.gov/ords/f?p=VOTERFTP:DOWNLOAD::FILE:NO:2:P2_PRODUCT_NUMBER:'
URL_OHIO_GIS = 'http://gis5.oit.ohio.gov/ArcGIS/rest/services/compositelocator/GeocodeServer/findAddressCandidates?SingleLine='

# list of voter object
input_voter_list = []


def load_csv(url):
    # Adding header value as a workaround HTTP 403 Error for the Ohio state website
    headers = {"User-Agent": "Mozilla/5.0"}
    req = Request(url=url, headers=headers)
    list_of_voter = []
    data = None
    row = None
    try:
        data = urlopen(req).read()
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    if data is None:
        return

    rows = csv.DictReader(data.decode('utf-8').splitlines(), skipinitialspace=True)
    for row in rows:
        row_as_dict = {k: v for k, v in row.items()}
        list_of_voter.append(row_as_dict)
    return list_of_voter


def create_voters_from_input_data():
    rows = load_csv(URL_INPUT_CSV)
    if rows is None:
        return
    for row in rows:
        input_voter_list.append(
            Voter(row['row'], row['name'], row['birth_year'], row['address'], row['city'], row['state'], row['zip']))
    return input_voter_list


def get_formatted_address_from_ohio_gis(address):
    # Future feature to check with OHIO GIS REST for Address candidates
    # print(get_formatted_address_from_OHIO_GIS("56 W Cross Street,Winchester"))
    # print(get_formatted_address_from_OHIO_GIS("14557 Township Hwy 60,Upper Sandusky"))
    # print(get_formatted_address_from_OHIO_GIS("1311-1/2 W Spring St,Lima"))

    if "po box" in address.lower():
        return address

    url_get_address = URL_OHIO_GIS + address.replace(' ', '+') +"&f=pjson"
    req = Request(url=url_get_address)

    try:
        data = json.loads(urlopen(req).read())
        if len(data['candidates']) > 0:
            return data['candidates'][0]['address']
        return address
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return address
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return address
    if data is None:
        return address


def match_with_county_data(county_data_src_url):
    rows = load_csv(county_data_src_url)

    for row in rows:
        for input_voter in input_voter_list:
            # If any of match filter is fail, skip the current row and continue to next row.
            # Search the exact matches for values Zip, State, City, Birth year, and Street number
            if input_voter.zip != int(row['RESIDENTIAL_ZIP']):
                continue
            if input_voter.state.lower() != row['RESIDENTIAL_STATE'].lower():
                continue
            if input_voter.city.lower() != row['RESIDENTIAL_CITY'].lower():
                continue
            if input_voter.birth_year != parse(row['DATE_OF_BIRTH'], fuzzy=True).year:
                continue
            # Empty address case
            if len(input_voter.address.split(maxsplit=1)) < 2:
                continue
            # Using fuzzy match for address information
            if input_voter.address.split(maxsplit=1)[0] != row['RESIDENTIAL_ADDRESS1'].strip().split(maxsplit=1)[0]:
                continue
            if fuzz.partial_ratio(input_voter.address.split(maxsplit=1)[1].lower(),
                                  row['RESIDENTIAL_ADDRESS1'].strip().split(maxsplit=1)[1].lower()) < 80:
                continue

            # Concat State voter's name
            src_full_name = row['FIRST_NAME'].strip() + " " + row['MIDDLE_NAME'].strip() + " " + row[
                'LAST_NAME'].strip()

            # Using fuzzy match for name
            if fuzz.partial_ratio(src_full_name.lower(), input_voter.name.lower()) < 70 and \
                    fuzz.token_sort_ratio(src_full_name.lower(), input_voter.name.lower()) < 70:
                continue

            # Match found, update matched_voterid
            input_voter.matched_voterid = row['SOS_VOTERID']


def create_output_csv_file():
    with open('output.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['row', 'name', 'birth_year', 'address', 'city', 'state', 'zip', 'matched_voterid'])
        for input_voter in input_voter_list:
            writer.writerow(list(input_voter))

def main():
    create_voters_from_input_data()
    match_with_county_data(URL_DATA_SRC_CSV + "1")
    match_with_county_data(URL_DATA_SRC_CSV + "2")
    match_with_county_data(URL_DATA_SRC_CSV + "3")
    match_with_county_data(URL_DATA_SRC_CSV + "4")
    create_output_csv_file()


if __name__ == '__main__':
    main()
