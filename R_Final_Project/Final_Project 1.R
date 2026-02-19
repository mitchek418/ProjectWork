library(arrow)        # For reading parquet files
library(tidyverse)    # Data manipulation and visualization
library(lubridate)    # Date handling
library(caret)        # For train/test split
library(broom)        # For tidy model outputs
library(knitr)        # For nice tables
library(car)          # For ANOVA tests
library(MASS)         # For negative binomial regression (glm.nb)

# Load the parquet file
crime_data <- read_parquet("chicago_crime_seasonality_2015_2024.parquet")

# Filter to 2015-2024 (should already be filtered, but confirming)
crime_data <- crime_data %>%
  filter(Year >= 2015 & Year <= 2024)

# Display data structure
glimpse(crime_data)

# Convert day and month to categorical (factor) variables
crime_data <- crime_data %>%
  mutate(
    # Day of week as factor (1=Monday, 7=Sunday)
    day_factor = factor(day,
                        levels = 1:7,
                        labels = c("Monday", "Tuesday", "Wednesday",
                                   "Thursday", "Friday", "Saturday", "Sunday")),
    
    # Month as factor
    month_factor = factor(month,
                          levels = 1:12,
                          labels = c("January", "February", "March", "April",
                                     "May", "June", "July", "August",
                                     "September", "October", "November", "December")),
    
    # Weekend as factor
    weekend_factor = factor(weekend,
                            levels = c(0, 1),
                            labels = c("Weekday", "Weekend")),
    
    # Season already appears to be categorical, ensure it's a factor
    season = as.factor(season)
  )

# Check the conversions
summary(crime_data %>% dplyr::select(day_factor, month_factor, weekend_factor, season))

# Define crime categories based on Primary Type

# Non-violent crimes
non_violent_types <- c("THEFT", "ROBBERY", "NARCOTICS", "BURGLARY")

# Violent crimes
violent_types <- c("BATTERY", "ASSAULT", "CRIMINAL DAMAGE", "HOMICIDE")

# Special events
special_event_types <- c("ARSON", "GAMBLING", "OTHER OFFENSE")

# Human trafficking/sex crimes
human_trafficking_types <- c("CRIM SEXUAL ASSAULT", "DOMESTIC VIOLENCE",
                             "PROSTITUTION", "KIDNAPPING", "STALKING",
                             "PUBLIC INDECENCY", "CRIMINAL SEXUAL ASSAULT",
                             "SEX OFFENSE", "HUMAN TRAFFICKING")

# Add category column
crime_data <- crime_data %>%
  mutate(
    crime_category = case_when(
      `Primary Type` %in% non_violent_types ~ "Non-Violent",
      `Primary Type` %in% violent_types ~ "Violent",
      `Primary Type` %in% special_event_types ~ "Special Event",
      `Primary Type` %in% human_trafficking_types ~ "Human Trafficking/Sex",
      TRUE ~ "Other"
    )
  )

# Check distribution
table(crime_data$crime_category)

# Create a date column (extract just the date, not time)
crime_data <- crime_data %>%
  mutate(date_only = as.Date(datetime_parsed))

# Aggregate to daily counts by crime category
daily_counts <- crime_data %>%
  group_by(date_only, day_factor, month_factor, weekend_factor, season,
           marathon_event, special_event, lolla_event, river_event) %>%
  summarise(
    count_nonviolent = sum(crime_category == "Non-Violent"),
    count_violent = sum(crime_category == "Violent"),
    count_special = sum(crime_category == "Special Event"),
    count_trafficking = sum(crime_category == "Human Trafficking/Sex"),
    count_total = n(),
    .groups = "drop"
  )

# Display summary
summary(daily_counts)
head(daily_counts, 10)

# Plot total crimes over time
ggplot(daily_counts, aes(x = date_only, y = count_total)) +
  geom_line(alpha = 0.5) +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Total Daily Crime Counts (2015-2024)",
       x = "Date", y = "Daily Crime Count") +
  theme_minimal()

# Boxplot by day of week
daily_counts %>%
  pivot_longer(cols = starts_with("count_"),
               names_to = "crime_type",
               values_to = "count") %>%
  ggplot(aes(x = day_factor, y = count, fill = crime_type)) +
  geom_boxplot() +
  facet_wrap(~crime_type, scales = "free_y") +
  labs(title = "Crime Counts by Day of Week",
       x = "Day of Week", y = "Count") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "none")

# Boxplot by month
daily_counts %>%
  pivot_longer(cols = starts_with("count_"),
               names_to = "crime_type",
               values_to = "count") %>%
  ggplot(aes(x = month_factor, y = count, fill = crime_type)) +
  geom_boxplot() +
  facet_wrap(~crime_type, scales = "free_y") +
  labs(title = "Crime Counts by Month",
       x = "Month", y = "Count") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "none")

