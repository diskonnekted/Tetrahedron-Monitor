from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple
import json
import math
import random
import uuid
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import numpy as np

# Environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "tetracore_db")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app = FastAPI(title="Tetracore Server Simulation", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Models
class Vector3D(BaseModel):
    x: float
    y: float
    z: float

class TetrahedronVertex(BaseModel):
    position: Vector3D
    energy: float = 0.0
    spin: float = 0.0
    mass_projection: float = 1.0

class Tetrahedron(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vertices: List[TetrahedronVertex]
    center: Vector3D
    energy_state: float = 1.0
    oscillation_frequency: float = 1.0
    phase: float = 0.0
    particle_type: str = "matter"  # "matter" or "antimatter"
    
class TetrahedronPair(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    matter_tetrahedron: Tetrahedron
    antimatter_tetrahedron: Tetrahedron
    stability_factor: float = 1.0
    pairing_strength: float = 1.0
    entanglement_connection: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

class SimulationState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pairs: List[TetrahedronPair] = []
    total_stability: float = 0.0
    system_energy: float = 0.0
    time_step: float = 0.0
    running: bool = False

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Tetracore Physics Engine
class TetracoreEngine:
    def __init__(self):
        self.simulation_state = SimulationState()
        
    def create_regular_tetrahedron(self, center: Vector3D, size: float = 1.0) -> List[TetrahedronVertex]:
        """Create vertices for a regular tetrahedron centered at given position"""
        # Regular tetrahedron vertices in unit form
        vertices_coords = [
            (1, 1, 1),
            (1, -1, -1),
            (-1, 1, -1),
            (-1, -1, 1)
        ]
        
        vertices = []
        for x, y, z in vertices_coords:
            position = Vector3D(
                x=center.x + x * size / math.sqrt(3),
                y=center.y + y * size / math.sqrt(3),
                z=center.z + z * size / math.sqrt(3)
            )
            vertex = TetrahedronVertex(
                position=position,
                energy=random.uniform(0.5, 1.5),
                spin=random.uniform(-1, 1),
                mass_projection=random.uniform(0.8, 1.2)
            )
            vertices.append(vertex)
        
        return vertices
    
    def create_counter_tetrahedron(self, original: Tetrahedron) -> Tetrahedron:
        """Create a counter-tetrahedron (antimatter pair) for stabilization"""
        # Mirror the tetrahedron across its center with inverted properties
        counter_vertices = []
        
        for vertex in original.vertices:
            # Mirror position relative to center
            mirrored_pos = Vector3D(
                x=2 * original.center.x - vertex.position.x,
                y=2 * original.center.y - vertex.position.y,
                z=2 * original.center.z - vertex.position.z
            )
            
            # Invert quantum properties for antimatter
            counter_vertex = TetrahedronVertex(
                position=mirrored_pos,
                energy=-vertex.energy,  # Inverted energy
                spin=-vertex.spin,      # Inverted spin
                mass_projection=vertex.mass_projection  # Mass remains same magnitude
            )
            counter_vertices.append(counter_vertex)
        
        counter_tetrahedron = Tetrahedron(
            vertices=counter_vertices,
            center=Vector3D(
                x=2 * original.center.x - original.center.x,
                y=2 * original.center.y - original.center.y, 
                z=2 * original.center.z - original.center.z
            ),
            energy_state=-original.energy_state,
            oscillation_frequency=original.oscillation_frequency,
            phase=original.phase + math.pi,  # Phase shifted for antimatter
            particle_type="antimatter"
        )
        
        return counter_tetrahedron
    
    def calculate_pair_stability(self, pair: TetrahedronPair) -> float:
        """Calculate stability factor for a tetrahedron pair"""
        matter = pair.matter_tetrahedron
        antimatter = pair.antimatter_tetrahedron
        
        # Distance between centers
        dx = matter.center.x - antimatter.center.x
        dy = matter.center.y - antimatter.center.y
        dz = matter.center.z - antimatter.center.z
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # Optimal distance for stability (arbitrary physics model)
        optimal_distance = 2.0
        distance_factor = 1.0 / (1.0 + abs(distance - optimal_distance))
        
        # Energy balance factor
        energy_balance = 1.0 - abs(matter.energy_state + antimatter.energy_state) / 2.0
        
        # Phase synchronization factor  
        phase_sync = (1.0 + math.cos(matter.phase - antimatter.phase)) / 2.0
        
        # Overall stability
        stability = distance_factor * energy_balance * phase_sync * pair.pairing_strength
        
        return max(0.0, min(1.0, stability))
    
    def update_oscillations(self, dt: float):
        """Update tetrahedron oscillations based on time step"""
        for pair in self.simulation_state.pairs:
            # Update matter tetrahedron
            matter = pair.matter_tetrahedron
            matter.phase += matter.oscillation_frequency * dt
            matter.energy_state = 1.0 + 0.3 * math.sin(matter.phase)
            
            # Update antimatter tetrahedron (synchronized but inverted)
            antimatter = pair.antimatter_tetrahedron
            antimatter.phase += antimatter.oscillation_frequency * dt
            antimatter.energy_state = -(1.0 + 0.3 * math.sin(antimatter.phase))
            
            # Update pair stability
            pair.stability_factor = self.calculate_pair_stability(pair)
    
    def create_tetrahedron_pair(self, center: Vector3D, separation: float = 2.0) -> TetrahedronPair:
        """Create a new matter-antimatter tetrahedron pair"""
        # Create matter tetrahedron
        matter_center = Vector3D(
            x=center.x - separation/2,
            y=center.y,
            z=center.z
        )
        matter_vertices = self.create_regular_tetrahedron(matter_center)
        matter_tetrahedron = Tetrahedron(
            vertices=matter_vertices,
            center=matter_center,
            energy_state=1.0,
            oscillation_frequency=random.uniform(0.5, 2.0),
            phase=random.uniform(0, 2*math.pi),
            particle_type="matter"
        )
        
        # Create antimatter tetrahedron
        antimatter_center = Vector3D(
            x=center.x + separation/2,
            y=center.y,
            z=center.z
        )
        antimatter_vertices = self.create_regular_tetrahedron(antimatter_center)
        antimatter_tetrahedron = Tetrahedron(
            vertices=antimatter_vertices,
            center=antimatter_center,
            energy_state=-1.0,
            oscillation_frequency=matter_tetrahedron.oscillation_frequency,
            phase=matter_tetrahedron.phase + math.pi,
            particle_type="antimatter"
        )
        
        # Create pair
        pair = TetrahedronPair(
            matter_tetrahedron=matter_tetrahedron,
            antimatter_tetrahedron=antimatter_tetrahedron,
            pairing_strength=random.uniform(0.7, 1.0),
            entanglement_connection=True
        )
        
        pair.stability_factor = self.calculate_pair_stability(pair)
        return pair
    
    def calculate_system_metrics(self):
        """Calculate overall system stability and energy"""
        if not self.simulation_state.pairs:
            self.simulation_state.total_stability = 0.0
            self.simulation_state.system_energy = 0.0
            return
            
        total_stability = sum(pair.stability_factor for pair in self.simulation_state.pairs)
        self.simulation_state.total_stability = total_stability / len(self.simulation_state.pairs)
        
        total_energy = sum(
            abs(pair.matter_tetrahedron.energy_state) + abs(pair.antimatter_tetrahedron.energy_state)
            for pair in self.simulation_state.pairs
        )
        self.simulation_state.system_energy = total_energy

# Global engine instance
engine = TetracoreEngine()

# API Endpoints
@app.get("/api/status")
async def get_status():
    return {"status": "Tetracore Server Running", "version": "1.0.0"}

@app.get("/api/simulation/state")
async def get_simulation_state():
    engine.calculate_system_metrics()
    return engine.simulation_state

@app.post("/api/simulation/start")
async def start_simulation():
    engine.simulation_state.running = True
    return {"message": "Simulation started", "running": True}

@app.post("/api/simulation/stop")
async def stop_simulation():
    engine.simulation_state.running = False
    return {"message": "Simulation stopped", "running": False}

@app.post("/api/simulation/reset")
async def reset_simulation():
    engine.simulation_state = SimulationState()
    return {"message": "Simulation reset"}

@app.post("/api/pairs/create")
async def create_pair(center_x: float = 0, center_y: float = 0, center_z: float = 0, separation: float = 2.0):
    center = Vector3D(x=center_x, y=center_y, z=center_z)
    pair = engine.create_tetrahedron_pair(center, separation)
    engine.simulation_state.pairs.append(pair)
    
    # Save to database
    try:
        await db.tetrahedron_pairs.insert_one(pair.model_dump())
    except Exception as e:
        print(f"Database error: {e}")
    
    return {"message": "Tetrahedron pair created", "pair_id": pair.id}

@app.delete("/api/pairs/{pair_id}")
async def delete_pair(pair_id: str):
    engine.simulation_state.pairs = [p for p in engine.simulation_state.pairs if p.id != pair_id]
    
    # Remove from database
    try:
        await db.tetrahedron_pairs.delete_one({"id": pair_id})
    except Exception as e:
        print(f"Database error: {e}")
    
    return {"message": "Tetrahedron pair deleted"}

@app.get("/api/pairs")
async def get_all_pairs():
    return {"pairs": engine.simulation_state.pairs}

@app.get("/api/pairs/{pair_id}")
async def get_pair(pair_id: str):
    pair = next((p for p in engine.simulation_state.pairs if p.id == pair_id), None)
    if not pair:
        raise HTTPException(status_code=404, detail="Pair not found")
    return pair

# WebSocket endpoint for real-time updates
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            if engine.simulation_state.running:
                # Update simulation
                engine.update_oscillations(0.1)
                engine.calculate_system_metrics()
                engine.simulation_state.time_step += 0.1
                
                # Broadcast update
                await manager.broadcast(engine.simulation_state.model_dump_json())
            
            await asyncio.sleep(0.1)  # 10 FPS update rate
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)