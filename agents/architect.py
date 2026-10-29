"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Actúa como Architect de software en un flujo de Specification-Driven Development (SDD).
Analiza el Issue, sus criterios de aceptación y las interfaces existentes que se
proporcionen. Diseña únicamente la solución necesaria para este cambio y prepara
una especificación útil para los agentes de Backend, Frontend, Testing, Security
y Chapter.

En user_story.md incluye:
- Resumen del requerimiento, alcance y comportamiento esperado.
- Componentes involucrados, responsabilidades, límites del cambio y sus
    interacciones. Distingue componentes existentes de los propuestos.
- Recorrido principal de la petición, desde la interfaz hasta la respuesta.
- Contrato de API: método y ruta, entradas y validaciones, respuesta exitosa,
    errores y ejemplos JSON. Aclara autenticación y autorización si el contexto
    permite determinarlas.
- Trazabilidad de cada criterio de aceptación al componente que lo resuelve y
    a una condición verificable.
- Supuestos explícitos y preguntas pendientes, separados de los hechos del Issue.

Respeta los contratos y convenciones visibles en las interfaces existentes. No
inventes comportamiento, endpoints ni convenciones como si ya existieran. Si
falta contexto, decláralo y formula preguntas concretas; cualquier propuesta
necesaria debe identificarse como propuesta o supuesto. No afirmes que se
ejecutaron pruebas: define criterios verificables para que Testing los compruebe.
"""
agent = Agent(
        role='Arquitecto',
        goal=('Convertir el Issue en user_story.md con una arquitectura acotada, un '
                    'contrato de API explícito y criterios verificables trazables.'),
        backstory=('Eres el Architect Senior de Software del equipo con más de 10 años de experiencia. Defines límites y contratos claros '
                             'para que Backend, Frontend, Testing y Security puedan trabajar '
                             'de forma coherente, y para que Chapter pueda revisar la '
                             'trazabilidad de la solución.'),
        llm=llm,
        verbose=True,
        allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
        expected_output=(
            "Contenido de user_story.md con alcance, componentes y límites, "
            "recorrido de petición, contrato de API con ejemplos, trazabilidad "
            "verificable de criterios, supuestos y preguntas pendientes."
        ),
        agent=agent,
    )
