# Load R packages

library(tidyverse)
library(shiny)

# Load local library

invisible(lapply(list.files("lib", full.names = TRUE), source))

# Load data

data <- read_ggi_data("data")

ui <- fluidPage(
    
    titlePanel(p(
        h1("Aluminum Supply Chain"),
        h2("Greenhouse Gas Intensity"),
    )),

    mainPanel(
        plotOutput("columns",)
    )

)

server <- function(input, output) {

    values <- c(
        electrolysis(data),
        anode(data),
        alumina(data),
        aluminum(data)
    )

    output$columns <- renderPlot(plot(values))

}

shinyApp(ui = ui, server = server)
