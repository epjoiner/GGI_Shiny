library(shiny)
library(bslib)
library(ggplot2)

# Define UI for app ----
ui <- page_sidebar(
  # App title ----
  title = "Produced Oil",
  # Sidebar panel for inputs ----
  sidebar = sidebar(
    sliderInput(
      inputId = "carbon_frac_conv",
      label = "Conventional Oil Carbon Fraction",
      min = 0,
      max = 1,
      value = 0.85
    ),
    sliderInput(
      inputId = "carbon_frac_sand",
      label = "Canadian Oil Sands Carbon Fraction",
      min = 0,
      max = 1,
      value = 0.85
    ),
    selectInput(
      inputId = "proc_supp_conv",
      label = "Conventional Oil Process & Supply Chain Contribution",
      choices = list("3%" = .03, "5%" = .05, "8%" = .08)
    ),
    selectInput(
      inputId = "proc_supp_sand",
      label = "Canadian Oil Sands Process & Supply Chain Contribution",
      choices = list("10%" = .10, "15%" = .15, "20%" = .20)
    )
  ),
  # Output: Bar chart ----
  plotOutput(outputId = "barPlot")
)

server <- function(input, output) {

  co2_per_c <- 44 / 12

  # This expression that generates a column chart is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs change
  # 2. Its output type is a plot

  output$barPlot <- renderPlot({

    conv_cc <- co2_per_c * input$carbon_frac_conv
    sand_cc <- co2_per_c * input$carbon_frac_sand
    conv_ps <- conv_cc * as.numeric(input$proc_supp_conv)
    sand_ps <- sand_cc * as.numeric(input$proc_supp_sand)

    y <- c(conv_ps, sand_ps, conv_cc, sand_cc)
    x <- c("Conv", "Sand", "Conv", "Sand")
    categories <- c("Process & Supply Chain", "Carbon Content")
    col <- factor(
      rep(categories, each = 2),
      levels = categories
    )

    plot_data <- data.frame(y, x, col)

    ggplot(aes(x = x, y = y, fill = col), data = plot_data) +
      geom_col(position = "stack") +
      scale_y_continuous(limits = c(0, 4.5)) +
      theme(legend.position = "bottom") +
      labs(fill = "")

  })

}

shinyApp(ui = ui, server = server)
