"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    fieldnames = (
        'datetime_utc',
        'distance_au',
        'velocity_km_s',
        'designation',
        'name',
        'diameter_km',
        'potentially_hazardous'
    )

    content_list = [
        {**c_approach.serialize(), **c_approach.neo.serialize()} for c_approach in results
    ]
    with open(filename, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
    for content_list in results:
        writer.writerow(content_list)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.

"""
    result_dict = []
    for content_list in results:

        c_data = {** c_data.serialize(), ** c_data.neo.serialize()}
        c_data["name"] = c_data["name"] if c_data["name"] != None else ""
        c_data["potentially_hazardous"] = bool(
            1) if content_list["potentially_hazardous"] else bool(0)

        result_dict.append(

            {
                "datetime_utc": c_data["datetime_utc"],
                "distance_au": c_data["distance_au"],
                "velocity_km_s": c_data["velocity_km_s"],
                "neo": {
                    "designation": c_data["designation"],
                    "name": c_data["name"],
                    "diameter_km": c_data["diameter_km"],
                    "potentially_hazardous": c_data["potentially_hazardous"],
                },
            }
        )
    with open(filename, "w") as outfile:
        json.dump(result_dict, outfile, sort_keys=True, indent="\t")
