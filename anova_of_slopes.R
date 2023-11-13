setwd('C:/Users/victo/Google Drive/HDDM/3_parameter_trace/v_trace/')
library(readr)
library(stats)
library(stringr)
library(tidyr)
library(ggplot2)
library(ggiraphExtra)


# Set the path to the folder
folder_path <- "C:/Users/victo/Google Drive/HDDM/3_parameter_trace/v_trace/"

# Get a list of files in the folder
file_list <- list.files(folder_path, pattern = "_slopes.csv", full.names = TRUE)

# Loop through the selected files
for (file in file_list) {
  # Extract 'ROI' followed by a number from the file name
  roi_match <- regmatches(file, regexpr("roi\\d+", file))
  
  # Check if a match is found, and store the ROI number in roi_number
  if (length(roi_match) > 0) {
    roi_number <- substr(roi_match, 4, nchar(roi_match))

    df <- read.csv(file, header = TRUE)
    df_stacked <- df %>%
      pivot_longer(cols = c(proto_rf,rf_excep,proto_excep), names_to = "Group", values_to = "Value")
    # print(df_stacked)
    model <- aov(Value ~ Group, data = df_stacked)
    anova_summary <- capture.output(summary(model))
    
    save_name <- paste("v_", roi_match, "_ANOVA.txt", sep = "")
    writeLines(anova_summary, save_name)
    
    # Perform Tukey's post hoc test
    tukey_result <- TukeyHSD(model)
    # Save Tukey's post hoc test results to a text file
    tukey_save_name <- paste("v_", roi_match, "_Tukey.txt", sep = "")
    writeLines(capture.output(tukey_result), tukey_save_name)
    
    # Create a violin plot
    violinplot <- ggplot(df_stacked, aes(x = Group, y = Value)) +
      geom_violin() +
      labs(title = "Violin Plot", x = "Group", y = "Value")
    ggsave(paste("violin_", roi_match, ".png", sep = ""), plot = violinplot)
    
    # Create a box plot
    boxplot <- ggplot(df_stacked, aes(x = Group, y = Value)) +
      geom_boxplot() +
      labs(title = "Box Plot", x = "Group", y = "Value")
    ggsave(paste("box_", roi_match, ".png", sep = ""), plot = boxplot)
  }
}
