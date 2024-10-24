library(shiny)
library(bslib)
library(tidyverse)
library(ggplot2)

coal_ggi <- data.frame(Rank = c("Bituminous", "Sub-bituminous",
                                "Lignite", "Anthracite"),
                       Carbon_Frac = c(0.7, 0.5, 0.41, 0.78)) %>%
            mutate(Carbon_Cont = Carbon_Frac * (44/12))
                        
colors_coal <- c("#ffc000","#7f7f7f")
names(colors_coal) <- c("SC_OPs", "Carbon_Cont")

# Define UI
ui <- fluidPage(
# App title ----
title = "Coal App",
titlePanel("Coal GGI Emissions by Rank (tCO2e / tCoal)"), 
# Sidebar panel for inputs ----
sidebarPanel(
  titlePanel("Supply Chain and Operations Emissions Input"), 
numericInput(
    "sco_b",
    "Bituminous",
    value = 0.117,
    min = 0,
    max = 5
  ),

numericInput(
    "sco_sb",
    "Sub-Bituminous",
    value = 0.020,
    min = 0,
    max = 5
  ),
  numericInput(
    "sco_l",
    "Lignite",
    value = 0.020,
    min = 0,
    max = 5
  ),
  numericInput(
    "sco_a",
    "Anthracite",
    value = 0.117,
    min = 0,
    max = 5
  )),
  # Output: Histogram --
  card(plotOutput(outputId = "distPlot"))

)

server <- function(input, output) {


  output$distPlot <- renderPlot({

    coal_ggi <- coal_ggi %>% mutate(SC_OPs = c(input$sco_b, input$sco_sb, input$sco_l, input$sco_a)) %>%
                            gather(., Source, Amount, Carbon_Cont:SC_OPs, factor_key = T) %>% group_by(Rank) %>% 
                            mutate(total_ggi = ifelse(Source == "SC_OPs", as.numeric(format(round(sum(Amount), 2), nsmall = 2)), ""), 
                                   Source = fct_relevel(Source, "SC_OPs", "Carbon_Cont")) 
    coal_ggi$Rank = factor(coal_ggi$Rank, levels = c("Bituminous", "Sub-bituminous", "Lignite", "Anthracite"), ordered = TRUE)

    ggplot(data = coal_ggi, aes(x = Rank, y = Amount, fill = Source)) +  
    geom_bar(position = "stack", stat="identity") + 
    scale_fill_manual(values = colors_coal, 
                      name = "Emissions Source",
                      labels = c("Supply Chain and Operations", "Coal Carbon Fraction")) +
    geom_text(aes(label = total_ggi), position= position_stack(0.9), vjust = -1)  + 
    labs(x = "Coal Rank", y = "GGI tCO2e / tCoal", title = "Coal GGI Emissions by Rank (tCO2e / tCoal)") + 
    theme_minimal()

    })

}

shinyApp(ui = ui, server = server)
