from fastapi import APIRouter
from api.database import get_conexao

router = APIRouter()

@router.get("/kpis/risco")
def contagem_por_risco():
    conn = get_conexao()
    if conn is None:
        return {"erro": "Falha na conexão"}
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT risk_classification, COUNT(*) as total
        FROM "SupplyChain"
        GROUP BY risk_classification
    """)
    resultado = cursor.fetchall()
    conn.close()
    
    return {"dados": resultado}

@router.get("/kpis/tempo_entrega")
def tempo_medio_entrega():
    conn=get_conexao()
    if conn is None:
        return {"erro":"Falha na conexão"}
    
    cursor = conn.cursosr()
    cursor.execute("""
            SELECT AVG(lead_time_days)
            FROM "SupplyChain"        
        """
    )
    resultado = cursor.fetchall()
    conn.close()

    return {"Tempo_medio_entrega":resultado}

