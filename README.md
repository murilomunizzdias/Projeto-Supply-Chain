# ⬡ Supply Chain — Monitor de Operações

Pipeline completa de dados para Supply Chain: tratamento de dados, API REST, frontend React e dashboard analítico com Streamlit.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Dados | Python + Pandas + Jupyter |
| Banco | PostgreSQL |
| API | FastAPI + psycopg2 |
| Frontend | React 19 + Vite + Axios |
| Dashboard | Streamlit + Plotly + PyDeck |

---

## Estrutura do Projeto

```
Projeto-Supply-Chain/
├── .venv/
├── .env                        # credenciais (não subir no git)
├── data/
│   └── supply_chain_clean.csv
├── notebooks/
│   └── Limpeza.ipynb
├── scripts/
├── sql/
├── api/
│   ├── main.py                 # FastAPI + CORS
│   ├── database.py             # conexão PostgreSQL
│   └── routers/
│       ├── kpis.py
│       ├── alerts.py
│       ├── analysis.py
│       └── insercao.py
├── frontend/                   # React + Vite
│   └── src/
│       ├── components/
│       │   ├── SideBar.jsx
│       │   ├── KpiCard.jsx
│       │   └── AlertaCard.jsx
│       └── pages/
│           ├── Dashboard.jsx
│           ├── Alertas.jsx
│           └── Simulador.jsx
└── dashboard/
    └── app.py                  # Streamlit
```

---

## Configuração

### 1. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=SupplyChain
DB_USER=postgres
DB_PASSWORD=sua_senha
```

### 2. Instalar dependências Python

```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv streamlit plotly pydeck pandas requests
```

### 3. Instalar dependências do frontend

```bash
cd frontend
npm install
```

---

## Como Rodar

Abra **3 terminais** na raiz do projeto:

**Terminal 1 — API:**
```bash
uvicorn api.main:app --reload
```
Acesse: http://localhost:8000/docs

**Terminal 2 — Frontend React:**
```bash
cd frontend
npm run dev
```
Acesse: http://localhost:5173

**Terminal 3 — Dashboard Streamlit:**
```bash
streamlit run dashboard/app.py
```
Acesse: http://localhost:8501

---

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Health check |
| GET | `/kpis/risco` | Contagem por risk_classification |
| GET | `/alerts/atraso` | delay_probability > 0.8 |
| GET | `/alerts/comportamento` | driver_behavior_score < 0.5 |
| GET | `/alerts/fadiga_critica` | fatigue_monitoring_score < 0.4 |
| GET | `/alerts/risco_rota` | route_risk_level > 8 |
| GET | `/alerts/porto_congestionado` | port_congestion_level > 8 |
| GET | `/alerts/estoque_baixo` | warehouse_inventory_level < 100 |
| GET | `/alerts/temperatura_da_carga` | iot_temperature > 30 ou < -5 |
| GET | `/alerts/equipamentos_indisponiveis` | handling_equipment_availability < 0.2 |
| GET | `/alerts/atraso_frequente` | AVG delivery_time_deviation > 1 |
| POST | `/inserir/registro` | Insere novo registro + retorna alertas |

---

## Dataset

- **Arquivo:** supply_chain_clean.csv
- **Registros:** 32.065 linhas
- **Colunas:** 27 variáveis
- **Período:** a partir de 2021-01-01
- **Target:** risk_classification (High_Risk / Moderate_Risk / Low_Risk)

---

## Funcionalidades

### Frontend React (porta 5173)
- **Dashboard** — KPIs de risco com contagem por classificação
- **Alertas** — 8 indicadores críticos monitorados em tempo real
- **Simulador** — formulário para simular uma operação e ver alertas disparados
- **Link direto** para o Dashboard Avançado (Streamlit)

### Dashboard Streamlit (porta 8501)
- **Dashboard** — métricas gerais + gráfico de pizza e barras
- **Mapa de Veículos** — posições GPS em mapa 3D colorido por nível de risco
- **Alertas** — resumo quantitativo de todos os alertas ativos
- **Análises** — evolução temporal, box plots por risco, rankings operacionais

---

## Autor

**Murilo Muniz Dias**
[github.com/murilomunizzdias](https://github.com/murilomunizzdias)
