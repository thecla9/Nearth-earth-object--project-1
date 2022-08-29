"""Functions to load the Nearth Earth Objects and Close Approaches from the data files."""

import csv
import json
from webbrowser import get
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """
    Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A list of `NearEarthObject`s.
    """
    try:
        with open(neo_csv_path) as f:
            reader = csv.DictReader(f)

            neos = []
            for neo in reader:
                neos.append(
                    NearEarthObject(
                        **{
                            'pdes':
                            neo.get('pdes', ''),
                            'name':
                            neo.get('name'),
                            'diameter':
                            neo.get('diameter'),
                            'pha':
                            neo.get('pha')
                        }))
            return neos
    except Exception as e:
        print('An error just occurred!', e)


def load_approaches(cad_json_path):
    """
    Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A list of `CloseApproach`es.
    """
    try:
        with open(cad_json_path) as f:
            reader = json.load(f)

            # Get the fields and data for the close approaches
            fields = reader.get('fields')
            data = reader.get('data')

            close_approaches = []
            for approach in data:
                # Create a close approach dictionary
                close_approach = {
                    fields[index]: value
                    for index, value in enumerate(approach)
                }
                # Add it to the list of all close approaches
                close_approaches.append(
                    CloseApproach(
                        **{
                            'des': close_approach.get('des'),
                            'cd': close_approach.get('cd'),
                            'dist': close_approach.get('dist'),
                            'v_rel': close_approach.get('v_rel')
                        }))

        return close_approaches
    except Exception as e:
        print('An error just occured!', e)
