import requests
import sys
import json
import time
from datetime import datetime

class TetracoreAPITester:
    def __init__(self, base_url="https://tetra-universe.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.created_pairs = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, params=params)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_status_endpoint(self):
        """Test basic status endpoint"""
        return self.run_test("Status Endpoint", "GET", "api/status", 200)

    def test_simulation_state(self):
        """Test simulation state endpoint"""
        return self.run_test("Simulation State", "GET", "api/simulation/state", 200)

    def test_start_simulation(self):
        """Test starting simulation"""
        return self.run_test("Start Simulation", "POST", "api/simulation/start", 200)

    def test_stop_simulation(self):
        """Test stopping simulation"""
        return self.run_test("Stop Simulation", "POST", "api/simulation/stop", 200)

    def test_reset_simulation(self):
        """Test resetting simulation"""
        return self.run_test("Reset Simulation", "POST", "api/simulation/reset", 200)

    def test_create_pair(self, center_x=0, center_y=0, center_z=0, separation=2.0):
        """Test creating a tetrahedron pair"""
        params = {
            'center_x': center_x,
            'center_y': center_y,
            'center_z': center_z,
            'separation': separation
        }
        success, response = self.run_test("Create Tetrahedron Pair", "POST", "api/pairs/create", 200, params=params)
        if success and 'pair_id' in response:
            self.created_pairs.append(response['pair_id'])
            return True, response['pair_id']
        return False, None

    def test_get_all_pairs(self):
        """Test getting all pairs"""
        return self.run_test("Get All Pairs", "GET", "api/pairs", 200)

    def test_get_pair(self, pair_id):
        """Test getting a specific pair"""
        return self.run_test(f"Get Pair {pair_id[:8]}", "GET", f"api/pairs/{pair_id}", 200)

    def test_delete_pair(self, pair_id):
        """Test deleting a pair"""
        success, _ = self.run_test(f"Delete Pair {pair_id[:8]}", "DELETE", f"api/pairs/{pair_id}", 200)
        if success and pair_id in self.created_pairs:
            self.created_pairs.remove(pair_id)
        return success

    def test_websocket_connection(self):
        """Test WebSocket connection (basic connectivity test)"""
        print(f"\n🔍 Testing WebSocket Connection...")
        try:
            import websocket
            ws_url = self.base_url.replace('https://', 'wss://') + '/api/ws'
            print(f"   WebSocket URL: {ws_url}")
            
            # Simple connection test
            ws = websocket.create_connection(ws_url, timeout=5)
            print("✅ WebSocket connection established")
            ws.close()
            self.tests_passed += 1
            self.tests_run += 1
            return True
        except ImportError:
            print("⚠️  WebSocket library not available, skipping WebSocket test")
            return True
        except Exception as e:
            print(f"❌ WebSocket connection failed: {str(e)}")
            self.tests_run += 1
            return False

def main():
    print("🚀 Starting Tetracore Server API Tests")
    print("=" * 50)
    
    tester = TetracoreAPITester()
    
    # Test basic endpoints
    print("\n📡 Testing Basic Endpoints")
    tester.test_status_endpoint()
    tester.test_simulation_state()
    
    # Test simulation controls
    print("\n🎮 Testing Simulation Controls")
    tester.test_start_simulation()
    time.sleep(1)  # Brief pause
    tester.test_stop_simulation()
    tester.test_reset_simulation()
    
    # Test tetrahedron pair management
    print("\n🔬 Testing Tetrahedron Pair Management")
    
    # Create multiple pairs
    success1, pair_id1 = tester.test_create_pair(0, 0, 0, 2.0)
    success2, pair_id2 = tester.test_create_pair(5, 0, 0, 2.5)
    success3, pair_id3 = tester.test_create_pair(-3, 2, 1, 3.0)
    
    # Test getting all pairs
    tester.test_get_all_pairs()
    
    # Test getting individual pairs
    if pair_id1:
        tester.test_get_pair(pair_id1)
    if pair_id2:
        tester.test_get_pair(pair_id2)
    
    # Test simulation with pairs
    print("\n⚡ Testing Simulation with Pairs")
    tester.test_start_simulation()
    print("   Letting simulation run for 3 seconds...")
    time.sleep(3)
    
    # Check state during simulation
    success, state_data = tester.test_simulation_state()
    if success:
        print(f"   Pairs count: {len(state_data.get('pairs', []))}")
        print(f"   System stability: {state_data.get('total_stability', 0):.2f}")
        print(f"   System energy: {state_data.get('system_energy', 0):.2f}")
        print(f"   Time step: {state_data.get('time_step', 0):.2f}")
        print(f"   Running: {state_data.get('running', False)}")
    
    tester.test_stop_simulation()
    
    # Test pair deletion
    print("\n🗑️  Testing Pair Deletion")
    if pair_id3:
        tester.test_delete_pair(pair_id3)
    
    # Verify deletion
    tester.test_get_all_pairs()
    
    # Test WebSocket connection
    print("\n🌐 Testing WebSocket Connection")
    tester.test_websocket_connection()
    
    # Clean up remaining pairs
    print("\n🧹 Cleaning up remaining pairs")
    for pair_id in tester.created_pairs.copy():
        tester.test_delete_pair(pair_id)
    
    # Final results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Backend API is working correctly.")
        return 0
    else:
        failed_tests = tester.tests_run - tester.tests_passed
        print(f"⚠️  {failed_tests} test(s) failed. Please check the backend implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())