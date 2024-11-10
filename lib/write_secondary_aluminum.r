# Making CSV files from dataframes of secondary aluminum data

write_2nd_alum <- function(datadir){

    # input static aluminum 
    second_aluminum_ggi <- data.frame(Source = c(rep("Primary", 5), rep("Scrap", 5), rep("Primary", 5), rep("Scrap", 5)), 
                                    Scrap_Amount = rep(c("0%", "25%", "50%", "75%", "100%"), 4),
                                    Scrap_Amount_num = rep(c(0, 0.25, .50, .75, 1), 4), 
                                    GGI_Amount = c(2.25, 1.68, 1.12, 0.56, 0, 0, 0.07, 0.13, 0.20, 0.26, 19.87, 14.90, 9.93, 4.97, 0.00, 0.00, 0.14, 0.28, 0.14, 0.56),
                                    Emissions_Scenario = c(rep("Low", 10), rep("High", 10)))

    second_aluminum_ggi_cus <- data.frame(Source = c(rep("Primary", 5), rep("Scrap", 5)),
                                        Scrap_Amount = rep(c("0%", "25%", "50%", "75%", "100%"), 2),
                                        Scrap_Amount_num = rep(c(0, 0.25, .50, .75, 1), 2),
                                        Emissions_Scenario =c(rep("Custom", 10))
                                        )

    write.csv(second_aluminum_ggi, file.path(datadir, "second_aluminum_ggi.csv"), row.names = FALSE)
    write.csv(second_aluminum_ggi_cus, file.path(datadir, "second_aluminum_ggi_cus.csv"), row.names = FALSE)

}
