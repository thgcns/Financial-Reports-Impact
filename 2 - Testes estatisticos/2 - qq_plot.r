# Caminho para o arquivo CSV
caminho_arquivo <- "C:\\Users\\thgcn\\OneDrive\\Academico\\Financial-Reports-Impact\\retornos_finais.csv"

# Carregar o arquivo CSV e verificar a especificação das colunas
data <- read_csv(caminho_arquivo, show_col_types = TRUE)

# Selecionar a coluna correta para retorno_com_publicacao
Return <- data$Returns
nxt_return <- data$nxt_return
remaining_return_week <- data$remaining_return_week
first_return_week <- data$first_return_week
remaining_return_month <- data$remaining_return_month
first_return_month <- data$first_return_month


# Remover NAs se necessário
Return <- na.omit(Return)
Return <- as.numeric(Return)
nxt_return <- na.omit(nxt_return)
nxt_return <- as.numeric(nxt_return)
remaining_return_week <- na.omit(remaining_return_week)
remaining_return_week <- as.numeric(remaining_return_week)
first_return_week <- na.omit(first_return_week)
first_return_week <- as.numeric(first_return_week)
remaining_return_month <- na.omit(remaining_return_month)
remaining_return_month <- as.numeric(remaining_return_month)
first_return_month <- na.omit(first_return_month)
first_return_month <- as.numeric(first_return_month)

# Função para plotar QQ plot
qq_plot <- function(data, title) {
  # Criar um dataframe para ggplot
  data_df <- data.frame(sample = data)
  
  # Criar o QQ plot
  p <- ggplot(data_df, aes(sample = sample)) +
    stat_qq() +
    stat_qq_line() +
    ggtitle(title) +
    theme_minimal()
  
  # Mostrar o gráfico
  print(p)
}



# Gerar QQ plot para retorno_com_publicacao
qq_plot(Return, "QQ plot para retornos diários sem influência")
qq_plot(nxt_return, "QQ plot para retornos diários com influência")
qq_plot(remaining_return_week, "QQ plot para retornos semanais sem influência")
qq_plot(first_return_week, "QQ plot para retornos semanais com influência")
qq_plot(remaining_return_month, "QQ plot para retornos mensais sem influência")
qq_plot(first_return_month, "QQ plot para retornos mensais com influência")

