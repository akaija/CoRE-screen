#!/usr/bin/env python3
from datetime import datetime
import os

import click
import yaml
import RASPA2

import core_screen
from core_screen.files import load_config_file
from core_screen.core_screen import worker_run_loop

@click.group()
def cs():
    pass

@cs.command()
@click.argument('config_path',type=click.Path())
def start(config_path):
    """Create a new run.
    
    Args:
        config_path (str): path to config-file (ex: setting/core_screen.sample.yaml)

    Prints run_id, creates run-folder with config-file.

    """
    config = load_config_file(config_path)
    core_screen_dir = os.path.dirname(os.path.dirname(core_screen.__file__))
    run_id = datetime.now().isoformat()
    config['run_id'] = run_id
    config['raspa2_dir'] = os.path.dirname(RASPA2.__file__)
    config['core_screen_dir'] = core_screen_dir
    
    run_dir = os.path.join(core_screen_dir, run_id)
    os.makedirs(run_dir, exist_ok=True)
    file_name = os.path.join(run_dir, 'config.yaml')
    with open(file_name, 'w') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)
    print('Run created with id: %s' % run_id)

@cs.command()
@click.argument('run_id')
def launch_worker(run_id):
    """Start process to manage run.

    Args:
        run_id (str): identification string for run.

    Runs HTSOHM-method in one process.

    """
    core_screen._init(run_id)
    worker_run_loop(run_id)

if __name__ == '__main__':
    cs()
