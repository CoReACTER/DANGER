from uuid import UUID, uuid4
from typing import LIst

from pymatgen.core.structure import Molecule
from pymatgen.analysis.graphs import MoleculeGraph
from pymatgen.analysis.local_env import OpenBabelNN
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.babel import BabelMolAdaptor
from pymatgen.util.graph_hashing import weisfeiler_lehman_graph_hash

from ase import Atoms

from yarp.yarpecule import yarpeucle

import openbabel

from danger.io import (
    pmg_to_yarp,
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

        if charge is None:
            self.charge = self.pmg_molecule.charge
        else:
            self.charge = charge
        
        if spin_multiplicity is None:
            self.pmg_molecule.set_charge_and_spin(self.charge)
            self.spin_multiplicity = self.pmg_molecule.spin_multiplicity
        else:
            self.spin_multiplicity = spin_multiplicity
            self.pmg_molecule.set_charge_and_spin(self.charge, self.spin_multiplicity)

        self.energy = energy
        self.enthalpy = enthalpy
        self.entropy = entropy
        self.free_energy = free_energy

        self._generate_properties()

    @property
    def graph(self):
        return self.mol.graph

    @property
    def pmg_molecule(self):
        return self.mol.molecule

    @property
    def ase_atoms(self):
        return AseAtomsAdaptor(self.pmg_molecule).get_atoms()

    @property
    def yarpecule(self):
        return pmg_to_yarp(self.mol)

    def _generate_properties(self):
        # Mostly features for querying
        self.alphabetical_formula = self.pmg_molecule.composition.alphabetical_formula
        self.graph_hash = weisfeiler_lehman_graph_hash(self.graph, node_attr="specie")

        ad = BabelMolAdaptor(molecule)
        openbabel.StereoFrom3D(ad.openbabel_mol)
        self.smiles = ad.pybel_mol.write("can").strip()
        self.inchi = ad.pybel_mol.write("inchi").strip()
    

class Pathway:
    """
    A reaction pathway, represented as an ordered series of discrete States.

    Args:
        pathway_id (UUID | str | None): Unique identifier for this reaction pathway
        states (List[State]): Points along the path
        provenance (Provenance): Provenance for this path
    """
    def __init__(
        self,
        pathway_id: UUID | str | None,
        states: List[State],
        provenance: Provenance
    ):

        if pathway_id is None:
            self.id = uuid4()
        elif isinstance(pathway_id, str):
            self.id = UUID(pathway_id)
        else:
            self.id = pathway_id

        self.states = states
        self.provenance = provenance


class Reaction:
    """
    A reaction, defined by some reaction endpoints, complexes, and/or a reaction pathway

    Args:
        reaction_id (UUID | str | None): Unique identifier for this reaction
        provenance (Provenance): Provenance for this reaction
        reactants (List[State] | None): Isolated reactants as States. Default is None.
        products (List[State] | None): Isolated products as States. Default is None.
        reactant_complex (State | None): (Optimized) reaction entrance complex. Default is None.
        product_complex (State | None): (Optimized) reaction exit complex. Default is None.
        transition_state (State | None): Transition-state for this reaction. Default is None.
        pathway (Pathway | None): Points along a path for this reaction. Default is None.
        energy (float | None): Reaction energy change (ΔE) in eV. Default is None.
        enthalpy (float | None): Reaction enthalpy change (ΔH) in eV. Default is None.
        entropy (float | None): Reaction entropy change (ΔS) in eV K^-1. Default is None.
        free_energy (float | None): Reaction free energy change (ΔG) in eV. Default is None.
    """

    def __init__(
        self,
        reaction_id: UUID | str | None,
        provenance: Provenance,
        reactants: List[State] | None = None,
        products: List[State] | None = None,
        reactant_complex: State | None = None,
        product_complex: State | None = None,
        transition_state: State | None = None,
        pathway: Pathway | None = None,
        energy: float | None = None,
        enthalpy: float | None = None,
        entropy: float | None = None,
        free_energy: float | None = None
    ):

        if reaction_id is None:
            self.id = uuid4()
        elif isinstance(reaction_id, str):
            self.id = UUID(reaction_id)
        else:
            self.id = reaction_id

        self.provenance = provenance

        self.reactants = reactants
        self.products = products

        self.reactant_complex = reactant_complex
        self.product_complex = product_complex

        self.transition_state = transition_state

        self.pathway = pathway

        self.energy = energy
        self.enthalpy = enthalpy
        self.entropy = entropy
        self.free_energy = free_energy


class Ensemble:
    pass


class ReactionNetwork:
    pass