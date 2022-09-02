"""Class to define the Near Earth Object database and link them with their associated Close Approaches."""


from ast import MatchAs


class NEODatabase:
    """A database of near-Earth objects and their close approaches."""

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        self._designation = {neo.des: neo for neo in self._neos}
        for approach in self._approaches:

            self.neos_by_name = {
                key.replace(key, value.name): value
                for key, value in self._designation.items()
                if value.name is not None

            }

        neo = self._designation[approach.des]
        approach.neo = neo
        neo.approaches.append(approach)

        # Generate mappings for neos to designation and neos to names
        self._neos_to_des = {
            neo.des: neo
            for neo in self._neos
        }
        self._neos_to_names = {neo.name: neo for neo in self._neos}

    def get_neo_by_designation(self, des):
        """Find and return an NEO by its primary designation.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self._des_to_neo.get(des.upper(), None)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return self.name_to_neo.get(name.capitalize(), None)

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
