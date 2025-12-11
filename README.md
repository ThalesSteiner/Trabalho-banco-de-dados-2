# 📊 Projeto de Banco de Dados II: League of Legends 

Projeto acadêmico voltado para a criação de um ambiente completo de banco de dados, garantindo integridade e segurança das informações, a partir de uma base de dados de League of Legends com foco na análise de partidas competitivas.




## 🎯 Objetivos do Projeto

O objetivo principal deste trabalho foi simular o ciclo de vida completo de um projeto em PostgreSQL para análises, partindo de dados brutos e desorganizados até a entrega de inteligência de negócio.

As etapas cumpridas foram:
-  **Análise de Dados:** Compreensão da base original e criação do Dicionário de Dados.
-  **Modelagem e Normalização:** Transformação de uma tabela para um modelo relacional na 3ª Forma Normal (3FN).
-  **Migração (ETL):** Scripts complexos de limpeza e carga de dados, tratando inconsistências
-  **Automatização:** Implementação de regras de negócio via *Triggers*, *Functions*, *Views* e *Procedures* no PostgreSQL.
-  **Business Intelligence:** Modelagem Dimensional e criação de um Data Warehouse para responder perguntas estratégicas.


## 🛠️ Tecnologias Utilizadas

* **SGBD:** PostgreSQL

* **Interface de Desenvolvimento:** DBeaver

* **Linguagens:** PostgreSQL, Python, Docker


## 📂 Estrutura do Banco de Dados

O projeto foi organizado em três *Schemas* lógicos para separar as responsabilidades:

| Schema | Nome | Descrição |
| :--- | :--- | :--- |
| `o` | **Original** | Base de dados original, com todas as entradas do usuário. |
| `n` | **Normalizado** |Tabelas relacionadas, integridade referencial (FKs) e dados limpos. |
| `dw` | **Data Warehouse** | Tabelas desnormalizadas (Fato e Dimensões) otimizadas para leitura e BI. |



## 🔍 Fonte de Dados

A base de dados foi obtida no Kaggle:

* **Fonte Original:** [League Of Legends Data](https://www.kaggle.com/datasets/prestonrobertson7/league-of-legends-data-9292022?select=Sep-09-2022_10000matches.csv)
* **Conteúdo:** Métricas detalhadas de combate (Kills, Deaths, Assists), economia (Gold), visão (Wards) e objetivos (Barão, Dragão).






## 🧠 Inteligência de Negócio (BI)

O Data Warehouse foi projetado para responder perguntas como:
* *"Quais campeões possuem a maior taxa de vitória em partidas com duração superior a 35 minutos?"*
* *"Existe uma vantagem estatística para o Time Azul no modo competitivo?"*
* *"Qual a relação entre o ouro acumulado e a quantidade de sentinelas colocadas?"*


## 👨‍💻 Autores

Este projeto foi desenvolvido como parte da avaliação da disciplina de Banco de Dados II.

* **Daniel Carvalho**
* **Iuri Sajnin**
* **Pedro Favato**
* **Thales Steiner**

