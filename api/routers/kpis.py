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