# Total aluminum GGI function

aluminum <- function(

    input_data,                         # data from `read_ggi_data()`

    scrap_frac = 0,                     # Fraction of secondary aluminum used

    alumina = 1.93,                     # Tonnes of alumina per tonne aluminum
    anode = 0.45,                       # Tonnes of anode per tonne aluminum    

    secondary_elec = 0.1103,            # MWh per tonne aluminum 
    secondary_elec_source = "Coal",     # Gas, Oil, Coal, or Renewables
    secondary_thermal = 4.54,           # MBtu per tonne aluminum
    secondary_thermal_source = "Coal",  # Gas, Oil, Coal, or Renewables

    electrolysis_elec = 16,             # MWh per tonne aluminum 
    electrolysis_elec_source = "Coal",  # Gas, Oil, Coal, or Renewables

    anode_raw_materials_ggi = 3.444,    # anode raw materials (supply chain)
    anode_elec = 0.1242,                # MWh per tonne anode 
    anode_elec_source = "Coal",         # Gas, Oil, Coal, or Renewables
    anode_thermal = 3.398,              # MBtu per tonne anode
    anode_thermal_source = "Coal",      # Gas, Oil, Coal, or Renewables

    anode_effect_pfcs_ggi = 0.16,       # anode effect PFCs [?]

    alumina_bauxite = 3,                # tonnes bauxite per tonne alumina
    alumina_elec = 0.622,               # MWh per tonne alumina 
    alumina_elec_source = "Coal",       # Gas, Oil, Coal, or Renewables
    alumina_thermal = 3.89,             # MBtu per tonne alumina
    alumina_thermal_source = "Oil",     # Gas, Oil, Coal, or Renewables

    bauxite_elec = .005,                # MWh per tonne bauxite
    bauxite_elec_source = "Coal",       # Gas, Oil, Coal, or Renewables
    bauxite_thermal_energy = 0.0015,    # tonnes fuel oil per tonne bauxite
    bauxite_fuel_oil_ggi = 3.82         # tonnes CO2e per tonne fuel oil

) {

    secondary_ggi <- secondary_aluminum(
        input_data,
        secondary_elec,
        secondary_elec_source,
        secondary_thermal,
        secondary_thermal_source
    )

    electrolysis_ggi <- electrolysis(
        input_data,
        electrolysis_elec,
        electrolysis_elec_source
    )

    anode_ggi <- anode(
        input_data,
        anode_raw_materials_ggi,
        anode_elec,
        anode_elec_source,
        anode_thermal,
        anode_thermal_source
    )

    alumina_ggi <- alumina(
        input_data,
        bauxite(
            input_data,
            bauxite_elec,
            bauxite_elec_source,
            bauxite_thermal_energy,
            bauxite_fuel_oil_ggi
        ),
        alumina_bauxite,
        alumina_elec,
        alumina_elec_source,
        alumina_thermal,
        alumina_thermal_source
    )

    primary_ggi <- sum(
        electrolysis_ggi,
        anode * anode_ggi,
        anode_effect_pfcs_ggi,
        alumina * alumina_ggi
    )

    aluminum_ggi <- sum(
        primary_ggi * (1 - scrap_frac),
        secondary_ggi * scrap_frac
    )

    return(list(
        electrolysis = electrolysis_ggi,
        anode = anode * anode_ggi,
        anode_pfcs = anode_effect_pfcs_ggi,
        alumina = alumina * alumina_ggi,
        primary = primary_ggi,
        secondary = scrap_frac * secondary_ggi,
        total = aluminum_ggi
    ))

}


# Secondary aluminum GGI function

