"""Generates an input file for transitioning from EG01 -> EG23"""
from __future__ import unicode_literals, print_function
from math import ceil

try:
    import simplejson as json
except ImportError:
    import json

# temporary hack using Bo Feng's reactor deployment schedule from DYMOND
bo_deployment = {'LWR': [0, 100, 0, 0, 0,  # expanding the timeline by five years at the beginning to match Bo's start time
        0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 
        1, 1, 1, 6, 6, 7, 6, 6, 6, 6, 7, 6, 6, 2, 1, 1, 1, 2, 1, 1, 2, 1, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 4, 3, 2, 
        0, 3, 3, 4, 3, 1, 1, 2, 8, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0],
    'FR': [0, 0, 0, 0, 0,  # same thing
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 1.6, 1.6, 1.2, 1.6, 1.6, 1.2, 1.6, 1.6, 1.2, 1.6, 1.6, 6.8, 6.4, 
        6.8, 6.4, 6.8, 6.4, 6.8, 6.8, 6.4, 5.2, 0, 0, 0, 1.6, 2, 1.6, 2, 1.6, 
        2, 2, 2, 1.6, 2, 2, 2, 2, 2, 2, 2.4, 2, 2, 2, 2.4, 2, 2.4, 3.2, 3.2, 0, 
        0, 0, 0, 1.6, 3.2, 0.4, 0.4, 0.8, 0.4, 2, 3.2, 0.8, 0.8, 3.6, 9.6, 8.8, 
        8.8, 8.4, 8.8, 10, 8.8, 8.8, 4.8, 3.6, 4, 4, 4.8, 4, 4, 5.2, 4, 4.8, 
        4.8, 4.4, 4.8, 4.8, 4.4, 4.8, 5.2, 4.4, 5.2, 4.8, 10.4, 10, 10, 10, 
        10.4, 10.4, 10.4, 10.4, 10, 11.2, 4.8, 6, 5.6, 5.6, 6, 5.6, 6.4, 5.6, 
        6, 6.4, 6, 6, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 7.2, 6.4, 6.8, 6.8, 7.2, 
        6.8, 7.2, 8, 8.4, 8, 8, 9.2, 8, 8.8, 8.4, 8.8, 8.8, 10.4, 8.8, 8.4, 10, 
        8.4, 14.4, 14.4, 15.2, 14.8, 14.8, 14.4, 14.8, 16, 15.2, 14.8, 11.2, 
        10, 10.4, 10.4, 11.6, 10.4, 10.8, 12, 10.8, 11.6]}

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
    #"control": {"duration": 12 * 185, "startmonth": 1, "startyear": 2015}, 
    "control": {"duration": 12 * 20, "startmonth": 1, "startyear": 2005}, 
    "facility": [
        {"name": "FR Fuel Fab",
         "config": {"FuelfabFacility": {
            "fissle_stream": "LWR Reprocessed", 
            "in_commods": {"key": "FR Reprocessed", "val": 0.0}, 
            "maximum_storage": 1e60, 
            "non_fissle_stream": "DU2", 
            "out_commod": "FR Fuel"
            }},}, 
        {"name": "MineU235",
         "config": {"Source": {"capacity": 4000, "commod": "U235", 
                               "recipe_name": "U235"}},}, 
        {"name": "U238", 
         "config": {"Source": {"capacity": 20000, "commod": "U238", 
                               "recipe_name": "Uranium 238"}},}, 
        {"name": "DU",
         "config": {"Source": {"capacity": 20000, "commod": "DU", 
                               "recipe_name": "DU"}},}, 
        {"name": "DU2",
         "config": {"Source": {"capacity": 20000, "commod": "DU2", 
                               "recipe_name": "DU"}},}, 
        {"name": "LWR Fuel FAb",
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
            "input_capacity": 2000, 
            "max_inv_size": 1e299, 
            "output_capacity": 2000, 
            "repro_input_path": "hist/FR_reprocess.txt"
            }},}, 
        {"name": "LWR",
         "config": {"ReactorFacility": {
            "DA_mode": 0, 
            "batches": 3, 
            "burnupcalc_timestep": 10, 
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
            "reactor_life": 480, 
            "target_burnup": 45, 
            "tolerence": 0.0010, 
            "trans_created": {"val": ["922350", "942380", "942390", "942400", 
                                      "942410", "942420"]}, 
            "trans_fission": {"val": ["922350", "942380", "942390", "942400", 
                                      "942410", "942420"]}
            }},}, 
   {
    "config": {
     "ReactorFacility": {
      "DA_mode": "0", 
      "batches": "5", 
      "burnupcalc_timestep": "10", 
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
      "generated_power": "1000.0", 
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
      "reactor_life": "960", 
      "target_burnup": "200", 
      "tolerence": "0.0010", 
      "trans_created": {"val": ["922350", "942380", "942390", "942400", "942410", "942420"]}, 
      "trans_fission": {"val": ["922350", "942380", "942390", "942400", "942410", "942420"]}
     }
    }, 
    "name": "FR"
   }, 
   {
    "config": {
     "ReprocessFacility": {
      "commod_out": {"val": ["FR Reprocessed", "WASTE"]}, 
      "in_commod": {"val": "FR Spent Fuel"}, 
      "input_capacity": "2000", 
      "max_inv_size": "1.000000000000000E+299", 
      "output_capacity": "2000", 
      "repro_input_path": "hist/FR_reprocess.txt"
     }
    }, 
    "name": "FR Reprocess"
   }, 
   {
    "config": {
     "Sink": {
      "capacity": "100000", 
      "in_commods": {"val": "WASTE"}, 
      "max_inv_size": "1.000000000000000E+299"
     }
    }, 
    "name": "SINK"
   }
  ], 
  "recipe": [
   {
    "basis": "mass", 
    "name": "Uranium 238", 
    "nuclide": {"comp": "100.0000002", "id": "922380"}
   }, 
   {
    "basis": "mass", 
    "name": "U235", 
    "nuclide": {"comp": "100.0000002", "id": "922350"}
   }, 
   {
    "basis": "mass", 
    "name": "DU", 
    "nuclide": [{"comp": "0.2500002", "id": "922350"}, {"comp": "99.7500002", "id": "922380"}]
   }
  ], 
  "region": {
   "name": "USA",
   "config": {"NullRegion": None}, 
   "institution": [
    {
     "name": "utility",
     "config": {"NullInst": None}, 
     "initialfacilitylist": {
      "entry": [
       {"number": 1, "prototype": "MineU235"}, 
       {"number": 1, "prototype": "U238"}, 
       {"number": 1, "prototype": "DU"}, 
       {"number": 1, "prototype": "DU2"}, 
       {"number": 1, "prototype": "LWR Fuel FAb"}, 
       {"number": 1, "prototype": "LWR Seperation"}, 
       {"number": 1, "prototype": "FR Reprocess"}, 
       {"number": 1, "prototype": "SINK"}, 
       {"number": 1, "prototype": "FR Fuel Fab"}
      ]
     }, 
    }, 
    {
     "name": "utility2",
     "config": {
      "DeployInst": {"buildorder": [
            "<prototype>LWR</prototype><number>2</number><date>5</date>",
            "<prototype>FR</prototype><number>1</number><date>10</date>",
            ]
        },
     }, 
    }
   ], 
  }
}}

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
