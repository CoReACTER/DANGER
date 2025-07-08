from pymatgen.core.structure import Molecule
from pymatgen.analysis.graphs import MoleculeGraph
from pymatgen.io.ase import AseAtomsAdaptor

from ase import Atoms

from yarp.yarpecule import yarpeucle

from danger.io import (
    yarp_to_pmg_molecule,
    yarp_to_pmg_molgraph
)
from danger.provenance import Provenance


class State:
    """
    A point (usually, but not always, a stationary point) on a potential energy surface.

    Args:
        mol (Molecule | MoleculeGraph | Atoms | yarpecule | str): Molecule object for this state. Can be a pymatgen
            Molecule or MoleculeGraph (preferred), ASE Atoms, YARP yarpecule, or a string (assumed to be SMILES).
        provenance (Provenance | None): Provenance for this state. Default is None, meaning that there is no
            provenance; this is only appropriate for initially provided species.
        charge (int | None): Molecular charge. If None (default), the charge will be inferred from `mol`. 
        spin_multiplicity (int | None): Molecular spin multiplicity. If None (default), the spin will be inferred from
            `mol`.
        energy (float | None): Energy of this PES state in eV. Default is None.
        enthalpy (float | None): Enthalpy of this PES state in eV. Default is None.
        entropy (float | None): Entropy of this PES state in eV K^-1. Default is None.
        free_energy (float | None): Free energy of this PES state in eV. Default is None.
    """
    
    def __init__(
        self,
        mol: Molecule | MoleculeGraph | Atoms | yarpecule | str,
        provenance: Provenance | None = None,
        charge: int | None = None,
        spin_multiplicity: int | None = None,
        energy: float | None = None,
        enthalpy: float | None = None,
        entropy: float | None = None,
        free_energy: float | None = None
        ):

        pass

    def _generate_properties(self):
        pass

    @property
    def graph(self):
        pass

    @property
    def pmg_molecule(self):
        pass

    @property
    def ase_atoms(self):
        pass

    @property
    def yarpecule(self):
        pass
    


create_reaction_table = """
    CREATE TABLE reactions (
        id                      TEXT NOT NULL PRIMARY KEY,
        provenance_id           TEXT NOT NULL,
        number_reactants        INTEGER NOT NULL,
        number_products         INTEGER NOT NULL,
        reactant_1_id           TEXT,
        reactant_2_id           TEXT,
        reactant_3_id           TEXT,
        reactant_complex_id     TEXT NOT NULL,
        product_1_id            TEXT,
        product_2_id            TEXT,
        product_3_id            TEXT,
        product_complex_id      TEXT NOT NULL,
        transition_state_id     TEXT,
        dE                      REAL,
        dH_298                  REAL,
        dS_298                  REAL,
        dG_298                  REAL
    );
"""

class Reaction:
    pass


class Ensemble:
    pass


class ReactionNetwork:
    pass