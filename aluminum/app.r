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
            sliderInput("electrolysis_elec_in", "Electrolysis: MWh per tonne Al", min = 0, max = 20, value = 16, step = 0.1),
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
            data, 
            electrolysis_elec = input$electrolysis_elec_in
        )

        ggi_table <- tibble(x = names(values), y = round(unlist(values),3)) %>%
            filter(!x %in% c("total", "secondary")) %>% # Just primary for now
            mutate(
                measure = if_else(x == "primary", "total", "relative"),
                x = fct_reorder(x, y)
            ) %>%
            arrange(y)

        plot_ly(
            ggi_table, name = "GGI", type = "waterfall", measure = ~measure,
            x = ~x, textposition = "auto", y= ~y, text = ~as.character(y),
            connector = list(line = list(color= "rgb(63, 63, 63)"))
        ) %>%
        layout(title = "",
                xaxis = list(title = ""),
                yaxis = list(title = "tonnes of CO2e per ton Al"),
                autosize = TRUE,
                showlegend = FALSE
        )
    })

}

# App

shinyApp(ui = ui, server = server)
