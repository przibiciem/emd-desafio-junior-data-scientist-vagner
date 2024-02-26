# Instruções - Como rodar meu código e visualização
Candidato: Vagner Przibiciem

## Arquivo analise_sql.sql

O arquivo analise_sql.sql está organizado questão à questão, contendo o número referente à mesma, a resposta da questão, e o código SQL utilizado para realizar a consulta no BigQuery no sistema da Google Cloud Platform.

Para rodar o código SQL, basta acessar a plataforma GCP, escolher um projeto, acessar a ferramenta BigQuery e realizar a consulta, seguindo os passos indicados no tutorial.

## Arquivo analise_python.ipynb

Para rodar o analise_python.ipynb, será necessário um interpretador como o Jupyter Notebook.
Basta executar o jupyter notebook, rodando o comando "jupyter notebook" em um ambiente python com os seguintes pacotes:
- basedosdados
- pandas
- datetime

Na sequência, abrir o analise_python.ipynb pelo explorador de arquivos do Jupyter Notebook.
Já será possível visualizar todo o código e os outputs. Caso queria rodar as células novamente, será necessário alterar o valor da variável id_projeto, na célula 1, para o seu id de projeto do GCP, após fazer a autenticação na máquina que será utilizada (creio que não seja possível utilizar o meu id de projeto, já que também é necessário autenticação).

## Arquivos de visualização. visualizacao.py e visualizacao2.py

Para rodar os arquivos de visualização, é necessário novamente autenticar com o python em sua conta GCP, e então alterar o valor da variável id_projeto para o nome do seu projeto do GCP.
Para abrir a visualização, será necessário abrir o prompt de comando, e utilizar um ambiente python com os seguintes pacotes instalados:
- streamlit
- pandas
- basedosdados
- datetime
Na sequência, rode os seguintes comando no cmd (lembre-se de alterar o caminho do arquivo para o caminho o qual o mesmo está salvo em sua máquina):
-streamlit run "c:\processo seletivo\visualizacao.py"
-streamlit run "c:\processo seletivo\visualizacao2.py"
