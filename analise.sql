# -*- coding: utf-8 -*-
"""

@author: Vagner
"""

-- 1. Resposta: 73 chamados.

SELECT COUNT(*) AS nchamados
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE data_inicio >= '2023-04-01' AND data_inicio < '2023-04-02';

-- 2. Resposta: Poluição Sonora.

SELECT tipo, COUNT(*) AS quantidade
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE data_inicio >= '2023-04-01' AND data_inicio < '2023-04-02'
GROUP BY tipo
ORDER BY quantidade DESC;
/* OBS.: É possível utilizar "LIMIT 1" para mostrar apenas o tipo de chamado que mais teve chamados abertos no dia 01/04/2023, porém optei por não utilizar pois pode haver um empate de número de chamados entre dois tipos diferentes. */


-- 3. Resposta: Engenho de Dentro, Leblon e Campo Grande.

SELECT bairro.nome, COUNT(*) AS quantidade
FROM datario.administracao_servicos_publicos.chamado_1746
JOIN datario.dados_mestres.bairro ON chamado_1746.id_bairro = bairro.id_bairro
WHERE data_inicio >= '2023-04-01' AND data_inicio < '2023-04-02'
GROUP BY chamado_1746.id_bairro, bairro.nome
ORDER BY quantidade DESC;
/* OBS.: Assim como na pergunta anterior, é possível adicionar "LIMIT 3" para retornar apenas os 3 bairros com mais chamados */

-- 4. Resposta: Zona Norte.

SELECT bairro.subprefeitura, COUNT(*) AS quantidade
FROM datario.administracao_servicos_publicos.chamado_1746
JOIN datario.dados_mestres.bairro ON chamado_1746.id_bairro = bairro.id_bairro
WHERE data_inicio >= '2023-04-01' AND data_inicio < '2023-04-02'
GROUP BY bairro.subprefeitura
ORDER BY quantidade DESC;
/* OBS.: Assim como nas perguntas anteriores, é possível adicionar "LIMIT 1" para retornar apenas a subprefeitura com mais chamados */

-- 5. Resposta: Existe 1 chamado aberto sem associação a bairro ou subprefeitura. Isto acontece pois tal chamado não possui nenhum dado de posição, como coordenadas por exemplo.

SELECT COUNT(*) AS qtd_vazio
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE data_inicio >= '2023-04-01' AND data_inicio < '2023-04-02' AND id_bairro IS NULL;

/* Por meio do código acima foi encontrado apenas um chamado nesse dia que não pode ser relacionado a um bairro ou subprefeitura, isso se dá pelo fato do chamado em questão não possuir nenhum dado de posição. Essa afirmação pode ser verificada ao realizar a consulta abaixo*/

SELECT *
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE data_inicio >= '2023-04-01' AND data_inicio < '2023-04-02' AND id_bairro IS NULL;

/* Além disso, também não é possível relacionar tal chamado a nenhuma subprefeitura, já que para tal é necessário um valor de id_bairro a fim de comparar com a tabela "bairro" */

-- 6. Resposta: 42408 chamados.

SELECT COUNT(*) AS quantidade
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE data_inicio >= '2022-01-01' AND data_inicio < '2024-01-01' AND subtipo = 'Perturbação do sossego';

-- 7.

-- Para encontrar os intervalos de tempo dos grandes eventos:
SELECT * FROM datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos

/* Para selecionar os dados dentre os intervalos encontrados:
Carnaval de 2023-02-18 a 2023-02-21
Reveillón de 2022-12-30 a 2023-01-01
Rock in Rio de 2022-09-02 a 2022-09-04
Rock in Rio de 2022-09-08 a 2022-09-11 */

SELECT *
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE 
  subtipo = 'Perturbação do sossego'
  AND (
    (data_inicio >= '2023-02-18' AND data_inicio < '2023-02-22')
    OR (data_inicio >= '2022-12-30' AND data_inicio < '2023-01-02')
    OR (data_inicio >= '2022-09-02' AND data_inicio< '2022-09-05')
    OR (data_inicio >= '2022-09-08' AND data_inicio < '2022-09-12')
  );
-- 8.

