
import sys
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.sql import text

from core_screen import config
from core_screen.db import Base, session, engine

class Material(Base):
    """Declarative class mapping to table storing material/simulation data.

    Attributes:
        id (int): database table primary_key.
        name (str): identification string for material.
        ga_absolute_volumetric_loading (float): absolute volumetric loading.
        ga_absolute_gravimetric_loading (float): absolute gravimetric loading.
        ga_absolute_molar_loading (float): absolute molar loading.
        ga_excess_volumetric_loading (float): excess volumetric loading.
        ga_excess_gravimetric_loading (float): excess gravimetric loading.
        ga_excess_molar_loading (float): excess molar loading.
        ga_host_host_avg (float): average energy of host-host interactions.
        ga_host_host_vdw (float): energy of host-host van der Waals
            interactions.
        ga_host_host_cou (float): energy of host-host electrostatic
            interactions.
        ga_adsorbate_adsorbate_avg (float): average energy of adsorbate-
            adsorbate interactions.
        ga_adsorbate_adsorbate_vdw (float): energy of adsorbate-adsorbate van
            der Waals interactions.
        ga_adsorbate_adsorbate_cou (float): energy of adsorbate-adsorbate
            electrostatic interactions.
        ga_host_adsorbate_avg (float): average energy of host-adsorbate
            interactions.
        ga_host_adsorbate_vdw (float): energy of host-adsorbate van der Waals
            interactions.
        ga_host_adsorbate_cou (float): energy of host-adsorbate electrostatic
            interactions.
        sa_unit_cell_surface_area (float): surface area of unit-cell.
        sa_volumetric_surface_area (float): surface area per unit volume.
        sa_gravimetric_surface_area (float): surface area per unit mass.
        vf_helium_void_fraction (float): void fraction measured with helium
            probe.

    """
    __tablename__ = 'materials'
    # COLUMN                                                 UNITS
    id = Column(Integer, primary_key=True)                 # dimm.
    name = Column(String(150))

    # data collected
    ga0_absolute_volumetric_loading = Column(Float)            # cm^3 / cm^3
    ga0_absolute_gravimetric_loading = Column(Float)           # cm^3 / g
    ga0_absolute_molar_loading = Column(Float)                 # mol / kg
    ga0_excess_volumetric_loading = Column(Float)              # cm^3 / cm^3
    ga0_excess_gravimetric_loading = Column(Float)             # cm^3 / g
    ga0_excess_molar_loading = Column(Float)                   # mol /kg
    ga0_host_host_avg = Column(Float)                          # K
    ga0_host_host_vdw = Column(Float)                          # K
    ga0_host_host_cou = Column(Float)                          # K
    ga0_adsorbate_adsorbate_avg = Column(Float)                # K
    ga0_adsorbate_adsorbate_vdw = Column(Float)                # K
    ga0_adsorbate_adsorbate_cou = Column(Float)                # K
    ga0_host_adsorbate_avg = Column(Float)                     # K
    ga0_host_adsorbate_vdw = Column(Float)                     # K
    ga0_host_adsorbate_cou = Column(Float)                     # K

    ga1_absolute_volumetric_loading = Column(Float)            # cm^3 / cm^3
    ga1_absolute_gravimetric_loading = Column(Float)           # cm^3 / g
    ga1_absolute_molar_loading = Column(Float)                 # mol / kg
    ga1_excess_volumetric_loading = Column(Float)              # cm^3 / cm^3
    ga1_excess_gravimetric_loading = Column(Float)             # cm^3 / g
    ga1_excess_molar_loading = Column(Float)                   # mol /kg
    ga1_host_host_avg = Column(Float)                          # K
    ga1_host_host_vdw = Column(Float)                          # K
    ga1_host_host_cou = Column(Float)                          # K
    ga1_adsorbate_adsorbate_avg = Column(Float)                # K
    ga1_adsorbate_adsorbate_vdw = Column(Float)                # K
    ga1_adsorbate_adsorbate_cou = Column(Float)                # K
    ga1_host_adsorbate_avg = Column(Float)                     # K
    ga1_host_adsorbate_vdw = Column(Float)                     # K
    ga1_host_adsorbate_cou = Column(Float)                     # K

    sa_unit_cell_surface_area = Column(Float)                 # angstroms ^ 2
    sa_volumetric_surface_area = Column(Float)                # m^2 / cm^3
    sa_gravimetric_surface_area = Column(Float)               # m^2 / g
    vf_helium_void_fraction = Column(Float)                   # dimm.

    def __init__(self, name, ):
        """Init material-row.

        Args:
            self (class): row in material table.
            run_id : identification string for run (default = None).

        Initializes row in materials datatable.

        """
        self.name = name
