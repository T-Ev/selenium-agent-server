import subprocess
import sys
import time
import signal
import os
from typing import List

class ServerManager:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.running = True

    def start_redis(self):
        print("Starting Redis server...")
        try:
            process = subprocess.Popen(
                ["redis-server"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(process)
            time.sleep(2)  # Wait for Redis to start
            print("Redis server started")
        except FileNotFoundError:
            print("Error: Redis server not found. Please install Redis.")
            self.shutdown()
            sys.exit(1)

    def start_celery(self):
        print("Starting Celery worker...")
        celery_cmd = [
            "celery",
            "-A", "app.core.celery_app",
            "worker",
            "--loglevel=info",
            "--pool=solo"  # Use solo pool for Windows compatibility
        ]
        process = subprocess.Popen(
            celery_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.processes.append(process)
        time.sleep(2)  # Wait for Celery to start
        print("Celery worker started")

    def start_uvicorn(self):
        print("Starting FastAPI server...")
        uvicorn_cmd = [
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ]
        process = subprocess.Popen(
            uvicorn_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.processes.append(process)
        print("FastAPI server started")

    def shutdown(self, signum=None, frame=None):
        print("\nShutting down all servers...")
        self.running = False
        
        # Send SIGTERM to all processes
        for process in self.processes:
            if process.poll() is None:  # If process is still running
                if sys.platform == 'win32':
                    process.terminate()
                else:
                    process.send_signal(signal.SIGTERM)
        
        # Wait for all processes to finish
        for process in self.processes:
            process.wait()
        
        print("All servers stopped")
        sys.exit(0)

    def run(self):
        # Register signal handlers
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        try:
            self.start_redis()
            self.start_celery()
            self.start_uvicorn()

            print("\nAll servers are running!")
            print("Access the API documentation at: http://localhost:8000/docs")
            print("Press Ctrl+C to stop all servers\n")

            # Keep the script running
            while self.running:
                time.sleep(1)

        except Exception as e:
            print(f"Error occurred: {e}")
            self.shutdown()

if __name__ == "__main__":
    # Ensure we're in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    manager = ServerManager()
    manager.run() 