# Boxplot by season
daily_counts %>%
  pivot_longer(cols = starts_with("count_"),
               names_to = "crime_type",
               values_to = "count") %>%
  ggplot(aes(x = season, y = count, fill = crime_type)) +
  geom_boxplot() +
  facet_wrap(~crime_type, scales = "free_y") +
  labs(title = "Crime Counts by Season",
       x = "Season", y = "Count") +
  theme_minimal() +
  theme(legend.position = "none")

# Boxplot weekend vs weekday
daily_counts %>%
  pivot_longer(cols = starts_with("count_"),
               names_to = "crime_type",
               values_to = "count") %>%
  ggplot(aes(x = weekend_factor, y = count, fill = crime_type)) +
  geom_boxplot() +
  facet_wrap(~crime_type, scales = "free_y") +
  labs(title = "Crime Counts: Weekend vs Weekday",
       x = "", y = "Count") +
  theme_minimal() +
  theme(legend.position = "none")

set.seed(123)  # For reproducibility

# Create train/test split
train_index <- createDataPartition(daily_counts$count_total, p = 0.8, list = FALSE)
train_data <- daily_counts[train_index, ]
test_data <- daily_counts[-train_index, ]

# Check the split
cat("Training set size:", nrow(train_data), "\n")
cat("Test set size:", nrow(test_data), "\n")
cat("Training proportion:", nrow(train_data) / nrow(daily_counts), "\n")

# Negative binomial regression for non-violent crime counts
model_nonviolent <- glm.nb(count_nonviolent ~ day_factor + month_factor +
                            weekend_factor + season + marathon_event +
                            special_event + lolla_event + river_event,
                          data = train_data)

# Model summary
summary(model_nonviolent)

# Predictions on test set
pred_nonviolent <- predict(model_nonviolent, newdata = test_data, type = "response")
rmse_nonviolent <- sqrt(mean((test_data$count_nonviolent - pred_nonviolent)^2))
cat("\nRMSE for Non-Violent Crime Model:", rmse_nonviolent, "\n")
cat("AIC:", AIC(model_nonviolent), "\n")

# Negative binomial regression for violent crime counts
model_violent <- glm.nb(count_violent ~ day_factor + month_factor +
                         weekend_factor + season + marathon_event +
                         special_event + lolla_event + river_event,
                       data = train_data)

# Model summary
summary(model_violent)

# Predictions on test set
pred_violent <- predict(model_violent, newdata = test_data, type = "response")
rmse_violent <- sqrt(mean((test_data$count_violent - pred_violent)^2))
cat("\nRMSE for Violent Crime Model:", rmse_violent, "\n")
cat("AIC:", AIC(model_violent), "\n")

# Negative binomial regression for trafficking/sex crime counts
model_trafficking <- glm.nb(count_trafficking ~ day_factor + month_factor +
                             weekend_factor + season + marathon_event +
                             special_event + lolla_event + river_event,
                           data = train_data)

# Model summary
summary(model_trafficking)

# Predictions on test set
pred_trafficking <- predict(model_trafficking, newdata = test_data, type = "response")
rmse_trafficking <- sqrt(mean((test_data$count_trafficking - pred_trafficking)^2))
cat("\nRMSE for Trafficking/Sex Crime Model:", rmse_trafficking, "\n")
cat("AIC:", AIC(model_trafficking), "\n")

# Negative binomial regression for total crime counts
model_total <- glm.nb(count_total ~ day_factor + month_factor +
                       weekend_factor + season + marathon_event +
                       special_event + lolla_event + river_event,
                     data = train_data)

# Model summary
summary(model_total)

# Predictions on test set
pred_total <- predict(model_total, newdata = test_data, type = "response")
rmse_total <- sqrt(mean((test_data$count_total - pred_total)^2))
cat("\nRMSE for Total Crime Model:", rmse_total, "\n")
cat("AIC:", AIC(model_total), "\n")

# Create a summary table of model performance metrics
performance_summary <- data.frame(
  Model = c("Non-Violent Crime", "Violent Crime",
            "Trafficking/Sex Crime", "Total Crime"),
  RMSE = c(rmse_nonviolent, rmse_violent, rmse_trafficking, rmse_total),
  AIC = c(AIC(model_nonviolent), AIC(model_violent),
          AIC(model_trafficking), AIC(model_total)),
  Deviance = c(deviance(model_nonviolent), deviance(model_violent),
               deviance(model_trafficking), deviance(model_total)),
  Theta = c(model_nonviolent$theta, model_violent$theta,
            model_trafficking$theta, model_total$theta)
)

kable(performance_summary,
      caption = "Model Performance Metrics (Negative Binomial)",
      digits = 2)

