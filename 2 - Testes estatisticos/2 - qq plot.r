# Carregar as bibliotecas necess�rias
library(ggplot2)
library(gridExtra)
library(readr)

# Caminho para o arquivo CSV
caminho_arquivo <- "C:\\Users\\thgcn\\OneDrive\\Academico\\Financial-Reports-Impact\\retornos_finais.csv"

# Carregar o arquivo CSV e verificar a especifica��o das colunas
data <- read_csv(caminho_arquivo, show_col_types = TRUE)

# Selecionar as colunas corretas
Return <- data$Returns
nxt_return <- data$nxt_return
remaining_return_week <- data$remaining_return_week
first_return_week <- data$first_return_week
remaining_return_month <- data$remaining_return_month
first_return_month <- data$first_return_month

# Remover NAs e converter para num�rico
Return <- as.numeric(na.omit(Return))
nxt_return <- as.numeric(na.omit(nxt_return))
remaining_return_week <- as.numeric(na.omit(remaining_return_week))
first_return_week <- as.numeric(na.omit(first_return_week))
remaining_return_month <- as.numeric(na.omit(remaining_return_month))
first_return_month <- as.numeric(na.omit(first_return_month))

# Fun��o para plotar QQ plot
qq_plot <- function(data, title) {
  # Criar um dataframe para ggplot
  data_df <- data.frame(sample = data)
  
  # Criar o QQ plot
  p <- ggplot(data_df, aes(sample = sample)) +
    stat_qq() +
    stat_qq_line() +
    ggtitle(title) +
    theme_minimal()
  
  # Retornar o gr�fico ggplot
  return(p)
}

# Criar os gr�ficos
plot1 <- qq_plot(Return, "Retornos di�rios sem influ�ncia")
plot2 <- qq_plot(nxt_return, "Retornos di�rios com influ�ncia")
plot3 <- qq_plot(remaining_return_week, "Retornos semanais sem influ�ncia")
plot4 <- qq_plot(first_return_week, "Retornos semanais com influ�ncia")
plot5 <- qq_plot(remaining_return_month, "Retornos mensais sem influ�ncia")
plot6 <- qq_plot(first_return_month, "Retornos mensais com influ�ncia")

# Organizar os gr�ficos em uma grade

grid.arrange(plot1, plot2, plot3, plot4, plot5, plot6, nrow = 3)
