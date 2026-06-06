#importing library
import pandas as pd
from mp_api.client import MPRester
import py3Dmol
from pymatgen.io.cif import CifWriter
from pymatgen.core import Structure
from pymatgen.core import Composition
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.local_env import CrystalNN

#making a class
class CrystalStructure:

    def __init__(self):
        self.API_KEY = "ihddElrSgFw4L4DlUUb4VkH1px5SYhS0"

    #making a file to pymatgen structure class
    def file_to_structure(self,data):
        structure = Structure.from_str(data,fmt="cif")
        sga = SpacegroupAnalyzer(structure)
        return structure,sga

    #checking if the mp id is correct
    def is_valid_mp_id(self,id):
        if id[:2] != "mp":
            return False
        if id[2] != "-":
            return False
        if not id[3:].isdigit():
            return False
        return True

    #making a pymatgen structure class from mp-id
    def mp_id_to_structure(self,id):
        with MPRester(self.API_KEY) as mpr:
            structure = mpr.get_structure_by_material_id(id)
        sga = SpacegroupAnalyzer(structure)
        return structure,sga

    #checking if chemical formula is correct
    def is_valid_formula(self,data):
        try:
            comp = Composition(data)
            return True
        except:
            return False
    
    #making pymatgen structure class from formula
    def formula_to_structure(self,data):
        with MPRester(self.API_KEY) as mpr:
            docs = mpr.materials.summary.search(
                formula = data
            )
        best = min(
            docs,
            key = lambda x: x.energy_above_hull
        )
        structure = best.structure
        sga = SpacegroupAnalyzer(structure)
        return structure,sga
    
    #creating a 3d model using py3dmol
    def creating_3d_model(self,data):
        cif_str = str(CifWriter(data))
        view = py3Dmol.view(width=800,height=600)
        view.addModel(cif_str,"cif")
        view.addStyle(
            {},
            {
                "sphere":{"radius":0.4},
                "stick":{"radius":0.12}
            }
        )
        view.zoomTo()
        return view
    
    #function for getting formula
    def get_formula(self,structure):
        return structure.composition.reduced_formula
    
    #collecting lattice parameters and making a dataframe with it
    def get_lattice_parameters(self,structure):
        lattice = structure.lattice
        lat_data = {
            "Parameter" : [
                "a","b","c",
                "alpha","beta","gamma"
            ],
            "Value" :[
                lattice.a,
                lattice.b,
                lattice.c,
                lattice.alpha,
                lattice.beta,
                lattice.gamma,
            ]
        }
        df = pd.DataFrame(lat_data)
        return df
    
    #function for getting volume
    def get_volume(self,structure):
        return structure.volume
    
    #function for getting density
    def get_density(self,structure):
        return structure.density
    
    #function for getting number of sites
    def get_no_of_sites(self,structure):
        return structure.num_sites
    
    ##function for getting information about space group
    def get_space_group(self,sga):
        return sga.get_space_group_symbol(),sga.get_space_group_number()
    
    #function for getting crystal system
    def get_crystal_system(self,sga):
        return sga.get_crystal_system()
    
    #function for getting lattice system
    def get_lattice_system(self,sga):
        return sga.get_lattice_type()
    
    #function for getting number of coordinate
    def get_co(self,structure):
        cnn = CrystalNN()
        return cnn.get_cn(structure,0)
    
    

