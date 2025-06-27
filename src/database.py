import sqlite3


create_provenance_table = """
    CREATE TABLE provenance (
        id                      TEXT NOT NULL PRIMARY KEY,
        object_type             INTEGER NOT NULL,
        object_id               TEXT NOT NULL,
        origin_type             INTEGER NOT NULL,
        parent_type             INTEGER,
        parent_id               INTEGER,
        calc_method             TEXT,
        level_of_theory         TEXT,
        index                   INTEGER
    );
"""

create_state_table = """
    CREATE TABLE states (
        id                      TEXT NOT NULL PRIMARY KEY,
        path                    TEXT NOT NULL,
        provenance_id           TEXT NOT NULL,
        alphabetical_formula    TEXT NOT NULL,
        graph_hash              TEXT NOT NULL,
        inchi                   TEXT NOT NULL,
        smiles                  TEXT,
        charge                  INTEGER NOT NULL,
        spin                    INTEGER NOT NULL,
        energy                  REAL,
        enthalpy_298            REAL,
        entropy_298             REAL,
        free_energy_298         REAL
    );
"""

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