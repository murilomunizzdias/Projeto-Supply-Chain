from pydantic import BaseModel
from fastapi import APIRouter
from api.database import get_conexao
import random
from datetime import datetime

router=APIRouter()


class Registro(BaseModel):
    delay_probability:float
    driver_behavior_score:float
    fatigue_monitoring_score:float
    route_risk_level: str
    port_congestion_level:float
    warehouse_inventory_level:float
    iot_temperature:float
    shipping_costs:float

@router.post("/inserir/registro")
def registro_de_shipping(dados: Registro):
    conn=get_conexao()
    
    if conn is None:
        return{"erro":"Falha na conexão"}
    
    agora = datetime.now()
    data = agora.date()
    hora = agora.strftime("%H:%M:%S")

    if dados.delay_probability > 0.7:
        risco = "High_Risk"
    elif dados.delay_probability > 0.4:
        risco = "Moderate_Risk"
    else:
        risco = "Low_Risk"

    try:
        cursor= conn.cursor()
        cursor.execute("""
        INSERT INTO "SupplyChain" (
            ...
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """, (
        data, hora,
        dados.delay_probability,
        dados.driver_behavior_score,
        dados.fatigue_monitoring_score,
        dados.route_risk_level,
        dados.port_congestion_level,
        dados.warehouse_inventory_level,
        dados.iot_temperature,
        dados.shipping_costs,
        risco,
        round(random.uniform(-2, 10), 2),   # delivery_time_deviation
        round(random.uniform(0, 1), 2),     # disruption_likelihood_score
        round(random.uniform(0.5, 5), 2),   # customs_clearance_time
        round(random.uniform(0, 1), 2),     # cargo_condition_status
        round(random.uniform(100, 10000), 2), # historical_demand
        round(random.uniform(1, 15), 2),    # lead_time_days
        round(random.uniform(0, 1), 2),     # supplier_reliability_score
        round(random.uniform(0, 1), 2),     # weather_condition_severity
        round(random.uniform(0, 1), 2),     # order_fulfillment_status
        round(random.uniform(0, 1), 2),     # handling_equipment_availability
        round(random.uniform(0.5, 5), 2),   # loading_unloading_time
        round(random.uniform(0, 10), 2),    # traffic_congestion_level
        round(random.uniform(-2, 5), 2),    # eta_variation_hours
        round(random.uniform(5, 20), 2),    # fuel_consumption_rate
        round(random.uniform(-120, -70), 6), # vehicle_gps_longitude
        round(random.uniform(30, 50), 6)    # vehicle_gps_latitude
    ))
        conn.commit()
    finally:
        conn.close()



    