# Goodness of fit for negative binomial model
cat("Deviance Goodness of Fit Test:\n")
cat("Residual Deviance:", deviance(model_total), "\n")
cat("Degrees of Freedom:", model_total$df.residual, "\n")
cat("Deviance / DF (should be close to 1):",
    deviance(model_total) / model_total$df.residual, "\n\n")

# Theta (dispersion parameter)
cat("Theta (dispersion parameter):", model_total$theta, "\n")
cat("Standard Error of Theta:", model_total$SE.theta, "\n\n")

# Residual plots
par(mfrow = c(2, 2))
plot(model_total)
par(mfrow = c(1, 1))

# Variance Inflation Factors
# Check for aliased coefficients first
aliased_coefs <- alias(model_total)

if (!is.null(aliased_coefs$Complete)) {
  cat("Warning: Model has aliased coefficients. VIF cannot be calculated.\n")
  cat("Aliased coefficients detected:\n")
  print(aliased_coefs$Complete)
  cat("\nThis typically occurs when predictors are perfectly correlated.\n")
  cat("Consider removing either 'season' or 'month_factor' from the model.\n\n")
} else {
  # Only calculate VIF if no aliased coefficients
  tryCatch({
    vif_values <- vif(model_total)
    cat("Variance Inflation Factors:\n")
    print(vif_values)
  }, error = function(e) {
    cat("Error calculating VIF:", e$message, "\n")
  })
}

# Test if there's a significant difference in non-violent crime counts
# between months controlling for weekend
anova_month_weekend_nv <- aov(count_nonviolent ~ month_factor + weekend_factor,
                              data = daily_counts)
summary(anova_month_weekend_nv)

# Post-hoc test if significant
if (summary(anova_month_weekend_nv)[[1]][["Pr(>F)"]][1] < 0.05) {
  cat("\nMonth is significant. Conducting post-hoc Tukey HSD test:\n")
  tukey_month_nv <- TukeyHSD(anova_month_weekend_nv, "month_factor")
  print(tukey_month_nv)
}

# Test if there's a significant difference in non-violent crime counts
# between months controlling for season
anova_month_season_nv <- aov(count_nonviolent ~ month_factor + season,
                             data = daily_counts)
summary(anova_month_season_nv)

# Test if there's a significant difference in violent crime counts
# between months controlling for weekend
anova_month_weekend_v <- aov(count_violent ~ month_factor + weekend_factor,
                             data = daily_counts)
summary(anova_month_weekend_v)

# Post-hoc test if significant
if (summary(anova_month_weekend_v)[[1]][["Pr(>F)"]][1] < 0.05) {
  cat("\nMonth is significant. Conducting post-hoc Tukey HSD test:\n")
  tukey_month_v <- TukeyHSD(anova_month_weekend_v, "month_factor")
  print(tukey_month_v)
}

# Test if there's a significant difference in violent crime counts
# between months controlling for season
anova_month_season_v <- aov(count_violent ~ month_factor + season,
                            data = daily_counts)
summary(anova_month_season_v)

# Visualize mean crime counts by month
daily_counts %>%
  group_by(month_factor) %>%
  summarise(
    mean_nonviolent = mean(count_nonviolent),
    mean_violent = mean(count_violent),
    se_nonviolent = sd(count_nonviolent) / sqrt(n()),
    se_violent = sd(count_violent) / sqrt(n())
  ) %>%
  pivot_longer(cols = c(mean_nonviolent, mean_violent),
               names_to = "crime_type",
               values_to = "mean_count") %>%
  mutate(
    se = ifelse(crime_type == "mean_nonviolent", se_nonviolent, se_violent),
    crime_type = ifelse(crime_type == "mean_nonviolent",
                        "Non-Violent", "Violent")
  ) %>%
  ggplot(aes(x = month_factor, y = mean_count, fill = crime_type)) +
  geom_col(position = "dodge") +
  geom_errorbar(aes(ymin = mean_count - se, ymax = mean_count + se),
                position = position_dodge(0.9), width = 0.2) +
  labs(title = "Mean Daily Crime Counts by Month",
       x = "Month", y = "Mean Count",
       fill = "Crime Type") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Summary statistics by season
season_summary <- daily_counts %>%
  group_by(season) %>%
  summarise(
    mean_total = mean(count_total),
    mean_violent = mean(count_violent),
    mean_nonviolent = mean(count_nonviolent),
    sd_total = sd(count_total)
  )

kable(season_summary,
      caption = "Crime Count Summary by Season",
      digits = 2)

# Summary statistics by weekend
weekend_summary <- daily_counts %>%
  group_by(weekend_factor) %>%
  summarise(
    mean_total = mean(count_total),
    mean_violent = mean(count_violent),
    mean_nonviolent = mean(count_nonviolent),
    sd_total = sd(count_total)
  )

kable(weekend_summary,
      caption = "Crime Count Summary by Weekend/Weekday",
      digits = 2)

