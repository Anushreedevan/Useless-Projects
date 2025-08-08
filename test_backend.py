import requests
import time

# The URL of our Flask backend server
BASE_URL = "http://127.0.0.1:5000"

def test_endpoints():
    """Sends requests to the Flask app and prints the responses."""
    print("--- Starting backend tests ---")

    # --- 1. Test the START endpoint ---
    print("\n[STEP 1] Starting the audio listener...")
    try:
        response = requests.get(f"{BASE_URL}/start_listening")
        print(f"Response: {response.json()['status']}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure 'app.py' is running.")
        return

    # --- 2. Test the GET COUNT endpoint with the new logic ---
    print("\n[STEP 2] Waiting for the first whistle...")
    print("Please make a loud whistling sound to start the timer!")
    
    whistle_count = 0
    whistle_count_threshold = 3 # This should match the threshold in app.py

    # Wait for the first whistle to be detected
    while whistle_count == 0:
        try:
            response = requests.get(f"{BASE_URL}/get_count")
            whistle_count = response.json()['count']
            if whistle_count > 0:
                print(f"First whistle detected! Count: {whistle_count}")
                break
            time.sleep(1)
        except requests.exceptions.ConnectionError:
            print("Connection to the server was lost. Please restart 'app.py'.")
            return
    
    # Wait for the counter to increment automatically
    while whistle_count < whistle_count_threshold:
        try:
            response = requests.get(f"{BASE_URL}/get_count")
            new_count = response.json()['count']
            if new_count > whistle_count:
                print(f"Time-based whistle counted! Current count: {new_count}")
                whistle_count = new_count
            time.sleep(1) # Check the count every second
        except requests.exceptions.ConnectionError:
            print("Connection to the server was lost. Please restart 'app.py'.")
            return

    print("\nWhistle count threshold reached. The 'Amma' sound should be playing!")


    # --- 3. Test the STOP endpoint ---
    print("\n[STEP 3] Stopping the audio listener...")
    try:
        response = requests.get(f"{BASE_URL}/stop_listening")
        print(f"Response: {response.json()['status']}")
    except requests.exceptions.ConnectionError:
        print("Connection to the server was lost. Please restart 'app.py'.")

    print("\n--- Tests finished ---")

if __name__ == "__main__":
    test_endpoints()

