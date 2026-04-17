import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API = "http://localhost:8000"

st.set_page_config(
    page_title="Supply Chain — Dashboard",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Space Mono', monospace; background-color: #0b0f1a; color: #e2e8f0; }
    .stApp { background-color: #0b0f1a; }
    section[data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1f2d45; }
    div[data-testid="stMetric"] { background-color: #111827; border: 1px solid #1f2d45; border-radius: 12px; padding: 16px; }
    div[data-testid="stMetric"]:hover { border-color: #00e5ff; }
    div[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 11px !important; }
    div[data-testid="stMetricValue"] { color: #e2e8f0 !important; }
    h1, h2, h3 { color: #00e5ff !important; font-family: 'Space Mono', monospace !important; }
    .block-container { padding: 2rem; }
    .stTabs [data-baseweb="tab-list"] { background-color: #111827; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #64748b; }
    .stTabs [aria-selected="true"] { color: #00e5ff !important; }
</style>
""", unsafe_allow_html=True)

LAYOUT = dict(
    paper_bgcolor="#111827", plot_bgcolor="#111827",
    font_color="#e2e8f0", font_family="Space Mono",
    xaxis=dict(gridcolor="#1f2d45", zerolinecolor="#1f2d45"),
    yaxis=dict(gridcolor="#1f2d45", zerolinecolor="#1f2d45"),
    legend=dict(bgcolor="#111827", bordercolor="#1f2d45", borderwidth=1),
    margin=dict(l=20, r=20, t=40, b=20),
)
COLORS = {"High_Risk": "#ef4444", "Moderate_Risk": "#f59e0b", "Low_Risk": "#10b981"}

@st.cache_data(ttl=30)
def fetch_sql(query):
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "SupplyChain"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "722406")
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return pd.DataFrame()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⬡ SupplyChain")
    st.markdown("**Monitor de Operações**")
    st.markdown("---")
    pagina = st.radio("Navegação", [
        "📊 Dashboard",
        "🗺️ Mapa de Veículos",
        "⚠️ Alertas",
        "📈 Análises",
    ])
    st.markdown("---")
    if st.button("🔄 Atualizar dados"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    try:
        requests.get(f"{API}/", timeout=2)
        st.success("API online")
    except:
        st.error("API offline")
    st.markdown("[🌐 Abrir React](http://localhost:5173)", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "📊 Dashboard":
    st.title("// DASHBOARD")
    st.caption("Visão geral das operações de supply chain")

    df_risco = fetch_sql('SELECT risk_classification, COUNT(*) as total FROM "SupplyChain" GROUP BY risk_classification')

    if not df_risco.empty:
        total   = int(df_risco["total"].sum())
        high    = int(df_risco[df_risco["risk_classification"] == "High_Risk"]["total"].sum())
        mod     = int(df_risco[df_risco["risk_classification"] == "Moderate_Risk"]["total"].sum())
        low     = int(df_risco[df_risco["risk_classification"] == "Low_Risk"]["total"].sum())

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total de Registros", f"{total:,}".replace(",","."))
        c2.metric("High Risk",     f"{high:,}".replace(",","."), f"{round(high/total*100,1)}%")
        c3.metric("Moderate Risk", f"{mod:,}".replace(",","."),  f"{round(mod/total*100,1)}%")
        c4.metric("Low Risk",      f"{low:,}".replace(",","."),  f"{round(low/total*100,1)}%")

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Distribuição de Risco")
            fig = px.pie(df_risco, values="total", names="risk_classification",
                         color="risk_classification", color_discrete_map=COLORS, hole=0.55)
            fig.update_traces(textfont_size=13, textfont_color="#e2e8f0",
                              marker=dict(line=dict(color="#0b0f1a", width=2)))
            fig.update_layout(**LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Contagem por Classificação")
            df_sorted = df_risco.sort_values("total", ascending=True)
            fig2 = px.bar(df_sorted, x="total", y="risk_classification",
                          orientation="h", color="risk_classification",
                          color_discrete_map=COLORS, text="total")
            fig2.update_traces(textfont_size=12, textposition="outside")
            fig2.update_layout(**LAYOUT, showlegend=False,
                               xaxis_title="Quantidade", yaxis_title="")
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("KPIs Operacionais")
    df_kpis = fetch_sql("""
        SELECT
            ROUND(AVG(delay_probability)::numeric, 3)         as avg_delay_prob,
            ROUND(AVG(lead_time_days)::numeric, 2)            as avg_lead_time,
            ROUND(AVG(shipping_costs)::numeric, 2)            as avg_shipping,
            ROUND(AVG(fuel_consumption_rate)::numeric, 2)     as avg_fuel,
            ROUND(AVG(port_congestion_level)::numeric, 2)     as avg_port,
            ROUND(AVG(driver_behavior_score)::numeric, 3)     as avg_driver,
            ROUND(AVG(fatigue_monitoring_score)::numeric, 3)  as avg_fatigue,
            ROUND(AVG(warehouse_inventory_level)::numeric, 1) as avg_stock
        FROM "SupplyChain"
    """)
    if not df_kpis.empty:
        row = df_kpis.iloc[0]
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Prob. Media de Atraso",  str(row["avg_delay_prob"]))
        k2.metric("Lead Time Medio (dias)", str(row["avg_lead_time"]))
        k3.metric("Custo Medio de Frete",   f"R$ {row['avg_shipping']}")
        k4.metric("Consumo Combustivel",    str(row["avg_fuel"]))
        k5,k6,k7,k8 = st.columns(4)
        k5.metric("Congestionamento Porto", f"{row['avg_port']}/10")
        k6.metric("Score Motorista",        str(row["avg_driver"]))
        k7.metric("Score Fadiga",           str(row["avg_fatigue"]))
        k8.metric("Estoque Medio",          str(row["avg_stock"]))


# ══════════════════════════════════════════════════════════════════════════════
# MAPA
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🗺️ Mapa de Veículos":
    st.title("// MAPA DE VEÍCULOS")
    st.caption("Posições e nível de risco por localização")

    col_f1, col_f2 = st.columns([2,1])
    with col_f1:
        n_veiculos = st.slider("Quantidade de pontos", 100, 5000, 1500, 100)
    with col_f2:
        filtro_risco = st.selectbox("Filtrar por risco", ["Todos","High_Risk","Moderate_Risk","Low_Risk"])

    where = f"WHERE risk_classification = '{filtro_risco}'" if filtro_risco != "Todos" else ""
    df_map = fetch_sql(f"""
        SELECT vehicle_gps_latitude as lat, vehicle_gps_longitude as lon,
               risk_classification, delay_probability,
               driver_behavior_score, route_risk_level, date
        FROM "SupplyChain" {where}
        ORDER BY RANDOM() LIMIT {n_veiculos}
    """)

    if not df_map.empty:
        color_map = {"High_Risk":[239,68,68,200], "Moderate_Risk":[245,158,11,200], "Low_Risk":[16,185,129,200]}
        df_map["cor"] = df_map["risk_classification"].map(color_map)
        df_map["cor"] = df_map["cor"].apply(lambda x: x if isinstance(x, list) else [100,100,100,150])

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Pontos exibidos", len(df_map))
        m2.metric("High Risk",    len(df_map[df_map["risk_classification"]=="High_Risk"]))
        m3.metric("Moderate Risk",len(df_map[df_map["risk_classification"]=="Moderate_Risk"]))
        m4.metric("Low Risk",     len(df_map[df_map["risk_classification"]=="Low_Risk"]))

        layer = pdk.Layer("ScatterplotLayer", data=df_map,
            get_position=["lon","lat"], get_color="cor",
            get_radius=35000, pickable=True, opacity=0.85)
        view = pdk.ViewState(latitude=df_map["lat"].mean(), longitude=df_map["lon"].mean(), zoom=3, pitch=40)
        deck = pdk.Deck(layers=[layer], initial_view_state=view,
            tooltip={"html":
                "<b>Risco:</b> {risk_classification}<br/>"
                "<b>Prob. Atraso:</b> {delay_probability}<br/>"
                "<b>Score Motorista:</b> {driver_behavior_score}<br/>"
                "<b>Risco Rota:</b> {route_risk_level}",
                "style":{"backgroundColor":"#111827","color":"#e2e8f0","fontSize":"12px"}},
            map_style="mapbox://styles/mapbox/dark-v10")
        st.pydeck_chart(deck)
        st.caption("🔴 High Risk  |  🟡 Moderate Risk  |  🟢 Low Risk")


# ══════════════════════════════════════════════════════════════════════════════
# ALERTAS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "⚠️ Alertas":
    st.title("// ALERTAS")
    st.caption("Monitoramento de indicadores críticos")

    df_alertas = fetch_sql("""
        SELECT
            COUNT(*) FILTER (WHERE delay_probability > 0.8)               as atraso_critico,
            COUNT(*) FILTER (WHERE driver_behavior_score < 0.5)           as comportamento,
            COUNT(*) FILTER (WHERE fatigue_monitoring_score < 0.4)        as fadiga,
            COUNT(*) FILTER (WHERE route_risk_level > 8)                  as risco_rota,
            COUNT(*) FILTER (WHERE port_congestion_level > 8)             as porto,
            COUNT(*) FILTER (WHERE warehouse_inventory_level < 100)       as estoque,
            COUNT(*) FILTER (WHERE iot_temperature > 30 OR iot_temperature < -5) as temperatura,
            COUNT(*) FILTER (WHERE handling_equipment_availability < 0.2) as equipamentos
        FROM "SupplyChain"
    """)

    if not df_alertas.empty:
        row = df_alertas.iloc[0]
        a1,a2,a3,a4 = st.columns(4)
        a1.metric("Atraso Critico",  int(row["atraso_critico"]))
        a2.metric("Comportamento",   int(row["comportamento"]))
        a3.metric("Fadiga Critica",  int(row["fadiga"]))
        a4.metric("Risco de Rota",   int(row["risco_rota"]))
        a5,a6,a7,a8 = st.columns(4)
        a5.metric("Porto Congestionado",    int(row["porto"]))
        a6.metric("Estoque Baixo",          int(row["estoque"]))
        a7.metric("Temperatura da Carga",   int(row["temperatura"]))
        a8.metric("Equipamentos Indispon.", int(row["equipamentos"]))

        st.markdown("---")
        df_bar = pd.DataFrame({
            "Alerta": ["Atraso Critico","Comportamento","Fadiga","Risco Rota",
                       "Porto","Estoque","Temperatura","Equipamentos"],
            "Quantidade": [int(row["atraso_critico"]), int(row["comportamento"]),
                           int(row["fadiga"]), int(row["risco_rota"]),
                           int(row["porto"]), int(row["estoque"]),
                           int(row["temperatura"]), int(row["equipamentos"])]
        }).sort_values("Quantidade", ascending=True)

        fig = px.bar(df_bar, x="Quantidade", y="Alerta", orientation="h",
                     color="Quantidade",
                     color_continuous_scale=["#10b981","#f59e0b","#ef4444"],
                     text="Quantidade")
        fig.update_traces(textfont_size=12, textposition="outside")
        fig.update_layout(**LAYOUT, coloraxis_showscale=False,
                          xaxis_title="Registros", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Top 20 — Maior Probabilidade de Atraso")
        df_top = fetch_sql("""
            SELECT date, hour, ROUND(delay_probability::numeric,3) as delay_probability,
                   risk_classification,
                   ROUND(driver_behavior_score::numeric,3) as driver_behavior_score,
                   ROUND(route_risk_level::numeric,2) as route_risk_level
            FROM "SupplyChain"
            WHERE delay_probability > 0.8
            ORDER BY delay_probability DESC LIMIT 20
        """)
        if not df_top.empty:
            st.dataframe(df_top, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ANÁLISES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📈 Análises":
    st.title("// ANÁLISES")
    st.caption("Tendências e distribuições do dataset")

    tab1, tab2, tab3 = st.tabs(["📅 Evolução Temporal", "📦 Distribuições", "🏆 Rankings"])

    with tab1:
        st.subheader("Evolução do Risco e Custo ao Longo do Tempo")
        df_time = fetch_sql("""
            SELECT date,
                ROUND(AVG(delay_probability)::numeric,3)  as avg_delay,
                ROUND(AVG(route_risk_level)::numeric,2)   as avg_route_risk,
                ROUND(AVG(shipping_costs)::numeric,2)     as avg_cost,
                COUNT(*) FILTER (WHERE risk_classification='High_Risk') as high_count,
                COUNT(*) FILTER (WHERE risk_classification='Low_Risk')  as low_count
            FROM "SupplyChain"
            GROUP BY date ORDER BY date
        """)
        if not df_time.empty:
            df_time["date"] = pd.to_datetime(df_time["date"])

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_time["date"], y=df_time["avg_delay"],
                name="Prob. Atraso Média", line=dict(color="#ef4444", width=2), fill="tozeroy",
                fillcolor="rgba(239,68,68,0.08)"))
            fig.add_trace(go.Scatter(x=df_time["date"], y=df_time["avg_route_risk"]/10,
                name="Risco Rota (norm.)", line=dict(color="#f59e0b", width=2, dash="dot")))
            fig.update_layout(**LAYOUT, title="Probabilidade de Atraso e Risco de Rota")
            st.plotly_chart(fig, use_container_width=True)

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df_time["date"], y=df_time["avg_cost"],
                name="Custo Médio", line=dict(color="#00e5ff", width=2), fill="tozeroy",
                fillcolor="rgba(0,229,255,0.06)"))
            fig2.update_layout(**LAYOUT, title="Evolução do Custo de Frete",
                               yaxis_title="R$")
            st.plotly_chart(fig2, use_container_width=True)

            fig3 = go.Figure()
            fig3.add_trace(go.Bar(x=df_time["date"], y=df_time["high_count"],
                name="High Risk", marker_color="#ef4444", opacity=0.8))
            fig3.add_trace(go.Bar(x=df_time["date"], y=df_time["low_count"],
                name="Low Risk", marker_color="#10b981", opacity=0.8))
            fig3.update_layout(**LAYOUT, barmode="group",
                               title="Contagem Diária: High Risk vs Low Risk")
            st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("Distribuição de Variáveis por Nível de Risco")
        variavel = st.selectbox("Escolha a variável", [
            "delay_probability", "driver_behavior_score", "fatigue_monitoring_score",
            "route_risk_level", "shipping_costs", "lead_time_days",
            "port_congestion_level", "warehouse_inventory_level",
            "fuel_consumption_rate", "eta_variation_hours"
        ])
        df_hist = fetch_sql(f"""
            SELECT {variavel}, risk_classification
            FROM "SupplyChain"
            ORDER BY RANDOM() LIMIT 8000
        """)
        if not df_hist.empty:
            # Box plot — muito mais informativo que scatter para dados aleatórios
            fig = px.box(df_hist, x="risk_classification", y=variavel,
                         color="risk_classification", color_discrete_map=COLORS,
                         points=False,
                         labels={"risk_classification": "Classificação de Risco",
                                 variavel: variavel.replace("_", " ").title()})
            fig.update_layout(**LAYOUT, showlegend=False,
                              title=f"Distribuição de {variavel.replace('_',' ').title()} por Risco")
            st.plotly_chart(fig, use_container_width=True)

            # Histograma por grupo
            fig2 = px.histogram(df_hist, x=variavel, color="risk_classification",
                                color_discrete_map=COLORS, nbins=40,
                                barmode="overlay", opacity=0.65,
                                labels={variavel: variavel.replace("_"," ").title()})
            fig2.update_layout(**LAYOUT, title="Histograma por Classificação de Risco",
                               yaxis_title="Frequência")
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Rankings Operacionais")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top 10 — Maior Custo de Frete**")
            df_rank1 = fetch_sql("""
                SELECT date, hour,
                       ROUND(shipping_costs::numeric,2) as custo_frete,
                       risk_classification,
                       ROUND(delay_probability::numeric,3) as prob_atraso
                FROM "SupplyChain"
                ORDER BY shipping_costs DESC LIMIT 10
            """)
            if not df_rank1.empty:
                fig = px.bar(df_rank1, x="custo_frete",
                             y=df_rank1.index.astype(str),
                             orientation="h", color="risk_classification",
                             color_discrete_map=COLORS, text="custo_frete")
                fig.update_layout(**LAYOUT, showlegend=False,
                                  xaxis_title="R$", yaxis_title="",
                                  title="Maiores Custos")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Média de Indicadores por Risco**")
            df_rank2 = fetch_sql("""
                SELECT risk_classification,
                    ROUND(AVG(delay_probability)::numeric,3)        as avg_atraso,
                    ROUND(AVG(shipping_costs)::numeric,2)           as avg_custo,
                    ROUND(AVG(lead_time_days)::numeric,2)           as avg_lead_time,
                    ROUND(AVG(fatigue_monitoring_score)::numeric,3) as avg_fadiga
                FROM "SupplyChain"
                GROUP BY risk_classification
            """)
            if not df_rank2.empty:
                fig = px.bar(df_rank2, x="risk_classification",
                             y=["avg_atraso","avg_fadiga"],
                             barmode="group", color_discrete_map={
                                 "avg_atraso":"#ef4444",
                                 "avg_fadiga":"#00e5ff"
                             },
                             labels={"value":"Média","variable":"Indicador",
                                     "risk_classification":"Risco"})
                fig.update_layout(**LAYOUT,
                                  title="Prob. Atraso vs Fadiga por Nível de Risco")
                st.plotly_chart(fig, use_container_width=True)