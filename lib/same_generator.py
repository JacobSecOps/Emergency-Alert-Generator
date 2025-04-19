import requests
from lib.constants import CODES, ORIGINATORS
from lib.logger import *


def get_state_fips(state):
    info("Getting State FIPS Code...")
    url = "https://api.census.gov/data/2020/dec/pl?get=NAME&for=state"
    info(f"Querying {url} for State: {state}")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    header, *rows = data
    states_fips = {row[0]: row[1] for row in rows}

    for name, fips in states_fips.items():
        if name.lower() == state.lower():
            info(f"{state} FIPS Code: {fips}")
            return fips
    error(f"Unable to find FIPS Code for {state}. Check your spelling?")
    exit(1)
    return None


def get_county_fips(state_fips, county):
    info("Getting County FIPS Code...")
    url = f"https://api.census.gov/data/2020/dec/pl?get=NAME&for=county&in=state:{state_fips}"
    info(f"Querying {url} for County: {county}")
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    
    header, *rows = data
    county_fips = {row[0]: row[2] for row in rows}

    for name, county_fips in county_fips.items():
        if county.lower() in name.lower():
            info(f"{name} FIPS Code: {county_fips}")
            return county_fips
    error(f"Unable to find FIPS Code for {county}. Check your spelling?")
    exit(1)
    return None


# Example SAME Output: ZCZC-EAS-RWT-012345+0030-2780415-KABC/TV-
def generate_same_header(state, county, day, hour, minute, origin, event, duration, identification):
    info("Generating SAME Header...")
    state_fips = get_state_fips(state)
    county_fips = get_county_fips(state_fips, county)
    if (len(identification) > 8):
        error("Identification length cannot be greater than 8 characters.")
        exit(1)
        return
    identification_padded = "{:<8}".format(identification)


    same_header = f"ZCZC-{origin}-{event}-0{state_fips}{county_fips}+{duration}-{day}{hour}{minute}-{identification_padded}"
    info(f"Output SAME Header: {same_header}")
    return same_header





