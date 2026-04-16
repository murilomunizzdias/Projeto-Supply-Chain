from fastapi import FastAPI
from api.routers import kpis, alerts, analysis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(kpis.router)
app.include_router(alerts.router)
app.include_router(analysis.router)

@app.get("/")
def inicio():
    return {"mensagem": "API funcionando!"}