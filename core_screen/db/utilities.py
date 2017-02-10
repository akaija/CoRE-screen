import sys
import uuid

from sqlalchemy import MetaData, Table, select

from core_screen.db import Base, session, engine

meta = MetaData(bind=engine)
materials = Table('materials', meta, autoload=True)

def check_for_data(name):
    result = engine.execute(
            select(
                [materials.c.ga_absolute_volumetric_loading,
                    materials.c.sa_volumetric_surface_area,
                    materials.c.vf_helium_void_fraction],
                materials.c.name == name
            )
        )
    exists = False
    g = None
    s = None
    v = None
    for row in result:
        g = row[0]
        s = row[1]
        v = row[2]
    result.close()
    if g != None and s != None and v != None:
        exists = True

    return exists

