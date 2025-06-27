import networkx as nx

from pymatgen.core.structure import Molecule
from pymatgen.analysis.graphs import MoleculeGraph
from pymatgen.analysis.local_env import NearNeighbors, OpenBabelNN
from pymatgen.io.ase import AseAtomsAdaptor

from ase import Atoms
from ase.io import read, write

from yarp import yarpecule


def pmg_to_yarp(pmg_mol: Molecule | MoleculeGraph, strategy: NearNeighbors = OpenBabelNN):
    """
    Convert a pymatgen `Molecule` object to a YARP `yarpecule`.

    Args:
        pmg_mol (Molecule | MoleculeGraph): The molecule object to be converted
        strategy (NearNeighbors): strategy to use to determine which atoms are connected. Default is OpenBabelNN,
            which uses OpenBabel's internal bond detection algorithm.

    Returns:
        yarpecule
    """

    if isinstance(pmg_mol, Molecule):
        mg = MoleculeGraph.with_local_env_strategy(pmg_mol, strategy)
    else:
        mg = pmg_mol

    adjmat = nx.adjacency_matrix(mg.graph.to_undirected())
    geo = mg.molecule.cart_coords
    elements = [str(e) for e in mg.molecule.species]

    charge = mg.molecule.charge

    return yarpecule((adjmat, geo, elements, charge))


def yarp_to_pmg_molecule(yarp_mol: yarpecule):
    """
    Convert a YARP `yarpecule` into a pymatgen `Molecule` object
    
    Args:
        yarp_mol (yarpecule): The molecule to be converted

    Returns:
        Molecule
    """

    return Molecule(
        yarp_mol.elements,
        yarp_mol.geo,
        charge=yarp_mol.q
    )


def yarp_to_pmg_molgraph(yarp_mol: yarpecule):
    """
    Convert a YARP `yarpecule` into a pymatgen `MoleculeGraph` object
    
    Args:
        yarp_mol (yarpecule): The molecule to be converted

    Returns:
        MoleculeGraph
    """

    species = yarp_mol.elements
    positions = yarp_mol.geo
    charge = yarp_mol.q

    edges = dict()
    n = len(species)

    for i in range(n):
        for j in range(i):
            if yarp_mol.adj_mat[i, j] == 1:
                edges[(i, j)] = None

    return MoleculeGraph.from_edges(
        Molecule(species, positions, charge=charge),
        edges
    )


def yarp_to_ase(yarp_mol: yarpecule):
    ad = AseAtomsAdaptor()

    return ad.get_atoms(
        yarp_to_pmg_molecule(yarp_mol)
    )


def ase_to_yarp(ase_mol: Atoms):
    ad = AseAtomsAdaptor()

    return pmg_to_yarp(
        ad.get_molecule(ase_mol)
    )
