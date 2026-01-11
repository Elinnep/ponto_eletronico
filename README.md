# Sistema de Controle de Frequência e Ponto Eletrônico

## 1. Introdução

Este documento descreve a idealização e especificação do sistema **Controle de Frequência e Ponto Eletrônico**, desenvolvido como parte da avaliação prática da disciplina de Desenvolvimento Web II.

O sistema tem como objetivo permitir o registro, acompanhamento e consulta da frequência de usuários, simulando um sistema de ponto eletrônico corporativo.

### 1.1 Tecnologias Utilizadas

* **Backend:** Django (Python)
* **Banco de Dados:** SQLite
* **Frontend:** HTML + Tailwind CSS
* **Autenticação:** Django Auth

---

## 2. Escopo do Sistema

O sistema permitirá:

* Cadastro e autenticação de usuários
* Registro de entradas, saídas e intervalos
* Consulta do espelho de ponto mensal
* Visualização de status de frequência

---

## 3. Requisitos Funcionais

### RF01 – Cadastro de Usuários

O sistema deve permitir o cadastro de usuários contendo:

* Nome completo
* Matrícula
* E-mail
* Senha

### RF02 – Autenticação

O sistema deve permitir que usuários cadastrados realizem login e logout de forma segura.

### RF03 – Registro de Ponto

O sistema deve permitir que o usuário registre:

* Entrada
* Início de intervalo
* Fim de intervalo
* Saída

Cada registro deve armazenar data e horário automaticamente.

### RF04 – Validação de Registros

O sistema deve impedir registros duplicados do mesmo tipo no mesmo dia.

### RF05 – Dashboard do Usuário

O sistema deve exibir:

* Horário atual
* Botão de registro de ponto
* Resumo do dia
* Últimas atividades

### RF06 – Espelho de Ponto

O sistema deve permitir a visualização mensal do espelho de ponto contendo:

* Data
* Horários registrados
* Total de horas
* Status do dia

### RF07 – Cálculo de Horas

O sistema deve calcular automaticamente:

* Total de horas trabalhadas por dia
* Total acumulado no mês

---

## 4. Requisitos Não Funcionais

### RNF01 – Plataforma

O sistema deve ser desenvolvido exclusivamente em Django.

### RNF02 – Banco de Dados

O sistema deve utilizar o banco de dados SQLite.

### RNF03 – Interface

A interface deve:

* Ser simples e intuitiva
* Utilizar Tailwind CSS

### RNF04 – Segurança

* Senhas devem ser armazenadas de forma criptografada
* Acesso às páginas deve ser restrito a usuários autenticados

### RNF05 – Desempenho

O sistema deve responder às ações do usuário em tempo aceitável.

---

## 5. Regras de Negócio

* Um usuário só pode registrar um tipo de ponto uma vez por dia
* A saída só pode ser registrada após a entrada
* Intervalo só pode ocorrer após a entrada
* Dias sem registros são considerados falta

---

## 6. Modelo de Dados (DER)

### 6.1 Entidades

#### Usuário

* id (PK)
* nome
* matricula
* email
* senha

#### RegistroPonto

* id (PK)
* usuario_id (FK)
* data
* hora
* tipo (ENTRADA, INICIO_INTERVALO, FIM_INTERVALO, SAIDA)

#### FrequenciaDia

* id (PK)
* usuario_id (FK)
* data
* total_horas
* status

### 6.2 Relacionamentos

* Usuário **1:N** RegistroPonto
* Usuário **1:N** FrequenciaDia

---

## 7. Casos de Uso

### UC01 – Realizar Login

**Ator:** Usuário

1. Usuário acessa a tela de login
2. Informa e-mail/matrícula e senha
3. Sistema valida credenciais
4. Sistema redireciona para o dashboard

### UC02 – Registrar Ponto

**Ator:** Usuário

1. Usuário acessa o dashboard
2. Clica no botão registrar ponto
3. Sistema registra horário e tipo automaticamente

### UC03 – Consultar Espelho de Ponto

**Ator:** Usuário

1. Usuário acessa menu "Meu Ponto"
2. Seleciona mês e ano
3. Sistema exibe registros e totais

---

## 8. Telas do Sistema

### 8.1 Tela de Login

* Campo de matrícula ou e-mail
* Campo de senha
* Botão entrar

### 8.2 Dashboard

* Saudação ao usuário
* Relógio em tempo real
* Botão de registro de ponto
* Resumo do dia

### 8.3 Espelho de Ponto

* Filtro por mês e ano
* Tabela de registros
* Indicadores de horas e ocorrências

---

## 9. Considerações Finais

Este sistema atende aos requisitos propostos para a avaliação, utilizando tecnologias simples, arquitetura organizada e boas práticas de desenvolvimento web com Django.

A implementação pode ser expandida futuramente para múltiplos perfis de usuário, aprovação de ajustes e relatórios administrativos.

**Credenciais de teste já criadas:**
- CPF: `12345678901`
- Senha: `admin123`