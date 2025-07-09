from uuid import UUID, uuid4

from pymatgen.core.structure import Molecule
from pymatgen.analysis.graphs import MoleculeGraph
from pymatgen.analysis.local_env import OpenBabelNN
from pymatgen.io.ase import AseAtomsAdaptor

from ase import Atoms

from yarp.yarpecule import yarpeucle

from danger.io import (
    yarp_to_pmg_molecule,
    yarp_to_pmg_molgraph
)
from danger.provenance import Provenance, NetworkObject, Origin


class State:
    """
    A point (usually, but not always, a stationary point) on a potential energy surface.

    Args:
        state_id (UUID | str | None): Unique identifier for this network state
        mol (Molecule | MoleculeGraph | Atoms | yarpecule): Molecule object for this state. Can be a pymatgen
            Molecule or MoleculeGraph (preferred), ASE Atoms, or a YARP yarpecule.
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
        state_id: UUID | str | None,
        mol: Molecule | MoleculeGraph | Atoms | yarpecule,
        provenance: Provenance | None = None,
        charge: int | None = None,
        spin_multiplicity: int | None = None,
        energy: float | None = None,
        enthalpy: float | None = None,
        entropy: float | None = None,
        free_energy: float | None = None
        ):

        if state_id is None:
            self.id = uuid4()
        elif isinstance(state_id, str):
            self.id = UUID(state_id)
        else:
            self.id = state_id

        if isinstance(mol, Molecule):
            self.mol = MoleculeGraph.with_local_env_strategy(mol, OpenBabelNN())
        elif isinstance(mol, Atoms):
            molecule = AseAtomsAdaptor(mol).get_molecule
            self.mol = MoleculeGraph.with_local_env_strategy(molecule, OpenBabelNN())
        elif isinstance(mol, yarpecule):
            self.mol = yarp_to_pmg_molgraph(mol)
        else:
            self.mol = mol

        if provenance is None:
            self.provenance = Provenance(
                None,
                NetworkObject.STATE,
                self.id,
                Origin.START,  # Only time an object can lack a provenance is if it was an input structure
                parent_type=None,
                parent_id=None,
                calc_method=None,
                level_of_theory=None,
                index=None,
                path=None
            )

        # TODO: you are here
        if charge is None:
            self.charge = self.pmg_molecule.charge
        else:
            if spin_multiplicity is


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