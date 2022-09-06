
"""Classes to instantiate Near Earth Objects and Close Approaches."""

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO)."""

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = str(info["pdes"])
        self.name = info["name"] if info["name"] != "" else None
        self.diameter = float(
            info["diameter"] if info["diameter"] != "" else "nan")
        self.hazardous = bool(info['pha'] if info['pha'] == "Y" else None)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def serialize(self):
        """Serialize returns dictionary."""
        return {
            'designation': self.designation,
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        is_fullname = f"{self.designation} ({self.name})" if self.name else f"{self.designation}"
        return is_fullname

    def __str__(self):
        """Return `str(self)`."""
        is_hazardous = "is" if self.hazardous else "is not"

        return f'NEO {self.fullname} has a diameter of {self.diameter:.3} km and {is_hazardous} potentially hazardous'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO."""

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info["des"]

        self.time = cd_to_datetime(info["cd"])

        self.distance = float(info["dist"])
        self.velocity = float(info["v_rel"])

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    def serialize(self):
        """Serialize returns dictionary."""
        return {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity
        }

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        self.time = datetime_to_str(self.time)
        return f'{self.time}'

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
