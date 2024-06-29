# Carregar as bibliotecas necessárias
library(ggplot2)
library(stats)

# Supondo que 'filtered_data' e 'new_final_data' são data frames já carregados
# Se necessário, substitua pela carga dos seus dados
# filtered_data <- read.csv('filtered_data.csv')
# new_final_data <- read.csv('new_final_data.csv')

# Selecionando os retornos
nxt_return <- filtered_data$nxt_return
Return <- new_final_data$Return
week_return <- new_final_data$week_return
month_return <- new_final_data$month_return

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

# Gerando QQ plots para comparar os quantis
qq_plot(nxt_return, 'QQ plot for nxt_return')
qq_plot(Return, 'QQ plot for Return')
qq_plot(week_return, 'QQ plot for week_return')
qq_plot(month_return, 'QQ plot for month_return')
