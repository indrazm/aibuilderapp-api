import random

from loguru import logger
from sqlmodel import Session, select

from app.database.engine import engine
from app.database.models import Project


def generate_available_port(min_port: int = 3000, max_port: int = 4000):
    max_attempts = 100

    with Session(engine) as session:
        used_ports = session.exec(select(Project.port)).all()
        used_ports_set = set(used_ports)

        logger.info(f"Found {len(used_ports_set)} ports already in use")

        for attempt in range(max_attempts):
            port = random.randint(min_port, max_port)

            if port not in used_ports_set:
                logger.info(f"Generated available port: {port}")
                return port

        logger.error(f"Could not find available port after {max_attempts} attempts")
        return None


def is_port_available(port: int):
    with Session(engine) as session:
        existing_project = session.exec(select(Project).where(Project.port == port)).first()

        is_available = existing_project is None
        logger.info(f"Port {port} is {'available' if is_available else 'in use'}")
        return is_available
