import numpy as np
import pandas as pd

FLEET_SPECS = {
    "PS Trillium": {"capacity": 1000, "default_active": True},
    "M/V Sam McBride": {"capacity": 915, "default_active": True},
    "M/V Thomas Rennie": {"capacity": 915, "default_active": True},
    "M/V William Inglis": {"capacity": 600, "default_active": True},
    "M/V Ongiara": {"capacity": 220, "default_active": False}
}

def simulate_fleet_dispatch(hourly_demand, active_vessels, cycle_time_mins=45):
    # Total capacity per departure across all active vessels
    fleet_departure_capacity = sum(
        FLEET_SPECS[v]["capacity"] for v in active_vessels if v in FLEET_SPECS
    )
    if fleet_departure_capacity == 0:
        fleet_departure_capacity = 1
        
    departures_per_vessel_hour = 60.0 / cycle_time_mins
    hourly_fleet_capacity = fleet_departure_capacity * (departures_per_vessel_hour / max(1, len(active_vessels)))
    
    results = []
    backlog = 0
    for demand in hourly_demand:
        net_load = demand + backlog
        transported = min(net_load, hourly_fleet_capacity)
        backlog = max(0, net_load - transported)
        utilization = (transported / hourly_fleet_capacity * 100) if hourly_fleet_capacity > 0 else 0
        required_trips = int(np.ceil(net_load / 800))  # approx 800 pax avg boat
        
        results.append({
            "demand": demand,
            "transported": int(transported),
            "backlog": int(backlog),
            "utilization": round(utilization, 1),
            "required_trips": required_trips,
            "status": "Normal" if backlog == 0 else ("Congested" if backlog < 1500 else "Critical Backlog")
        })
    return pd.DataFrame(results), hourly_fleet_capacity
