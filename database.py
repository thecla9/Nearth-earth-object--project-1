"""Class to define the Near Earth Object database and link them with their associated Close Approaches."""


class NEODatabase:
    """A database of near-Earth objects and their close approaches."""

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # Generate a mapping for neos to its indexes
        des_to_index = {
            neo.designation: index
            for index, neo in enumerate(self._neos)
        }

        # Link the neos to their close approach
        for approach in self._approaches:
            if approach._designation in des_to_index.keys():
                # Assign the approach it's neo
                approach.neo = self._neos[des_to_index.get(
                    approach._designation)]
                # Add the approach to the neo approaches' list
                self._neos[des_to_index.get(
                    approach._designation)].approaches.append(approach)

        # Generate mappings for neos to designation and neos to names
        self._neos_to_des = {
            neo.designation: neo
            for neo in self._neos
        }
        self._neos_to_names = {neo.name: neo for neo in self._neos}

    def get_neo_by_designation(self, des):
        """Find and return an NEO by its primary designation.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self._neos_to_des.get(des.upper(), None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return self._neos_to_names.get(name.capitalize(), None)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        if filters:
            for approach in self._approaches:
                if all(map(lambda f: f(approach), filters)):
                    # if all(matches):
                    yield approach
        else:
            for approach in self._approaches:
                yield approach
