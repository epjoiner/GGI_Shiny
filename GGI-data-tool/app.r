library(shiny)
library(bslib)
library(tidyverse)

# Define UI for app that draws a histogram ----
ui <- page_sidebar(
  # App title ----
  title = "Produced Oil",
  # Sidebar panel for inputs ----
  sidebar = sidebar(
    # Input: Slider for the number of bins ----
    sliderInput(
      inputId = "proc_supp",
      label = "Process & Supply Chain Emission Intensity\n(tons CO2e per ton crude)",
      min = 0,
      max = 0.5,
      value = 0.126
    ),
    sliderInput(
      inputId = "carbon_frac",
      label = "Carbon Content\n(tons CO2e per ton crude)",
      min = 0,
      max = 1,
      value = 0.85
    )
  ),
  # Output: Bar chart ----
  plotOutput(outputId = "distPlot")
)

server <- function(input, output) {

  # Histogram of the Old Faithful Geyser Data ----
  # with requested number of bins
  # This expression that generates a histogram is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs (input$bins) change
  # 2. Its output type is a plot
  output$distPlot <- renderPlot({

    x    <- faithful$waiting/60
    bins <- seq(min(x), max(x), length.out = input$bins + 1)

    hist(x, breaks = bins, col = "#007bc2", border = "white",
         xlab = "Waiting time to next eruption (in hours)",
         main = "Histogram of waiting times")

    })

}

shinyApp(ui = ui, server = server)
