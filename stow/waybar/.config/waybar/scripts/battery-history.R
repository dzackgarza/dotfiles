#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(forecast)
  library(ggplot2)
  library(readr)
  library(dplyr)
  library(tidyr)
  library(lubridate)
})

args <- commandArgs(trailingOnly = TRUE)
input_path <- args[[1]]
output_path <- args[[2]]
range_seconds <- as.numeric(args[[3]])

history <- read_csv(input_path, show_col_types = FALSE) |>
  mutate(timestamp = as.POSIXct(timestamp, origin = "1970-01-01", tz = Sys.timezone())) |>
  arrange(timestamp)

if (nrow(history) < 2) {
  stop("UPower returned too little history for analysis")
}

history <- history |>
  mutate(time_num = as.numeric(timestamp))

smooth_grid <- tibble(
  timestamp = seq(min(history$timestamp), max(history$timestamp), length.out = 200)
) |>
  mutate(
    time_num = as.numeric(timestamp),
    percentage = predict(loess(percentage ~ time_num, data = history, span = 0.5), time_num)
  )

regular <- tibble(
  timestamp = seq(
    floor_date(min(history$timestamp), unit = "minute"),
    ceiling_date(max(history$timestamp), unit = "minute"),
    by = "1 min"
  )
) |>
  mutate(time_num = as.numeric(timestamp)) |>
  left_join(history |> select(timestamp, percentage), by = "timestamp")

regular$percentage <- approx(
  x = history$time_num,
  y = history$percentage,
  xout = regular$time_num,
  rule = 2
)$y

forecast_horizon <- max(5, min(60, ceiling(range_seconds / 60 * 0.25)))
forecast_fit <- forecast(auto.arima(ts(regular$percentage, frequency = 1)), h = forecast_horizon)
forecast_data <- tibble(
  timestamp = seq(
    max(regular$timestamp) + minutes(1),
    by = "1 min",
    length.out = forecast_horizon
  ),
  percentage = pmin(100, pmax(0, as.numeric(forecast_fit$mean))),
  lower = pmin(100, pmax(0, as.numeric(forecast_fit$lower[, 2]))),
  upper = pmin(100, pmax(0, as.numeric(forecast_fit$upper[, 2])))
)

break_interval <- case_when(
  range_seconds <= 3600 ~ "15 min",
  range_seconds <= 10800 ~ "30 min",
  range_seconds <= 28800 ~ "1 hour",
  TRUE ~ "3 hours"
)

plot <- ggplot(history, aes(timestamp, percentage)) +
  geom_ribbon(
    data = forecast_data,
    aes(timestamp, ymin = lower, ymax = upper),
    inherit.aes = FALSE,
    fill = "#81a1c1",
    alpha = 0.2
  ) +
  geom_line(aes(color = "Observed"), linewidth = 0.8) +
  geom_point(aes(color = "Observed"), size = 1.5) +
  geom_line(
    data = smooth_grid,
    aes(timestamp, percentage, color = "LOESS"),
    linewidth = 1.1,
    inherit.aes = FALSE
  ) +
  geom_line(
    data = forecast_data,
    aes(timestamp, percentage, color = "Forecast"),
    linewidth = 1,
    linetype = "dashed",
    inherit.aes = FALSE
  ) +
  scale_x_datetime(
    date_labels = "%H:%M",
    date_breaks = break_interval,
    expand = c(0.01, 0)
  ) +
  scale_y_continuous(limits = c(0, 100), breaks = seq(0, 100, 25)) +
  scale_color_manual(
    values = c(Observed = "#a3be8c", LOESS = "#88c0d0", Forecast = "#81a1c1")
  ) +
  labs(x = NULL, y = "Battery (%)", title = "Battery history") +
  theme_minimal(base_size = 11) +
  theme(
    plot.background = element_rect(fill = "#1f1f26", color = NA),
    panel.background = element_rect(fill = "#1f1f26", color = NA),
    panel.grid = element_line(color = "#4c566a", linewidth = 0.25),
    axis.text = element_text(color = "#d8dee9"),
    axis.title = element_text(color = "#d8dee9"),
    plot.title = element_text(color = "#d8dee9"),
    legend.position = "bottom",
    legend.text = element_text(color = "#d8dee9"),
    legend.title = element_blank()
  )

ggsave(output_path, plot, width = 8, height = 4.5, dpi = 120, bg = "#1f1f26")
