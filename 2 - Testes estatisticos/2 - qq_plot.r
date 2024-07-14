# Instalar e carregar pacotes necessários
install.packages("rlang", dependencies = TRUE)
install.packages(c("ggplot2", "qqplotr", "readr"))
library(ggplot2)
library(qqplotr)
library(readr)

# Carregar o CSV
data <- read_csv("retornos_finais.csv")

# Função para gerar QQ plots
generate_qqplot <- function(data, column_name) {
  ggplot(data, aes(sample = !!sym(column_name))) +
    stat_qq() +
    stat_qq_line() +
    labs(title = paste("QQ plot for", column_name),
         x = "Theoretical Quantiles",
         y = "Sample Quantiles") +
    theme_minimal()
}

# Gerar QQ plots para cada coluna
columns <- c('Return', 'nxt_return', 'first_return_week', 'remaining_return_week', 'first_return_month', 'remaining_return_month')

for (column in columns) {
  plot <- generate_qqplot(data, column)
  print(plot)
}

