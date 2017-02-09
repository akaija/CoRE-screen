import os
import sys
from math import sqrt
from datetime import datetime

import numpy as np
from sqlalchemy.sql import func, or_
from sqlalchemy.orm.exc import FlushError

import core_screen
from core_screen import config
from core_screen.db import session, Material
from core_screen.db.utilities import check_database
from core_screen import simulation

def run_all_simulations(material):
    """Simulate helium void fraction, gas loading, and surface area.

    Args:
        material (sqlalchemy.orm.query.Query): material to be analyzed.

    Depending on properties specified in config, adds simulated data for helium
    void fraction, gas loading, heat of adsorption, surface area, and
    corresponding bins to row in database corresponding to the input-material.
        
    """
    simulations = config['material_properties']
    ############################################################################
    # run helium void fraction simulation
    if 'helium_void_fraction' in simulations:
        results = simulation.helium_void_fraction.run(material.name)
        material.update_from_dict(results)
    ############################################################################
    # run gas loading simulation
    if 'gas_adsorption' in simulations:
        arguments = [material.name]
        if 'helium_void_fraction' in simulations:
            arguments.append(material.vf_helium_void_fraction)
        results = simulation.gas_adsorption.run(*arguments)
        material.update_from_dict(results)
    ############################################################################
    # run surface area simulation
    if 'surface_area' in simulations:
        results = simulation.surface_area.run(material.name)
        material.update_from_dict(results)

def worker_run_loop(run_id):
    """
    Args:
        run_id (str): identification string for run.

    Writes seed generation and simulates properties, then manages overall
    bin-mutate-simualte routine until convergence cutt-off or maximum
    number of generations is reached.

    """
    core_screen_dir = os.path.dirname(core_screen.__file__)
    core_mof_dir = os.path.join(core_screen_dir, 'core-mof-july2014')
    material_names = os.listdir(core_mof_dir)

    for cif_name in material_names:
        name = cif_name[:-4]
        print(name)
        if not check_database(name):
            material = Material(name)
            material.name = name
            session.add(material)
            session.commit()
#        try:
            run_all_simulations(material)
#            session.add(material)
            session.commit()
        else:
            print('Material %s already in database!' % name)
#        except:
#            pass

        sys.stdout.flush()
