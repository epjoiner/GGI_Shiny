# Read CSV files from data directory

read_ggi_data <- function(datadir) {

    paths <- list.files(datadir, ".csv", full.names = TRUE)
    names <- list.files(datadir, ".csv", full.names = FALSE)
    tidy_names <- sapply(names, tools::file_path_sans_ext)

    output <- lapply(paths, read.csv)
    names(output) <- tidy_names

    return(output)

}
