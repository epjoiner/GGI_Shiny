# Load R packages

library(shiny)
library(dplyr)
library(forcats)
library(plotly)
library(bslib)

# User interface

ui <- page_fillable(
  
  layout_sidebar(
    
    sidebar = sidebar(
      accordion(
        accordion_panel(
          title = "Electrolysis Parameters",
          sliderInput(
            "electrolysis_elec_in", 
            "Electrolysis: MWh per tonne Al", 
            min = 0, max = 20, value = 16, step = 0.1
          )
        ),
        accordion_panel(
          title = "Anode Parameters",
          sliderInput(
            "anode_raw_mat_ggi", 
            "Anode: Raw materials, tonne CO2e per tonne anode", 
            min = 0, max = 5, value = 3.44, step = 0.01
          ),
          sliderInput(
            "anode", 
            "Anode: Tonnes per tonne Aluminum", 
            min = 0, max = 1, value = 0.45, step = 0.01
          ),
          sliderInput(
            "anode_elec", 
            "Anode Electricity: MWh per tonne Anode", 
            min = 0, max = 1, value = 0.1242, step = 0.001
          ),
          sliderInput(
            "anode_thermal", 
            "Anode Thermal Energy: MBtu per tonne Anode", 
            min = 0, max = 10, value = 3.398, step = 0.1
          ),
          sliderInput(
            "anode_effect_pfcs_ggi", 
            "Anode Effect PFCs GGI", 
            min = 0, max = 1, value = 0.16, step = 0.01
          )
        ),
        accordion_panel(
          title = "Alumina Parameters",
          sliderInput(
            "alumina", 
            "Alumina: Tonnes per tonne Aluminum", 
            min = 0, max = 5, value = 1.93, step = 0.01
          ),
          sliderInput(
            "alumina_bauxite", 
            "Alumina Bauxite: Tonnes per tonne Alumina", 
            min = 0, max = 10, value = 3, step = 0.1
          ),
          sliderInput(
            "alumina_elec", 
            "Alumina Electricity: MWh per tonne Alumina", 
            min = 0, max = 5, value = 0.622, step = 0.01
          ),
          sliderInput(
            "alumina_thermal", 
            "Alumina Thermal Energy: MBtu per tonne Alumina", 
            min = 0, max = 10, value = 3.89, step = 0.1
          )
        ),
        accordion_panel(
          title = "Bauxite Parameters",
          sliderInput(
            "bauxite_elec", 
            "Bauxite Electricity: MWh per tonne Bauxite", 
            min = 0, max = 0.01, value = 0.005, step = 0.0001
          ),
          sliderInput(
            "bauxite_thermal_energy", 
            "Bauxite Thermal Energy: Tonnes Fuel Oil per tonne Bauxite", 
            min = 0, max = 0.01, value = 0.0015, step = 0.0001
          ),
          sliderInput(
            "bauxite_fuel_oil_ggi", 
            "Bauxite Fuel Oil GGI: Tonnes CO2e per tonne Fuel Oil", 
            min = 0, max = 10, value = 3.82, step = 0.1
          )
        )
      )
    ),
    
    fillPage(plotlyOutput("waterfall", height = "90%"))
    
  )
)

# Server

server <- function(input, output) {
  
  # Load local library
  invisible(lapply(list.files("lib", full.names = TRUE), source))
  
  # Load data
  data <- read_ggi_data("data")
  
  output$waterfall <- renderPlotly({
    
    values <- aluminum(
      input_data = data, 
      alumina = input$alumina,
      anode = input$anode,
      electrolysis_elec = input$electrolysis_elec_in,
      anode_raw_materials_ggi = input$anode_raw_mat_ggi,
      anode_elec = input$anode_elec,
      anode_thermal = input$anode_thermal,
      anode_effect_pfcs_ggi = input$anode_effect_pfcs_ggi,
      alumina_bauxite = input$alumina_bauxite,
      alumina_elec = input$alumina_elec,
      alumina_thermal = input$alumina_thermal,
      bauxite_elec = input$bauxite_elec,
      bauxite_thermal_energy = input$bauxite_thermal_energy,
      bauxite_fuel_oil_ggi = input$bauxite_fuel_oil_ggi
    )
    
    ggi_table <- tibble(x = names(values), y = round(unlist(values), 3)) %>%
      filter(!x %in% c("total", "secondary")) %>% # Just primary for now
      mutate(
        measure = if_else(x == "primary", "total", "relative"),
        x = fct_reorder(x, y)
      ) %>%
      arrange(y)
    
    plot_ly(
      ggi_table, name = "GGI", type = "waterfall", measure = ~measure,
      x = ~x, textposition = "auto", y = ~y, text = ~as.character(y),
      connector = list(line = list(color = "rgb(63, 63, 63)"))
    ) %>%
      layout(
        title = "",
        xaxis = list(title = ""),
        yaxis = list(
          title = "tonnes of CO2e per tonne Al", 
          range = c(0, max(20, max(ggi_table$y)))
        ),
        autosize = TRUE,
        showlegend = FALSE
      )
  })
  
}

# App

shinyApp(ui = ui, server = server)
