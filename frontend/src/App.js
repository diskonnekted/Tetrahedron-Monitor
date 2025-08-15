import React, { useState, useEffect, useRef } from 'react';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { Progress } from './components/ui/progress';
import { Separator } from './components/ui/separator';
import { Alert, AlertDescription } from './components/ui/alert';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Plus, 
  Trash2, 
  Atom, 
  Zap, 
  Activity,
  Eye,
  Settings,
  Info
} from 'lucide-react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [simulationState, setSimulationState] = useState({
    pairs: [],
    total_stability: 0,
    system_energy: 0,
    time_step: 0,
    running: false
  });
  const [isConnected, setIsConnected] = useState(false);
  const [selectedPair, setSelectedPair] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const wsRef = useRef(null);
  const canvasRef = useRef(null);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const connectWebSocket = () => {
      const wsUrl = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://') + '/api/ws';
      wsRef.current = new WebSocket(wsUrl);
      
      wsRef.current.onopen = () => {
        setIsConnected(true);
        console.log('WebSocket connected');
      };
      
      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setSimulationState(data);
      };
      
      wsRef.current.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket disconnected');
        // Reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };
      
      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Initial data fetch
  useEffect(() => {
    fetchSimulationState();
  }, []);

  const fetchSimulationState = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/simulation/state`);
      const data = await response.json();
      setSimulationState(data);
    } catch (error) {
      console.error('Error fetching simulation state:', error);
    }
  };

  const startSimulation = async () => {
    try {
      await fetch(`${BACKEND_URL}/api/simulation/start`, { method: 'POST' });
      // Refresh state to show updated running status
      await fetchSimulationState();
    } catch (error) {
      console.error('Error starting simulation:', error);
    }
  };

  const stopSimulation = async () => {
    try {
      await fetch(`${BACKEND_URL}/api/simulation/stop`, { method: 'POST' });
      // Refresh state to show updated running status
      await fetchSimulationState();
    } catch (error) {
      console.error('Error stopping simulation:', error);
    }
  };

  const resetSimulation = async () => {
    try {
      await fetch(`${BACKEND_URL}/api/simulation/reset`, { method: 'POST' });
      fetchSimulationState();
    } catch (error) {
      console.error('Error resetting simulation:', error);
    }
  };

  const createPair = async () => {
    try {
      const randomX = (Math.random() - 0.5) * 10;
      const randomY = (Math.random() - 0.5) * 10;
      const randomZ = (Math.random() - 0.5) * 10;
      
      await fetch(`${BACKEND_URL}/api/pairs/create?center_x=${randomX}&center_y=${randomY}&center_z=${randomZ}&separation=2.5`, { 
        method: 'POST' 
      });
      
      // Refresh state immediately after creating pair
      await fetchSimulationState();
    } catch (error) {
      console.error('Error creating pair:', error);
    }
  };

  const deletePair = async (pairId) => {
    try {
      await fetch(`${BACKEND_URL}/api/pairs/${pairId}`, { method: 'DELETE' });
      if (selectedPair && selectedPair.id === pairId) {
        setSelectedPair(null);
      }
    } catch (error) {
      console.error('Error deleting pair:', error);
    }
  };

  // 3D Visualization Component
  const TetrahedronVisualization = ({ pair, isSelected, onClick }) => {
    const matter = pair.matter_tetrahedron;
    const antimatter = pair.antimatter_tetrahedron;
    
    const getParticleColor = (type, energy) => {
      if (type === 'matter') {
        return energy > 0 ? 'bg-blue-500' : 'bg-blue-300';
      } else {
        return energy < 0 ? 'bg-red-500' : 'bg-red-300';
      }
    };

    const getStabilityColor = (stability) => {
      if (stability > 0.8) return 'text-green-500';
      if (stability > 0.5) return 'text-yellow-500';
      return 'text-red-500';
    };

    return (
      <div 
        className={`relative p-4 rounded-lg border-2 transition-all duration-300 cursor-pointer hover:shadow-lg ${
          isSelected ? 'border-purple-500 shadow-purple-500/20' : 'border-gray-300 hover:border-gray-400'
        }`}
        onClick={() => onClick(pair)}
      >
        {/* Connection Line */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-0.5 w-20 bg-gradient-to-r from-blue-500 to-red-500 opacity-60"></div>
        </div>
        
        {/* Matter Tetrahedron */}
        <div className="flex justify-between items-center">
          <div className="flex flex-col items-center space-y-2">
            <div className={`w-8 h-8 rounded-full ${getParticleColor('matter', matter.energy_state)} animate-pulse`}>
              <div className="w-full h-full flex items-center justify-center">
                <Atom className="w-4 h-4 text-white" />
              </div>
            </div>
            <Badge variant="outline" className="text-xs">Matter</Badge>
            <span className="text-xs text-gray-600">E: {matter.energy_state.toFixed(2)}</span>
          </div>
          
          {/* Center Info */}
          <div className="flex flex-col items-center space-y-1">
            <Badge className={`${getStabilityColor(pair.stability_factor)}`}>
              {(pair.stability_factor * 100).toFixed(0)}%
            </Badge>
            <div className="text-xs text-gray-500">Stability</div>
            {pair.entanglement_connection && (
              <Zap className="w-3 h-3 text-purple-500 animate-pulse" />
            )}
          </div>
          
          {/* Antimatter Tetrahedron */}
          <div className="flex flex-col items-center space-y-2">
            <div className={`w-8 h-8 rounded-full ${getParticleColor('antimatter', antimatter.energy_state)} animate-pulse`}>
              <div className="w-full h-full flex items-center justify-center">
                <Atom className="w-4 h-4 text-white transform rotate-180" />
              </div>
            </div>
            <Badge variant="outline" className="text-xs">Antimatter</Badge>
            <span className="text-xs text-gray-600">E: {antimatter.energy_state.toFixed(2)}</span>
          </div>
        </div>
        
        {/* Pair ID */}
        <div className="text-xs text-gray-400 mt-2 text-center">
          ID: {pair.id.substring(0, 8)}...
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Atom className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Tetracore Server</h1>
                <p className="text-sm text-gray-600">Counter-Tetrahedron Pairing System</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Badge variant={isConnected ? "default" : "destructive"}>
                {isConnected ? "Connected" : "Disconnected"}
              </Badge>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowDetails(!showDetails)}
              >
                <Info className="w-4 h-4 mr-2" />
                Details
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Control Panel */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="flex items-center space-x-2">
                <Settings className="w-5 h-5" />
                <span>Simulation Controls</span>
              </CardTitle>
              <div className="flex space-x-2">
                <Button
                  onClick={simulationState.running ? stopSimulation : startSimulation}
                  variant={simulationState.running ? "destructive" : "default"}
                  size="sm"
                >
                  {simulationState.running ? (
                    <>
                      <Pause className="w-4 h-4 mr-2" />
                      Stop
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 mr-2" />
                      Start
                    </>
                  )}
                </Button>
                <Button onClick={resetSimulation} variant="outline" size="sm">
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Reset
                </Button>
                <Button onClick={createPair} variant="outline" size="sm">
                  <Plus className="w-4 h-4 mr-2" />
                  Create Pair
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{simulationState.pairs.length}</div>
                <div className="text-sm text-gray-600">Active Pairs</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {(simulationState.total_stability * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-gray-600">System Stability</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {simulationState.system_energy.toFixed(2)}
                </div>
                <div className="text-sm text-gray-600">System Energy</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {simulationState.time_step.toFixed(1)}s
                </div>
                <div className="text-sm text-gray-600">Time Step</div>
              </div>
            </div>
            
            <Separator className="my-4" />
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Overall System Stability</span>
                <span>{(simulationState.total_stability * 100).toFixed(1)}%</span>
              </div>
              <Progress value={simulationState.total_stability * 100} className="h-2" />
            </div>
          </CardContent>
        </Card>

        {/* Tetrahedron Pairs Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Eye className="w-5 h-5" />
                  <span>Tetrahedron Pairs Visualization</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {simulationState.pairs.length === 0 ? (
                  <Alert>
                    <Info className="h-4 w-4" />
                    <AlertDescription>
                      No tetrahedron pairs exist. Create your first pair to begin the simulation.
                    </AlertDescription>
                  </Alert>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {simulationState.pairs.map((pair) => (
                      <div key={pair.id} className="relative">
                        <TetrahedronVisualization
                          pair={pair}
                          isSelected={selectedPair && selectedPair.id === pair.id}
                          onClick={setSelectedPair}
                        />
                        <Button
                          variant="destructive"
                          size="sm"
                          className="absolute -top-2 -right-2 w-6 h-6 p-0"
                          onClick={(e) => {
                            e.stopPropagation();
                            deletePair(pair.id);
                          }}
                        >
                          <Trash2 className="w-3 h-3" />
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Pair Details Panel */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="w-5 h-5" />
                  <span>Pair Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {selectedPair ? (
                  <div className="space-y-4">
                    <div>
                      <h3 className="font-semibold text-lg mb-2">Pair {selectedPair.id.substring(0, 8)}</h3>
                      <Badge className={
                        selectedPair.stability_factor > 0.8 ? "bg-green-500" :
                        selectedPair.stability_factor > 0.5 ? "bg-yellow-500" : "bg-red-500"
                      }>
                        Stability: {(selectedPair.stability_factor * 100).toFixed(1)}%
                      </Badge>
                    </div>
                    
                    <Separator />
                    
                    <div className="space-y-3">
                      <div>
                        <h4 className="font-medium text-blue-600 mb-1">Matter Tetrahedron</h4>
                        <div className="text-sm space-y-1">
                          <div>Energy State: {selectedPair.matter_tetrahedron.energy_state.toFixed(3)}</div>
                          <div>Frequency: {selectedPair.matter_tetrahedron.oscillation_frequency.toFixed(2)} Hz</div>
                          <div>Phase: {selectedPair.matter_tetrahedron.phase.toFixed(2)} rad</div>
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="font-medium text-red-600 mb-1">Antimatter Tetrahedron</h4>
                        <div className="text-sm space-y-1">
                          <div>Energy State: {selectedPair.antimatter_tetrahedron.energy_state.toFixed(3)}</div>
                          <div>Frequency: {selectedPair.antimatter_tetrahedron.oscillation_frequency.toFixed(2)} Hz</div>
                          <div>Phase: {selectedPair.antimatter_tetrahedron.phase.toFixed(2)} rad</div>
                        </div>
                      </div>
                    </div>
                    
                    <Separator />
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Pairing Strength</span>
                        <span>{(selectedPair.pairing_strength * 100).toFixed(0)}%</span>
                      </div>
                      <Progress value={selectedPair.pairing_strength * 100} className="h-2" />
                      
                      <div className="flex justify-between text-sm">
                        <span>Entanglement</span>
                        <Badge variant={selectedPair.entanglement_connection ? "default" : "secondary"}>
                          {selectedPair.entanglement_connection ? "Connected" : "Disconnected"}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    <Activity className="w-12 h-12 mx-auto mb-3 opacity-30" />
                    <p>Select a tetrahedron pair to view detailed analysis</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {showDetails && (
              <Card className="mt-4">
                <CardHeader>
                  <CardTitle className="text-sm">System Information</CardTitle>
                </CardHeader>
                <CardContent className="text-xs space-y-2">
                  <div>
                    <strong>Methane Metauniverse Theory:</strong> Reality modeled as geometric tetrahedron lattice
                  </div>
                  <div>
                    <strong>Counter-Tetrahedra:</strong> Antimatter pairs providing system stabilization
                  </div>
                  <div>
                    <strong>Entanglement:</strong> Physical connections between paired nodes
                  </div>
                  <div>
                    <strong>Oscillations:</strong> Internal vibrations projected as observable time
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;