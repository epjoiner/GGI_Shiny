# Load R packages

library(tidyverse)
library(shiny)

# Load local library

invisible(lapply(list.files("lib", full.names = TRUE), source))

# Load data

data <- read_ggi_data("data")

ui <- fluidPage(
    
    titlePanel("test"),

    mainPanel(
        verbatimTextOutput("tibble")
    )

)

server <- function(input, output) {

    output$tibble <- renderPrint(data)

}

shinyApp(ui = ui, server = server)
