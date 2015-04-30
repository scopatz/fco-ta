"""Generates an input file for transitioning from EG01 -> EG23"""
from __future__ import unicode_literals, print_function

from math import ceil

try:
    import simplejson as json
except ImportError:
    import json

# temporary hack using Bo Feng's reactor deployment schedule from DYMOND, 
# assuming deployment of 100 LWRs between 1965 and 2015, at 2 reactors/year
bo_deployment = {'LWR': [0,            # 1964
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 1965 - 1974
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 1975 - 1984
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 1985 - 1994
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 1995 - 2004
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  # 2005 - 2014
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 2015 - 2024
        2, 1, 1, 1, 1, 6, 6, 7, 6, 6,  # 2025 - 2034
        6, 6, 7, 6, 6, 2, 1, 1, 1, 2,  # 2035 - 2044
        1, 1, 2, 1, 0, 0, 0, 0, 0, 0,  # 2045 - 2054
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2055 - 2064
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2065 - 2074
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2075 - 2084
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2085 - 2094
        0, 0, 0, 3, 4, 3, 3, 2, 0, 3,  # 2095 - 2104
        4, 3, 3, 1, 0, 5, 0, 0, 0, 0,  # 2105 - 2114
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2115 - 2124
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2125 - 2134
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2135 - 2144
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2145 - 2154
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2155 - 2164
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2165 - 2174
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2175 - 2184
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2185 - 2194
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2195 - 2204
        0, 0, 0, 0, 0, 0,              # 2205 - 2210
        ],
    'FR': [0,                          # 1964
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1965 - 1974
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1975 - 1984
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1985 - 1994
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 1995 - 2004
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 2005 - 2014
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # 2015 - 2024
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # 2025 - 2034
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # 2035 - 2044
        0.0, 0.0, 0.0, 0.0, 1.6, 1.6, 1.2, 1.6, 1.6, 1.2,  # 2045 - 2054
        1.6, 1.6, 1.2, 1.6, 1.6, 6.8, 6.4, 6.8, 6.4, 6.8,  # 2055 - 2064
        6.4, 6.8, 6.8, 6.4, 6.8, 1.6, 2.0, 1.6, 2.0, 1.6,  # 2065 - 2074
        2.0, 1.6, 2.0, 2.0, 1.6, 2.0, 2.0, 2.0, 2.0, 2.0,  # 2075 - 2084
        2.0, 2.0, 2.0, 2.0, 2.0, 2.4, 2.0, 2.0, 2.4, 2.0,  # 2085 - 2094
        3.2, 3.2, 3.2, 0.0, 0.0, 0.0, 0.0, 2.0, 3.2, 0.4,  # 2095 - 2104
        0.8, 0.4, 0.8, 1.6, 3.6, 4.0, 8.4, 9.6, 8.8, 8.8,  # 2105 - 2114
        8.4, 8.8, 10.0, 8.8, 8.8, 4.8, 3.6, 4.0, 4.0, 4.8, # 2115 - 2124
        4.0, 4.0, 5.2, 4.0, 4.8, 4.8, 4.4, 4.8, 4.8, 4.4,  # 2125 - 2134
        4.8, 5.2, 4.4, 5.2, 4.8, 10.4, 10.0, 10.0, 10.0, 10.4,  # 2135 - 2144
        10.4, 10.4, 10.4, 10.0, 10.8, 5.2, 6.0, 5.6, 6.0, 5.6,  # 2145 - 2154
        6.0, 5.6, 6.0, 6.4, 5.6, 6.4, 6.0, 6.4, 6.4, 6.4,  # 2155 - 2164
        6.4, 6.4, 6.8, 6.4, 6.8, 7.2, 6.4, 6.8, 7.2, 6.8,  # 2165 - 2174
        8.4, 8.0, 8.4, 8.0, 9.2, 8.0, 8.4, 9.2, 8.4, 8.8,  # 2175 - 2184
        10.4, 8.8, 9.2, 8.4, 9.2, 14.4, 14.4, 15.2, 14.8, 14.8,  # 2185 - 2194
        14.4, 14.8, 16.0, 15.2, 14.8, 11.2, 10.0, 10.4, 10.4, 11.6, # 2195 - 2204
        10.4, 10.8, 12.0, 10.8, 11.6, 12.0,  # 2205 - 2210
        ]
    }