secondary_aluminum <- function(

    input_data,                         # data from `read_ggi_data()`
    electricity = 0.1103,               # MWh per tonne aluminum 
    electricity_source = "Coal",        # Gas, Oil, Coal, or Renewables
    thermal = 4.54,                     # MBtu per tonne aluminum
    thermal_source = "Coal"             # Gas, Oil, Coal, or Renewables

) {

    elec_ggi <- ggi_lookup(
        input_data,
        "electricity",
        electricity_source,
        "CO2e.MWh"
    )
    
    therm_ggi <- ggi_lookup(
        input_data,
        "thermal",
        thermal_source,
        "CO2e.MBtu"
    )

    secondary_aluminum_ggi <- c(
        electricity * elec_ggi,
        thermal * therm_ggi
    )

    return(sum(secondary_aluminum_ggi))

}


# Electrolysis GGI function

electrolysis <- function(

    input_data,                         # data from `read_ggi_data()`
    electricity = 16,                   # MWh per tonne aluminum 
    electricity_source = "Coal"         # Gas, Oil, Coal, or Renewables

) {

    electrolysis_ggi <- ggi_lookup(
        input_data,
        "electricity",
        electricity_source,
        "CO2.MWh"
    )

    return(electricity * electrolysis_ggi)

}


# Anode GGI function

anode <- function(

    input_data,                         # data from `read_ggi_data()`
    raw_materials_ggi = 3.444,          # anode raw materials (supply chain)
    electricity = 0.1242,               # MWh per tonne anode 
    electricity_source = "Coal",        # Gas, Oil, Coal, or Renewables
    thermal = 3.398,                    # MBtu per tonne anode
    thermal_source = "Coal"             # Gas, Oil, Coal, or Renewables

) {

    elec_ggi <- ggi_lookup(
        input_data,
        "electricity",
        electricity_source,
        "CO2e.MWh"
    )
    
    therm_ggi <- ggi_lookup(
        input_data,
        "thermal",
        thermal_source,
        "CO2e.MBtu"
    )

    anode_ggi <- c(
        raw_materials_ggi,
        electricity * elec_ggi,
        thermal * therm_ggi
    )

    return(sum(anode_ggi))

}


# Alumina GGI function

alumina <- function(

    input_data,                         # data from `read_ggi_data()`
    bauxite_ggi = 0.01098,              # tonnes CO2e per tonne bauxite
    bauxite = 3,                        # tonnes bauxite per tonne alumina
    electricity = 0.622,                # MWh per tonne alumina 
    electricity_source = "Coal",        # Gas, Oil, Coal, or Renewables
    thermal = 3.89,                     # MBtu per tonne alumina
    thermal_source = "Oil"              # Gas, Oil, Coal, or Renewables

) {

    elec_ggi <- ggi_lookup(
        input_data,
        "electricity",
        electricity_source,
        "CO2e.MWh"
    )
    
    therm_ggi <- ggi_lookup(
        input_data,
        "thermal",
        thermal_source,
        "CO2e.MBtu"
    )

    alumina_ggi <- c(
        bauxite * bauxite_ggi,
        electricity * elec_ggi,
        thermal * therm_ggi
    )

    return(sum(alumina_ggi))

}


# Bauxite GGI function

bauxite <- function(

    input_data,                         # data from `read_ggi_data()`
    electricity = .005,                 # MWh per tonne bauxite
    electricity_source = "Coal",        # Gas, Oil, Coal, or Renewables
    thermal_energy = 0.0015,            # tonnes fuel oil per tonne bauxite
    fuel_oil_ggi = 3.82                 # tonnes CO2e per tonne fuel oil

) {

    elec_ggi <- ggi_lookup(
        input_data,
        "electricity",
        electricity_source,
        "CO2e.MWh"
    )

    baux_ggi <- c(
        electricity * elec_ggi,
        thermal_energy * fuel_oil_ggi
    )

    return(sum(baux_ggi))

}

# Function to look up GGI values from input data

ggi_lookup <- function(
    
    input_data,                         # data from `read_ggi_data()`
    sheet = "thermal",                  # which table within data list
    source = "Coal",                    # Which row (source) within table
    units = "CO2e.MBtu"                 # Which column (units) within table

) {

    tbl <- input_data[[sheet]]
    return(tbl[tbl$Source == source, units])

}

