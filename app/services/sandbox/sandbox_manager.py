import os
import subprocess
import time

from loguru import logger


def setup_sandbox(project_id: str, port: int):
    """
    Setup package.json and bun.js server to serve HTML files in the sandbox.

    This function creates:
    1. A package.json file with bun configuration
    2. A server.js file that serves HTML files using Bun
    3. Starts the server in the background

    Returns:
        tuple: (message, pid) - A message indicating the success and the server PID, or (error_message, None) on failure.
    """
    os.makedirs(f"sandbox/projects/{project_id}", exist_ok=True)

    try:
        logger.info("Setting up sandbox with package.json and Bun server")

        with open("sandbox/templates/package.json", "r") as f:
            package_json = f.read()

        with open(f"sandbox/projects/{project_id}/package.json", "w+") as f:
            f.write(package_json)
        logger.info("Created package.json")

        with open("sandbox/templates/server.js", "r") as f:
            server_js = f.read().replace("{PORT}", str(port))

        with open(f"sandbox/projects/{project_id}/server.js", "w+") as f:
            f.write(server_js)
        logger.info("Created server.js")

        with open("sandbox/templates/index.html", "r") as f:
            index_html = f.read()

        with open(f"sandbox/projects/{project_id}/index.html", "w+") as f:
            f.write(index_html)

        logger.info("Starting Bun server in background")
        process = subprocess.Popen(
            ["bun", "run", "server.js"],
            cwd=f"sandbox/projects/{project_id}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        logger.info(f"Server process created with PID: {process.pid}")

        time.sleep(1)
        if process.poll() is not None:
            _, stderr = process.communicate()
            error_msg = stderr.decode()
            logger.error(f"Server failed to start: {error_msg}")
            return f"Error starting server: {error_msg}", None

        result = f"Sandbox setup complete! Server running at http://localhost:{port}, PID: {process.pid}"
        logger.info(result)
        return result, process.pid

    except Exception as e:
        logger.error(f"Error setting up sandbox: {e}")
        return f"Error setting up sandbox: {e}", None
