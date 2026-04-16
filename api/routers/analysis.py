from fastapi import APIRouter
from api.database import get_conexao

router = APIRouter()

@router.get("/analysis/correlacao_clima_atraso")
def correlacao_clima_atraso():
    conn=get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor=conn.get.cursor()
        cursor.execute("""
                SELECT CORR(weather_condition_severity,delay_probability)
                FROM "SupplyChain"
        """)
        resultado=cursor.fetchall()
        return{"Correlacao_atraso__clima":resultado}
    finally:
        conn.close()

@router.get("/analysis/correlacao_fadiga_desvio")
def correlacao_fadiga_desvio():
    conn=get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor=conn.get.cursor()
        cursor.execute("""
                SELECT CORR(fatigue_monitoring_score,delivery_time_deviation)
                FROM "SupplyChain"
        """)
        resultado=cursor.fetchall()
        return{"Correlacao_fadiga_desvio":resultado}
    finally:
        conn.close()

@router.get("/analysis/correlacao_congestionamento_porto_lead")
def correlacao_porto_lead():
    conn=get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor=conn.get.cursor()
        cursor.execute("""
                SELECT CORR(port_congestion_level vs lead_time_days)
                FROM "SupplyChain"
        """)
        resultado=cursor.fetchall()
        return{"Correlacao_congestionamento_lead":resultado}
    finally:
        conn.close()

@router.get("/analysis/correlacao_custo_frete_date")
def correlacao_frete_date():
    conn=get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor=conn.get.cursor()
        cursor.execute("""
                SELECT CORR(shipping_costs,date)
                FROM "SupplyChain"
        """)
        resultado=cursor.fetchall()
        return{"Correlacao_frete_date":resultado}
    finally:
        conn.close()

@router.get("/analysis/correlacao_demanda_vs_estoque")
def correlacao_demanda_estoque():
    conn=get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor=conn.get.cursor()
        cursor.execute("""
                SELECT CORR(historical_demand,warehouse_inventory_level)
                FROM "SupplyChain"
        """)
        resultado=cursor.fetchall()
        return{"Correlacao_demanda_estoque":resultado}
    finally:
        conn.close()



