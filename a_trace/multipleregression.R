# Set the working directory to the folder containing your CSV files and ROI activation file
setwd('C:/Users/victo/Google Drive/HDDM/3_parameter_trace/')
# Load required libraries
library(readr)
library(stats)
library(stringr)
library(tidyr)
library(ggplot2)
library(ggiraphExtra)
# loop through the csv files in the directory 
csv_files <- list.files(pattern = "_trace.csv$")
roi_data <- read.csv("roi_betas.csv")
# Loop through each CSV file
for (csv_file in csv_files) {
  data <- read.csv(csv_file, header = FALSE)
  stimuli <- c(rep("prototype", 1000), rep("rulefollowers", 1000), rep("exception", 1000))
  
  # Add the new column to the DataFrame
  data$type <- stimuli
  csv_title <- sub(".csv$", "", csv_file) 
  integers <- as.integer(unlist(str_extract_all(csv_title, "\\d+")))
  col <- paste("roi", integers, sep='')
  betas <- as.numeric(roi_data[[col]])
  
  betas <- c(betas, 'stimuli')
  colnames(data) <- betas
  
  proto_slopes <- numeric(1000)
  rulefollower_slopes <- numeric(1000)
  exception_slopes <- numeric(1000)
  x <- as.numeric(betas)
  
  proto_rf <- numeric(1000)
  rf_excep <- numeric(1000)
  proto_excep <- numeric(1000)
  
  
  for (i in 1:1000) {
    proto <- data[i, ]
    rulefollower <- data[1000 + i, ]
    exception <- data[2000 + i, ]
    proto = unlist(c(proto))
    rulefollower = unlist(c(rulefollower))
    exception = unlist(c(exception))
    
    reg_model1 = lm(proto ~ x) 
    proto_slopes[i] = reg_model1$coefficients[2]
   
    reg_model2= lm(rulefollower ~ x) 
    rulefollower_slopes[i] = reg_model2$coefficients[2]
    
    reg_model3= lm(exception ~ x) 
    exception_slopes[i] = reg_model3$coefficients[2]
    
    proto_rf[i] = proto_slopes[i] - rulefollower_slopes[i]
    rf_excep[i] = rulefollower_slopes[i] - exception_slopes[i]
    proto_excep[i] = proto_slopes[i] - exception_slopes[i]
    
  }

  df <- data.frame(
    proto_slopes = proto_slopes,
    rulefollower_slopes = rulefollower_slopes,
    exception_slopes = exception_slopes,
    proto_rf = proto_rf,
    rf_excep = rf_excep,
    proto_excep = proto_excep
  )
  file_path <- "slopes_diff.csv"
}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  # long_df <- pivot_longer(data, cols = -stimuli, names_to = "beta", values_to = "drift_rate")
  # long_df$beta <- as.numeric(long_df$beta)
  # model <- lm(drift_rate ~ beta * stimuli, data=long_df)
  # model_summary <- summary(model)
  # model_summary_text <- capture.output(print(model_summary))
  
#   p <- ggPredict(model, se=FALSE,interactive=FALSE, title='hello')
#   p <- plot(p) +
#     labs(
#       title = paste('drift rate value in', col)
#     )
#   ggsave(paste('drift rate in', col, '.png'), p, width = 6, height = 4)
#   file_path <- paste("linear_model_summary", col, ".txt")
#   writeLines(model_summary_text, con = file_path)




