# 🌤️ ETL Pipeline — Clima de São Paulo

Pipeline ETL automatizado que coleta dados meteorológicos de São Paulo via API do OpenWeather, processa com Python/Pandas e armazena em PostgreSQL, orquestrado pelo Apache Airflow em ambiente Docker.

---

## 🏗️ Arquitetura

```
OpenWeather API
      │
      ▼
  [ EXTRACT ]  ──→  weather_data.json
      │
      ▼
  [ TRANSFORM ] ──→ limpeza, renomeação e conversão de timezone
      │
      ▼
  [ LOAD ] ──→ PostgreSQL (tabela: sp_weather)
      │
   (tudo orquestrado pelo Apache Airflow via DAG)
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| 🐍 Python | Scripts ETL (extract, transform, load) |
| 🐼 Pandas | Normalização e transformação dos dados |
| 🌬️ Apache Airflow | Orquestração e agendamento da pipeline |
| 🐘 PostgreSQL | Armazenamento dos dados finais |
| 🐳 Docker | Containers e persistência de volumes |
| 🐧 WSL (Linux) | Ambiente de linha de comando |

---

## 📁 Estrutura do Projeto

```
projeto/
├── config/
│   └── .env                  # Variáveis de ambiente (credenciais)
├── src/
│   ├── extract_data.py       # Extração da API OpenWeather
│   ├── transform_data.py     # Limpeza e transformação
│   └── load_data.py          # Carga no PostgreSQL
├── dags/
│   └── weather_pipeline.py   # DAG do Airflow
├── data/
│   └── weather_data.json     # Dados brutos extraídos
├── notebooks/
│   └── normalizacao.ipynb    # Exploração e normalização inicial
└── docker-compose.yml
```

---

## ⚙️ Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (ou Docker Engine + WSL)
- [WSL 2](https://learn.microsoft.com/pt-br/windows/wsl/install) (se Windows)
- Chave de API gratuita do [OpenWeather](https://openweathermap.org/api)

---

## 🚀 Instalação e Execução

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2️⃣ Configure as variáveis de ambiente

Crie o arquivo `config/.env` com base no exemplo abaixo:

```env
user=seu_usuario_postgres
password=sua_senha_postgres
database=nome_do_banco
api_key=sua_chave_openweather
```

### 3️⃣ Suba os containers com Docker

```bash
docker-compose up -d
```

Isso irá inicializar os seguintes serviços:

- 🐘 **PostgreSQL** — banco de dados na porta `5432`
- 🌬️ **Airflow** (webserver, scheduler, worker, etc.) — UI na porta `8080`
- 📦 **Redis** — broker de mensagens do Airflow

### 4️⃣ Acesse o Airflow

Abra o navegador em: [http://localhost:8080](http://localhost:8080)

- Usuário padrão: `airflow`
- Senha padrão: `airflow`

### 5️⃣ Ative a DAG

Na interface do Airflow, localize a DAG `weather_pipeline` e ative-a clicando no toggle. Ela está agendada para rodar a **cada hora** (`0 */1 * * *`).

---

## 🔄 Detalhes da Pipeline

### 📥 Extract (`extract_data.py`)

Faz uma requisição GET à API do OpenWeather para a cidade de São Paulo e salva a resposta em `data/weather_data.json`.

```
GET https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}
```

### 🔧 Transform (`transform_data.py`)

Aplica as seguintes transformações no DataFrame:

- ❌ **Remove** as colunas: `weather`, `weather_icon`, `sys.type`
- 🕐 **Converte timezone** para horário de SP (`America/Sao_Paulo`): `datetime`, `sunrise`, `sunset`
- ✏️ **Renomeia** todas as colunas para um padrão legível

O resultado intermediário é salvo em `/opt/airflow/data/temp_data.parquet`.

### 📤 Load (`load_data.py`)

Conecta ao PostgreSQL via SQLAlchemy (`psycopg2`) e insere os dados transformados na tabela `sp_weather` com `if_exists='append'` — preservando o histórico de todas as coletas.

### 🗂️ DAG (`weather_pipeline.py`)

```
extract() >> transform() >> load()
```

| Configuração | Valor |
|---|---|
| DAG ID | `weather_pipeline` |
| Schedule | A cada 1 hora (`0 */1 * * *`) |
| Retries | 2 |
| Retry delay | 5 minutos |
| Tags | `weather`, `etl` |

---

## 🗄️ Tabela no PostgreSQL

A tabela `sp_weather` armazena os dados processados. Para visualizar, acesse o **pgAdmin** ou execute:

```sql
SELECT * FROM sp_weather;
```

Principais colunas da tabela:

| Coluna | Descrição |
|---|---|
| `datetime` | Data e hora da coleta (horário SP) |
| `city_name` | Cidade (São Paulo) |
| `temperature` | Temperatura atual (°C) |
| `feels_like` | Sensação térmica (°C) |
| `temp_min` / `temp_max` | Temperaturas mínima e máxima |
| `humidity` | Umidade relativa (%) |
| `pressure` | Pressão atmosférica (hPa) |
| `wind_speed` | Velocidade do vento (m/s) |
| `sunrise` / `sunset` | Nascer e pôr do sol (horário SP) |

---

## 🐛 Troubleshooting

**Airflow não encontra os módulos Python?**
Verifique se o caminho `/opt/airflow/src` está inserido no `sys.path` da DAG.

**Erro de conexão com o PostgreSQL?**
Confirme que o `host` está como `host.docker.internal` (comunicação entre containers) e que o `.env` está correto.

**DAG não aparece no Airflow?**
Certifique-se que o arquivo da DAG está na pasta mapeada como `dags/` no `docker-compose.yml`.

---

## 📄 Licença

Este projeto é de uso educacional e livre para adaptações. 🤝