-- Carnaval. Resposta: 241 chamados.
SELECT COUNT(*)
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE 
  subtipo = 'Perturbação do sossego'
  AND (
    (data_inicio >= '2023-02-18' AND data_inicio < '2023-02-22')
  );

Reveillon. Resposta: 137 chamados.
SELECT COUNT(*)
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE 
  subtipo = 'Perturbação do sossego'
  AND (
    (data_inicio >= '2022-12-30' AND data_inicio < '2023-01-02')
  );
  
Rock and Rio (1). Resposta: 366 chamados.
SELECT COUNT(*)
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE 
  subtipo = 'Perturbação do sossego'
  AND (
    (data_inicio >= '2022-09-02' AND data_inicio< '2022-09-05')
  );
  
Rock and Rio (2). Resposta: 468 chamados.
SELECT COUNT(*)
FROM datario.administracao_servicos_publicos.chamado_1746
WHERE 
  subtipo = 'Perturbação do sossego'
  AND (
    (data_inicio >= '2022-09-08' AND data_inicio < '2022-09-12')
  );

-- 9. Obs.: Este código cria uma tabela do número de chamados por dia, e então a média entre esse número de chamados, omitindo dias em que possivelmente não ocorra nenhum chamado.

-- Carnaval. Resposta: 60.25...
SELECT AVG(chamados)
  FROM(
    SELECT 
        DATE(data_inicio),
        COUNT(*) AS chamados
    FROM 
        datario.administracao_servicos_publicos.chamado_1746
    WHERE 
        data_inicio >= '2023-02-18' AND data_inicio < '2023-02-22' AND subtipo = 'Perturbação do sossego'
    GROUP BY 
        DATE(data_inicio)
);

-- Reveillon. Resposta: 45.66...
SELECT AVG(chamados)
  FROM(
    SELECT 
        DATE(data_inicio),
        COUNT(*) AS chamados
    FROM 
        datario.administracao_servicos_publicos.chamado_1746
    WHERE 
        data_inicio >= '2022-12-30' AND data_inicio < '2023-01-02' AND subtipo = 'Perturbação do sossego'
    GROUP BY 
        DATE(data_inicio)
);

-- Rock and Rio (1). Resposta: 122.0
SELECT AVG(chamados)
  FROM(
    SELECT 
        DATE(data_inicio),
        COUNT(*) AS chamados
    FROM 
        datario.administracao_servicos_publicos.chamado_1746
    WHERE 
        data_inicio >= '2022-09-02' AND data_inicio< '2022-09-05' AND subtipo = 'Perturbação do sossego'
    GROUP BY 
        DATE(data_inicio)
);

-- Rock and Rio (2). Resposta: 117.0
SELECT AVG(chamados)
  FROM(
    SELECT 
        DATE(data_inicio),
        COUNT(*) AS chamados
    FROM 
        datario.administracao_servicos_publicos.chamado_1746
    WHERE 
       data_inicio >= '2022-09-08' AND data_inicio < '2022-09-12' AND subtipo = 'Perturbação do sossego'
    GROUP BY 
        DATE(data_inicio)
);

-- 10. Resposta: 58.093, considerando todos os dias no período (primeiro código), ou 63.201, omitindo dias com 0 chamados (segundo código).

-- Primeiro código (Valor correto de média diária, contendo dias com 0 chamados)
SELECT 
COUNT(*)/730
FROM 
datario.administracao_servicos_publicos.chamado_1746
WHERE 
data_inicio >= '2022-01-01' AND data_inicio < '2024-01-01' AND subtipo = 'Perturbação do sossego';

-- Segundo código (Valor de média diária apenas de dias com chamados)
SELECT AVG(chamados)
  FROM(
    SELECT 
        DATE(data_inicio),
        COUNT(*) AS chamados
    FROM 
        datario.administracao_servicos_publicos.chamado_1746
    WHERE 
        data_inicio >= '2022-01-01' AND data_inicio < '2024-01-01' AND subtipo = 'Perturbação do sossego'
    GROUP BY 
        DATE(data_inicio)
);

/* Em conclusão, o Reveillon e Carnaval apresentaram médias diárias de chamados por perturbação do sossego menores do que a média do intervalo entre 2022 e 2023, enquanto os dias de Rock in Rio tiveram uma média de chamados aproximadamente igual ao dobro da média do intervalo entre 2022 e 2023. */

