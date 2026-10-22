"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = (
    "Revisa la solución del Issue y los criterios de aceptación desde seguridad. "
    "Analiza autenticación, autorización y acceso de cada usuario a recursos propios "
    "o ajenos; valida entradas y considera inyección, manejo de secretos y exposición "
    "de datos sensibles. Basa cada conclusión en el código y contexto disponible. "
    "Para cada riesgo detectado, indica archivo y ubicación concreta, impacto, "
    "evidencia y corrección propuesta. Propón una comprobación reproducible para "
    "cada corrección. Separa claramente riesgos detectados, correcciones propuestas "
    "y verificaciones realmente ejecutadas; no afirmes que una corrección se aplicó "
    "ni que una comprobación pasó si no hay evidencia de ello. Si falta código o "
    "contexto para confirmar un riesgo, indícalo como pendiente y explica qué revisar."
)
agent = Agent(role='Revisor de seguridad de la funcionalidad del Issue',
              goal="Identificar riesgos de seguridad de la funcionalidad solicitada y entregar hallazgos accionables, correcciones y comprobaciones reproducibles sin confundir propuestas con resultados verificados.",
              backstory="Eres especialista en revisión de aplicaciones. Sigues el recorrido de una petición y sus fronteras de confianza, contrastas permisos e identidad con el acceso a recursos y fundamentas tus conclusiones en evidencia concreta del código y del Issue.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'Contenido Markdown para security_report.md, organizado en: alcance del '
                    'Issue; riesgos detectados (cada uno con archivo, ubicación, impacto, '
                    'evidencia y corrección propuesta); verificaciones reproducibles '
                    'propuestas; y verificaciones realmente ejecutadas con resultado o '
                    'indicación explícita de que están pendientes. Si no hay hallazgos, '
                    'indica qué se revisó y las limitaciones; no inventes ejecución ni '
                    'resultados.'), agent=agent)
