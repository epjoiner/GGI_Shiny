library(shiny)
library(bslib)
library(tidyverse)
library(ggplot2)

coal_ggi <- data.frame(Rank = c("Bituminous", "Sub-bituminous",
                                "Lignite", "Anthracite"),
                       Carbon_Frac = c(0.7, 0.5, 0.41, 0.78)) %>%
            mutate(Carbon_Cont = Carbon_Frac * (44/12))
                        



# Define UI
ui <- fluidPage(
# App title ----
title = "Coal App",
# Sidebar panel for inputs ----
sidebarPanel(
numericInput(
    "sco_b",
    "SC and Operations - Bituminous",
    value = 1,
    min = 0,
    max = 1
  ),

numericInput(
    "sco_sb",
    "SC and Operations - Sub-Bituminous",
    value = 1,
    min = 0,
    max = 1
  ),
  numericInput(
    "sco_l",
    "SC and Operations - Lignite",
    value = 1,
    min = 0,
    max = 1
  ),
  numericInput(
    "sco_a",
    "SC and Operations - Anthracite",
    value = 1,
    min = 0,
    max = 1
  )),
  # Output: Histogram --
  card(plotOutput(outputId = "distPlot"))

)

server <- function(input, output) {


  output$distPlot <- renderPlot({

    coal_ggi <- coal_ggi %>% mutate(SC_OPs = c(input$sco_b, input$sco_sb, input$sbo_l, input$sbo_a)) %>%
                            gather(., Source, Amount, Carbon_Cont:SC_OPs, factor_key = T)

    ggplot(data = coal_ggi, aes(x = Rank, y = Amount, fill = Source)) +  
    geom_bar(position = "stack", stat="identity")  

    })

}

shinyApp(ui = ui, server = server)
