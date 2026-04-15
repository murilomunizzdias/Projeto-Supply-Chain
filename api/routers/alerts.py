from fastapi import APIRouter
from api.database import get_conexao

router = APIRouter()

@router.get("/alerts/atraso")
def alertas_atraso():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, hour, delay_probability, risk_classification
            FROM "SupplyChain"
            WHERE delay_probability > 0.8
            ORDER BY delay_probability DESC
            LIMIT 50
        """)
        resultado = cursor.fetchall()
        return {"alertas": resultado}
    finally:
        conn.close()


@router.get("/alerts/comportamento")
def alerta_comportamento_motorista():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, hour, driver_behavior_score
            FROM "SupplyChain"
            WHERE driver_behavior_score < 0.5
            ORDER BY driver_behavior_score DESC
            LIMIT 50
        """)
        resultado = cursor.fetchall()
        return {"alertas_comportamento": resultado}
    finally:
        conn.close()


@router.get("/alerts/atraso_frequente")
def atraso_frequente():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(delivery_time_deviation) as media
            FROM "SupplyChain"
        """)
        resultado = cursor.fetchone()
        media = resultado[0] if resultado and resultado[0] is not None else 0
        
        if media > 1:
            return {"Media_desvio_entrega": media, "alerta": True}
        else:
            return {"Media_desvio_entrega": media, "alerta": False}
    finally:
        conn.close()


@router.get("/alerts/fadiga_critica")
def fadiga_critica():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fatigue_monitoring_score
            FROM "SupplyChain"
            WHERE fatigue_monitoring_score < 0.4
        """)
        resultado = cursor.fetchall()
        return {"Alerta_de_fadiga": resultado}
    finally:
        conn.close()


@router.get("/alerts/risco_rota")
def risco_rota():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT route_risk_level
            FROM "SupplyChain"
            WHERE route_risk_level > 8
        """)
        resultado = cursor.fetchall()
        return {"Alerta_de_rota": resultado}
    finally:
        conn.close()


@router.get("/alerts/porto_congestionado")
def porto_congestionado():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT port_congestion_level
            FROM "SupplyChain"
            WHERE port_congestion_level > 8
        """)
        resultado = cursor.fetchall()
        return {"Alerta_de_congestionamento": resultado}
    finally:
        conn.close()


@router.get("/alerts/estoque_baixo")
def estoque_baixo():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT warehouse_inventory_level
            FROM "SupplyChain"
            WHERE warehouse_inventory_level < 100
        """)
        resultado = cursor.fetchall()
        return {"Alerta_de_estoque": resultado}
    finally:
        conn.close()


@router.get("/alerts/temperatura_da_carga")
def temperatura_da_carga():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT iot_temperature
            FROM "SupplyChain"
            WHERE iot_temperature > 30 OR iot_temperature < -5   
        """)
        resultado = cursor.fetchall()
        return {"Alerta_de_temperatura": resultado}
    finally:
        conn.close()


@router.get("/alerts/equipamentos_indisponiveis")
def equipamentos_indisponiveis():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT handling_equipment_availability
            FROM "SupplyChain"
            WHERE handling_equipment_availability < 0.2  
        """)
        resultado = cursor.fetchall()
        return {"Alerta_de_equipamentos": resultado}
    finally:
        conn.close()
        