BASE_SIM = {"simulation": {
    "archetypes": {
        "spec": [
            {"lib": "Brightlite", "name": "FuelfabFacility"}, 
            {"lib": "agents", "name": "Source"}, 
            {"lib": "agents", "name": "Source"}, 
            {"lib": "Brightlite", "name": "FuelfabFacility"}, 
            {"lib": "Brightlite", "name": "ReprocessFacility"}, 
            {"lib": "Brightlite", "name": "ReactorFacility"}, 
            {"lib": "Brightlite", "name": "ReactorFacility"}, 
            {"lib": "Brightlite", "name": "ReprocessFacility"}, 
            {"lib": "agents", "name": "Sink"}, 
            {"lib": "agents", "name": "NullRegion"}, 
            {"lib": "agents", "name": "NullInst"}, 
            {"lib": "cycamore", "name": "DeployInst"}
            ]
        }, 
    "commodity": [
        {"name": "LWR Fuel Fab", "solution_priority": 1.0}, 
        {"name": "LWR Spent Fuel", "solution_priority": 1.0}, 
        {"name": "FR Spent Fuel", "solution_priority": 1.0}, 
        {"name": "FR Fuel", "solution_priority": 1.0}, 
        {"name": "DU", "solution_priority": 1.0}, 
        {"name": "LWR Reprocessed", "solution_priority": 1.0}, 
        {"name": "FR Reprocessed", "solution_priority": 1.0}, 
        {"name": "U235", "solution_priority": 1.0}, 
        {"name": "U238", "solution_priority": 1.0}, 
        {"name": "FR Fuel", "solution_priority": 1.0}, 
        {"name": "WASTE", "solution_priority": 1.0}
        ], 
    #"control": {"duration": 12 * 251, "startmonth": 1, "startyear": 1964}, 
    "control": {"duration": 12 * 151, "startmonth": 1, "startyear": 1964}, 
    "facility": [
        {"name": "FR Fuel Fab",
         "config": {"FuelfabFacility": {
            "fissle_stream": "LWR Reprocessed", 
            #"in_commods": {"key": "FR Reprocessed", "val": 0.05}, 
            "in_commods": {"key": "FR Reprocessed", "val": 0.0}, 
            "maximum_storage": 1e60, 
            "non_fissle_stream": "DU2", 
            "out_commod": "FR Fuel"
            }},}, 
        {"name": "MineU235",
         "config": {"Source": {"capacity": 4000000, "commod": "U235", 
                               "recipe_name": "U235"}},}, 
        {"name": "U238", 
         "config": {"Source": {"capacity": 2000000, "commod": "U238", 
                               "recipe_name": "Uranium 238"}},}, 
        {"name": "DU",
         "config": {"Source": {"capacity": 2000000, "commod": "DU", 
                               "recipe_name": "DU"}},}, 
        {"name": "DU2",
         "config": {"Source": {"capacity": 2000000, "commod": "DU2", 
                               "recipe_name": "DU"}},}, 
        {"name": "LWR Fuel Fab",
         "config": {"FuelfabFacility": {
            "fissle_stream": "U235", 
            "in_commods": {"key": "DU", "val": 0.0}, 
            "maximum_storage": 1e60, 
            "non_fissle_stream": "U238", 
            "out_commod": "LWR Fuel",
            }},}, 
        {"name": "LWR Seperation",
         "config": {"ReprocessFacility": {
            "commod_out": {"val": ["LWR Reprocessed", "WASTE"]}, 
            "in_commod": {"val": "LWR Spent Fuel"}, 
            "input_capacity": 2000000, 
            "max_inv_size": 1e299, 
            "output_capacity": 2000000, 
            "repro_input_path": "hist/FR_reprocess.txt"
            }},}, 
        {"name": "LWR",
         "lifetime": 12*80,   
         "config": {"ReactorFacility": {
            "DA_mode": 0, 
            "batches": 3, 
            "burnupcalc_timestep": 200, 
            "core_mass": 1000, 
            "cylindrical_delta": 5, 
            "disadv_a": 0.40950, 
            "disadv_b": 0.707490, 
            "disadv_fuel_sigs": 0.430, 
            "disadv_mod_siga": 0.2220, 
            "disadv_mod_sigs": 3.440, 
            "efficiency": 0.330, 
            "flux_mode": 1, 
            "fuel_Sig_tr": 3.940, 
            "fuel_area": "89197", 
            "generated_power": 1000.0, 
            "in_commods": {"val": "LWR Fuel"}, 
            "interpol_pairs": {"key": "BURNUP", "val": 42}, 
            "libraries": {"val": "extLWR"}, 
            "max_inv_size": 1e299, 
            "mod_Sig_a": 0.02220, 
            "mod_Sig_f": 0.0, 
            "mod_Sig_tr": 3.460, 
            "mod_thickness": 100, 
            "nonleakage": 0.980, 
            "out_commod": "LWR Spent Fuel", 
            "reactor_life": 960, 
            "target_burnup": 45, 
            "tolerance": 0.0010, #gaaaah spelling
            "CR_fissile": {"val": ["922350", "942380", "942390", "942400", 
                                   "942410", "942420"]}, 
            }},}, 
        {"name": "FR",
         "lifetime": 12*80,       
         "config": {"ReactorFacility": {
            "DA_mode": 0, 
            "batches": 5, 
            "burnupcalc_timestep": 200, 
            "core_mass": "10", 
            "cylindrical_delta": "5", 
            "disadv_a": "0.40950", 
            "disadv_b": "0.707490", 
            "disadv_fuel_sigs": "0.430", 
            "disadv_mod_siga": "0.2220", 
            "disadv_mod_sigs": "3.440", 
            "efficiency": "0.330", 
            "flux_mode": "1", 
            "fuel_Sig_tr": "3.940", 
            "fuel_area": "89197", 
            "generated_power": "400.0", 
            "in_commods": {"val": "FR Fuel"}, 
            "interpol_pairs": {"key": "BURNUP", "val": "42"}, 
            "libraries": {"val": "FR50"}, 
            "max_inv_size": "1.000000000000000E+299", 
            "mod_Sig_a": "0.02220", 
            "mod_Sig_f": "0.0", 
            "mod_Sig_tr": "3.460", 
            "mod_thickness": "100", 
            "nonleakage": "0.57", 
            "out_commod": "FR Spent Fuel", 
            "reactor_life": 960, 
            "target_burnup": 200, 
            "tolerance": "0.0010", #can I correct this already? 
            "CR_fissile": {"val": ["922350", "942380", "942390", "942400", 
                                   "942410", "942420"]}, 
            }},}, 
        {"name": "FR Reprocess",
         "config": {"ReprocessFacility": {
            "commod_out": {"val": ["FR Reprocessed", "WASTE"]}, 
            "in_commod": {"val": "FR Spent Fuel"}, 
            "input_capacity": 2000000, 
            "max_inv_size": 1.0E+299, 
            "output_capacity": 200000, 
            "repro_input_path": "hist/FR_reprocess.txt"
            }},}, 
        {"name": "SINK",
         "config": {"Sink": {
            "capacity": 10000000, 
            "in_commods": {"val": "WASTE"}, 
            "max_inv_size": "1.000000000000000E+299"
            }},}
        ], 
    "recipe": [
        {"name": "Uranium 238", 
         "basis": "mass",
         "nuclide": {"comp": 100.0, "id": "922380"}
         }, 
        {"name": "U235", 
         "basis": "mass", 
         "nuclide": {"comp": 100.0, "id": "922350"}
         }, 
        {"name": "DU", 
         "basis": "mass", 
         "nuclide": [{"comp": 0.25, "id": "922350"}, 
                     {"comp": 99.75, "id": "922380"}]
         }
        ], 
    "region": {
        "name": "USA",
        "config": {"NullRegion": None}, 
        "institution": [
            {"name": "utility",
             "config": {"NullInst": None}, 
             "initialfacilitylist": {"entry": [
                {"number": 1, "prototype": "MineU235"}, 
                {"number": 1, "prototype": "U238"}, 
                {"number": 1, "prototype": "DU"}, 
                {"number": 1, "prototype": "DU2"}, 
                {"number": 1, "prototype": "LWR Fuel Fab"}, 
                {"number": 1, "prototype": "LWR Seperation"}, 
                {"number": 1, "prototype": "FR Reprocess"}, 
                {"number": 1, "prototype": "SINK"}, 
                {"number": 1, "prototype": "FR Fuel Fab"}
                ]}, 
             }, 
            {"name": "utility2",
             "config": {"DeployInst": {"buildorder": [
                "<prototype>LWR</prototype><number>2</number><date>5</date>",
                "<prototype>FR</prototype><number>1</number><date>10</date>",
                ]},}, 
             }
            ], 
        }
    }
}

def make_simulation():
    build_sched = []
    lwr_xml = "<prototype>LWR</prototype><number>{0}</number><date>{1}</date>"
    for i, n in enumerate(bo_deployment['LWR']):
        if n == 0:
            continue
        build_sched.append(lwr_xml.format(n, i*12))
    fr_xml = "<prototype>FR</prototype><number>{0}</number><date>{1}</date>"
    for i, n in enumerate(bo_deployment['FR']):
        if n == 0:
            continue
        build_sched.append(fr_xml.format(int(ceil(n)), i*12))
     
    BASE_SIM["simulation"]["region"]["institution"][1]["config"]["DeployInst"]["buildorder"] = build_sched
    return BASE_SIM    


def main():
    sim = make_simulation()
    with open('eg01-eg23.json', 'w') as f:
        json.dump(sim, f, sort_keys=True, indent=1, separators=(', ', ': '))

if __name__ == '__main__':
    main()
