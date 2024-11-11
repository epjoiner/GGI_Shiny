library(shiny)

# Source library functions

invisible(lapply(list.files("lib", full.names = TRUE), source))

# Write secondary aluminum data to directory

write_2nd_alum("2nd-aluminum/data")

# Run shiny app(s)

#runApp("coal")
#runApp("produced-oil")
runApp("2nd-aluminum")
