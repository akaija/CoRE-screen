import sys
import os
import subprocess
import shutil
from datetime import datetime
from uuid import uuid4

import core_screen
from core_screen import config

def write_raspa_file(filename, name):
    """Writes RASPA input file for calculating surface area.

    Args:
        filename (str): path to input file.
        run_id (str): identification string for run.
        material_id (str): name for material.

    Writes RASPA input-file.

    """
    simulation_cycles = config['surface_area']['simulation_cycles']
    with open(filename, "w") as raspa_input_file:
        raspa_input_file.write(
            "SimulationType         MonteCarlo\n" +
            "NumberOfCycles         %s\n" % (simulation_cycles) +             # number of MonteCarlo cycles
            "PrintEvery             1\n" +
            "PrintPropertiesEvery   1\n" +
            "\n" +
            "Forcefield             GenericMOFs" +
            "CutOff                 12.8\n" +                        # electrostatic cut-off, Angstroms
            "\n" +
            "Framework                  0\n" +
            "FrameworkName              %s\n" % (name) +
            "UnitCells                  3 3 3\n" +
            "SurfaceAreaProbeDistance   Minimum\n" +
            "\n" +
            "Component 0 MoleculeName               N2\n" +
            "            StartingBead               0\n" +
            "            MoleculeDefinition         TraPPE\n" +
            "            SurfaceAreaProbability     1.0\n" +
            "            CreateNumberOfMolecules    0\n")

def parse_output(output_file):
    """Parse output file for void fraction data.

    Args:
        output_file (str): path to simulation output file.

    Returns:
        results (dict): total unit cell, gravimetric, and volumetric surface
            areas.

    """
    results = {}
    with open(output_file) as origin:
        count = 0
        for line in origin:
            if "Surface area" in line:
                if count == 0:
                    results['sa_unit_cell_surface_area'] = float(line.split()[2])
                    count = count + 1
                elif count == 1:
                    results['sa_gravimetric_surface_area'] = float(line.split()[2])
                    count = count + 1
                elif count == 2:
                    results['sa_volumetric_surface_area'] = float(line.split()[2])

    print(
        "\nSURFACE AREA\n" +
        "%s\tA^2\n"      % (results['sa_unit_cell_surface_area']) +
        "%s\tm^2/g\n"    % (results['sa_gravimetric_surface_area']) +
        "%s\tm^2/cm^3"   % (results['sa_volumetric_surface_area']))
    return results

def run(name):
    """Runs surface area simulation.

    Args:
        run_id (str): identification string for run.
        material_id (str): unique identifier for material.

    Returns:
        results (dict): surface area simulation results.

    """
    simulation_directory  = config['simulations_directory']


    if simulation_directory == 'LOCAL':
        core_screen_dir = os.path.dirname(core_screen.__file__)
        path = os.path.join(core_screen_dir, name)
    elif simulation_directory == 'SCRATCH':
        path = os.environ['SCRATCH']
    else:
        print('OUTPUT DIRECTORY NOT FOUND.')
    output_dir = os.path.join(path, 'output_%s_%s' % (name, uuid4()))


    print("Output directory :\t%s" % output_dir)
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "SurfaceArea.input")


    write_raspa_file(filename, name)
    force_field_path = os.path.join(
            core_screen_dir, 'simulation', 'GenericMOFs')
    shutil.copy(os.path.join(force_field_path, 'force_field_mixing_rules.def'),
            output_dir)
    shutil.copy(os.path.join(force_field_path, 'force_field.def'), output_dir)
    shutil.copy(os.path.join(force_field_path, 'pseudo_atoms.def'), output_dir)
    cif_path = os.path.join(core_screen_dir, 'core-mof-july2014')
    shutil.copy(os.path.join(cif_path, '%s.cif' % name), output_dir)


    while True:
        try:
            print("Date :\t%s" % datetime.now().date().isoformat())
            print("Time :\t%s" % datetime.now().time().isoformat())
            print("Calculating surface area of %s..." % (name))
            subprocess.run(['simulate', './SurfaceArea.input'], check=True, cwd=output_dir)

            filename = "output_%s_3.3.3_298.000000_0.data" % (name)
            output_file = os.path.join(output_dir, 'Output', 'System_0', filename)
            results = parse_output(output_file)
#            shutil.rmtree(output_dir, ignore_errors=True)
            sys.stdout.flush()
        except (FileNotFoundError, KeyError) as err:
            print(err)
            print(err.args)
            continue
        break

    return results
