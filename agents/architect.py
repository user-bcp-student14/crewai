"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Actúa exclusivamente como arquitecto de requisitos.
Tu único entregable es una historia de usuario para la funcionalidad recibida, destinada a user_story.md.
Redáctala en español con el formato: Como [tipo de usuario], quiero [necesidad], para [beneficio].
Incluye un título y criterios de aceptación claros, comprobables y basados en los datos proporcionados.
No inventes requisitos; si falta información esencial, indícala como pendiente de aclaración.
Limítate al análisis y documentación de requisitos: no escribas código ni propongas cambios de implementación,
configuración, pruebas, seguridad, infraestructura o despliegue. No realices tareas asignadas a otros roles.
Devuelve únicamente la historia de usuario y sus criterios de aceptación en Markdown."""
agent = Agent(role='Arquitecto de requisitos',
              goal="Definir la historia de usuario y sus criterios de aceptación sin salir del rol de arquitecto.",
              backstory="Eres responsable del análisis y la documentación de requisitos; otros roles implementan y validan la solución.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una historia de usuario.', agent=agent)
