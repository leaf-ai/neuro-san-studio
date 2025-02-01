import os
import subprocess
import signal
import glob
import sys
import argparse
import threading

class NeuroSanRunner:
    """Command-line tool to run the Neuro SAN server and web client."""

    def __init__(self):
        """Initialize configuration and parse CLI arguments."""
        self.is_windows = os.name == "nt"

        # Default Configuration
        self.neuro_san_server_host = "localhost"
        self.neuro_san_server_port = 30013
        self.neuro_san_web_client_port = 5003
        self.neuro_san_agent_name = "hello_world"
        self.thinking_file = "C:\\tmp\\agent_thinking.txt" if self.is_windows else "/tmp/agent_thinking.txt"

        # Parse command-line arguments
        self.config = self.parse_args()

        # Process references
        self.server_process = None
        self.app_process = None

        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)

    def parse_args(self):
        """Parses command-line arguments for configuration."""
        parser = argparse.ArgumentParser(description="Run the Neuro SAN server and web client.")

        parser.add_argument('--server-host', type=str, default=self.neuro_san_server_host, help="Host address for the Neuro SAN server")
        parser.add_argument('--server-port', type=int, default=self.neuro_san_server_port, help="Port number for the Neuro SAN server")
        parser.add_argument('--web-client-port', type=int, default=self.neuro_san_web_client_port, help="Port number for the web client")
        parser.add_argument('--agent-name', type=str, default=self.neuro_san_agent_name, help="Agent name for the session")
        parser.add_argument('--thinking-file', type=str, default=self.thinking_file, help="Path to the agent thinking file")
        parser.add_argument('--demo-mode', action='store_true', help="Run in demo mode, using default neuro-san settings")

        return vars(parser.parse_args())

    def set_environment_variables(self):
        """Set required environment variables, optionally using neuro-san defaults."""
        os.environ["PYTHONPATH"] = os.getcwd()

        if self.config["demo_mode"]:
            os.environ.pop("AGENT_MANIFEST_FILE", None)
            os.environ.pop("AGENT_TOOL_PATH", None)
            print("Running in **Demo Mode** - Using neuro-san default manifest and tools")
        else:
            os.environ["AGENT_MANIFEST_FILE"] = "./registries/manifest.hocon"
            os.environ["AGENT_TOOL_PATH"] = "./coded_tools"

        print(f"PYTHONPATH set to: {os.environ['PYTHONPATH']}\n")
        if not self.config["demo_mode"]:
            print(f"AGENT_MANIFEST_FILE set to: {os.environ['AGENT_MANIFEST_FILE']}")
            print(f"AGENT_TOOL_PATH set to: {os.environ['AGENT_TOOL_PATH']}\n")

    def generate_html_files(self):
        """Generate .html files for all registry files except manifest.hocon."""
        for file in glob.glob("./registries/*"):
            if os.path.basename(file) != "manifest.hocon":
                print(f"Generating .html file for: {file}")
                result = subprocess.run(
                    [sys.executable, "-m", "neuro_san_web_client.agents_diagram_builder", "--input_file", file],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
                )
                print(result.stdout)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)

    def stream_output(self, pipe, log_file, prefix):
        """Stream subprocess output to console and log file in real-time."""
        with open(log_file, "a") as log:
            for line in iter(pipe.readline, ''):
                formatted_line = f"{prefix}: {line.strip()}"
                print(formatted_line)  # Print to console
                log.write(formatted_line + "\n")  # Write to log file
        pipe.close()

    def start_process(self, command, process_name, log_file):
        """Start a subprocess and capture logs."""
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if self.is_windows else 0

        with open(log_file, "w") as log:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, bufsize=1, universal_newlines=True,
                                       preexec_fn=None if self.is_windows else os.setpgrp,
                                       creationflags=creation_flags)

        print(f"Started {process_name} with PID {process.pid}")

        # Start streaming logs in separate threads
        stdout_thread = threading.Thread(target=self.stream_output, args=(process.stdout, log_file, process_name))
        stderr_thread = threading.Thread(target=self.stream_output, args=(process.stderr, log_file, process_name))
        stdout_thread.start()
        stderr_thread.start()

        return process

    def signal_handler(self, signum, frame):
        """Handle termination signals to cleanly exit."""
        print("\nTermination signal received. Stopping all processes...")

        if self.server_process:
            print(f"\nStopping SERVER (PID {self.server_process.pid})...")
            if self.is_windows:
                self.server_process.terminate()
            else:
                os.killpg(os.getpgid(self.server_process.pid), signal.SIGKILL)

        if self.app_process:
            print(f"Stopping WEB CLIENT (PID {self.app_process.pid})...")
            if self.is_windows:
                self.app_process.terminate()
            else:
                os.killpg(os.getpgid(self.app_process.pid), signal.SIGKILL)

        sys.exit(0)

    def run(self):
        """Run the Neuro SAN server and web client."""
        print("\nRun Config:\n" + "\n".join(f"{key}: {value}" for key, value in self.config.items()) + "\n")

        # Set environment variables
        self.set_environment_variables()

        # Generate HTML files if not in demo mode
        if not self.config["demo_mode"]:
            self.generate_html_files()

        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)

        # Set up signal handling for termination
        signal.signal(signal.SIGINT, self.signal_handler)  # Handle Ctrl+C
        if not self.is_windows:
            signal.signal(signal.SIGTERM, self.signal_handler)  # Handle kill command (not available on Windows)

        # Start server (Log to logs/server.log)
        server_command = [
            sys.executable, "-u", "-m", "neuro_san.service.agent_main_loop",
            "--port", str(self.config["server_port"])
        ]
        self.server_process = self.start_process(server_command, "SERVER", "logs/server.log")

        print(f"CLIENT: {self.config['agent_name']}")
        # Start web client (Log to logs/client.log)
        client_command = [
            sys.executable, "-u", "-m", "neuro_san_web_client.app",
            "--server-host", self.config["server_host"],
            "--server-port", str(self.config["server_port"]),
            "--web-client-port", str(self.config["web_client_port"]),
            "--agent-name", self.config["agent_name"],
            "--thinking-file", self.config["thinking_file"]
        ]
        self.app_process = self.start_process(client_command, "WEB CLIENT", "logs/client.log")

        # Wait for both processes to finish
        self.server_process.wait()
        self.app_process.wait()


if __name__ == "__main__":
    runner = NeuroSanRunner()
    runner.run()
