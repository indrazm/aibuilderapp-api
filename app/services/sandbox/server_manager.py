import os
import signal
import time

from loguru import logger


def stop_server(pid: int):
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)

        # Check if process is still running
        try:
            os.kill(pid, 0)
            # Process still exists, force kill
            os.kill(pid, signal.SIGKILL)
            logger.warning(f"Force killed server process {pid}")
        except ProcessLookupError:
            # Process already terminated
            pass

        logger.info(f"Server process {pid} stopped")
        return True

    except ProcessLookupError:
        logger.warning(f"Process {pid} not found")
        return False
    except Exception as e:
        logger.error(f"Error stopping server process {pid}: {e}")
        return False
