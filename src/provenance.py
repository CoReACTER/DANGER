from enum import Enum
from pathlib import Path
from uuid import UUID, uuid4


class NetworkObject(Enum):
    """
    Types of network objects (for Provenance)
    """
    STATE = 1  # Any PES point
    ENDPOINT = 2  # (Optimized) reaction endpoint
    TS = 3  # (Optimized) transition-state
    PATH = 4  # Reaction pathway (with associated STATEs)
    REACTION = 5  # Reaction (potentially w/ PATH, potentially w/ ENDPOINT & TS)
    ENSEMBLE = 6  # Reaction ensemble (made up of multiple related REACTIONs)
    UNKNOWN = -1


class Origin(Enum):
    """
    Sources of network objects (for Provenance)
    """
    START = 1  # Provided by the user as input
    FRAGMENT = 2  # Obtained by fragmenting a molecule
    RECOMB = 3  # Obtained by recombining some fragments
    CONF_SEARCH = 4  # Obtained via conformer search
    PATH_OPT = 5  # Obtained via reaction path optimization
    ENDPOINT = 6  # Obtained from some reaction endpoint


class Provenance():
    """
    Container class for data provenance

    Args:
        provenance_id (UUID | str | None): Unique identifier for this provenance.
        object_type (NetworkObject | int): Object type of the object with this provenance.
        object_id (UUID | str): Unique ID of the object with this provenance.
        origin_type (Origin | int): Source of the network object
        parent_type (NetworkObject | int | None): Object type of the parent of the network object, if present.
            Default is None, which is only appropriate if the object has origin START.
        parent_id (UUID | str | None): The unique identifier of the parent of the network object, if present.
            Default is None, which is only appropriate if the object has origin START.
        calc_method (str | None): Where relevant, calculation method used to obtain the object. Default is None.
        level_of_theory (str | None): Where relevant, level of theory used to obtain the object. Default is None.
        index (int | None): Specifically for reaction paths, the place of the object along the path, where 0 is the
            reactant endpoint and len(path) is the product endpoint. Default is None.
        path (str | Path | None): Path to directory where calculations relevant to the network object are stored.
            Default is None, indicating that there are no calculations relevant to this network object.
    """

    def __init__(
        provenance_id: UUID | str | None,
        object_type: NetworkObject | int,
        object_id: UUID | str,
        origin_type: Origin | int,
        parent_type: NetworkObject | int | None = None,
        parent_id: UUID | str | None = None,
        calc_method: str | None = None,
        level_of_theory: str | None = None,
        index: int | None = None,
        path: str | Path | None = None,
    ):

        if provenance_id is None:
            self.id = uuid4()
        elif isinstance(provenance_id, str):
            self.id = UUID(provenance_id)
        else:
            self.id = provenance_id

        if isinstance(object_type, NetworkObject):
            self.object_type = object_type
        else:
            self.object_type = NetworkObject(object_type)

        if isinstance(object_id, str):
            self.object_id = UUID(object_id)
        else:
            self.object_id = object_id

        if isinstance(parent_type, int):
            self.parent_type = NetworkObject(parent_type)
        else:
            self.parent_type = parent_type

        if isinstance(parent_id, str):
            self.parent_id = UUID(parent_id)
        else:
            self.parent_id = parent_id

        if isinstance(path, str):
            self.path = Path(path)
        else:
            self.path = path

        self.calc_method = calc_method
        self.level_of_theory = level_of_theory
        self.index = index

    def validate(self):
        raise NotImplementedError()

    