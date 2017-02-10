from sqlalchemy import *

from core_screen.db.__init__ import engine

meta = MetaData(bind=engine)
materials = Table('materials', meta, autoload=True)

def query_GA():
    cols = [materials.c.ga_absolute_volumetric_loading]
    result = engine.execute(select(cols))
    GA = []
    for row in result:
        GA.append(row[0])
    result.close()
    return GA

def query_SA():
    cols = [materials.c.sa_volumetric_surface_area]
    result = engine.execute(select(cols))
    SA = []
    for row in result:
        SA.append(row[0])
    result.close()
    return SA

def query_VF():
    cols = [materials.c.vf_helium_void_fraction]
    result = engine.execute(select(cols))
    VF = []
    for row in result:
        VF.append(row[0])
    result.close()
    return VF
