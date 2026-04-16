from fastapi import APIRouter
from api.database import get_conexao

router = APIRouter()

@router.get("/kpis/risco")
def contagem_por_risco():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
    
        cursor = conn.cursor()
        cursor.execute("""
            SELECT risk_classification, COUNT(*) as total
            FROM "SupplyChain"
            GROUP BY risk_classification
        """)
        resultado = cursor.fetchall()
        return {"dados": resultado}
    
    finally:
        conn.close()

@router.get("/kpis/tempo_entrega")
def tempo_medio_entrega():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
                SELECT AVG(lead_time_days)
                FROM "SupplyChain"        
            """
        )
        resultado = cursor.fetchall()
        return {"Tempo_medio_entrega":resultado}
    
    finally: 
        conn.close()

@router.get("/kpis/lead_time_medio")
def lead_time_medio():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexâo"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(lead_time_days)
            FROM "SupplyChain"
        """)
        resultado = cursor.fetchall()
        return {"Tempo_medio_lead":resultado}
    
    finally:
        conn.close()

@router.get("/kpis/shipping_costs")
def custo_transporte():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexâo"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(shipping_costs)
            FROM "SupplyChain"
        """)
        resultado = cursor.fetchall()
        return {"custo_medio_transporte":resultado}
    
    finally:
        conn.close()

@router.get("/kpis/consumo_combustivel")
def consumo_medio_combustivel():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexâo"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(fuel_consumption_rate)
            FROM "SupplyChain"
        """)
        resultado = cursor.fetchall()
        return {"Consumo_medio_combustivel":resultado}
    
    finally:
        conn.close()

@router.get("/kpis/taxa_media_atraso")
def taxa_media_atraso():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexâo"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(delivery_time_deviation)
            FROM "SupplyChain"
        """)
        resultado = cursor.fetchall()
        return {"taxa_media_atraso":resultado}
    
    finally:
        conn.close()

@router.get("/kpis/taxa_fulfillment_pedidos")
def taxa_fulfillment_pedidos():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexâo"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(order_fulfillment_status)
            FROM "SupplyChain"
        """)
        resultado = cursor.fetchall()
        return {"taxa_media_fulfillment":resultado}
    
    finally:
        conn.close()







