from fastapi import FastAPI
from api.routers import kpis, alerts, analysis

app = FastAPI()

app.include_router(kpis.router)
app.include_router(alerts.router)
app.include_router(analysis.router)

@app.get("/")
def inicio():
    return {"mensagem": "API funcionando!"}