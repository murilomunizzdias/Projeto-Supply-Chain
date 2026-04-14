from fastapi import APIRouter
from api.database import get_conexao

router = APIRouter()
@router.get("/alerts/atraso")
def alertas_atraso():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, hour, delay_probability, risk_classification
        FROM "SupplyChain"
        WHERE delay_probability > 0.8
        ORDER BY delay_probability DESC
        LIMIT 50
    """)
    resultado = cursor.fetchall()
    conn.close()
    
    return {"alertas": resultado}

@router.get("/alerts/comportamento")
def alerta_comportamento_motorista():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    cursor=conn.cursor()
    cursor.execute("""
        SELECT date, hour, driver_behavior_score
        FROM "SupplyChain"
        WHERE driver_behavior_score < 0.5
        ORDER BY driver_behavior_score DESC
        LIMIT 50
    
        """
    )
    resultado = cursor.fetchall()
    conn.close()
    return {"alertas_comportamento": resultado}

@router.get("/alerts/atraso_frequente")
def atraso_frequente():
    conn= get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(delivery_time_deviation) as media
        FROM "SupplyChain"
        HAVING AVG(delivery_time_deviation) > 1
        """
    )
    resultado = cursor.fetchall()
    conn.close()
    return{"Média_desvio_entrega ":resultado}


@router.get("/alerts/fadiga_critica")
def fadiga_critica():
    conn= get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    cursor= conn.cursor()
    cursor.execute("""
            SELECT fatigue_monitoring_score
            FROM "SupplyChain"
            WHERE fatigue_monitoring_score> 0.4
    """)
    resultado = cursor.fetchall()
    conn.close()
    return{"Alerta_de_fadiga":resultado}

@router.get("/alerts/risco_rota")
def risco_rota():
    conn= get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    cursor= conn.cursor()
    cursor.execute("""
            SELECT route_risk_level
            FROM "SupplyChain"
            WHERE route_risk_level>8
    """)
    resultado = cursor.fetchall()
    conn.close()
    return{"Alerta_de_rota":resultado}


        
