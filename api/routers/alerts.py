from fastapi import APIRouter
from api.database import get_conexao

router = APIRouter()
@router.get("/alertas/atraso")
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

@router.get("/alertas/comportamento")
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
    return {"alertas": resultado}

    conn.close()