"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Tareas del ingeniero de pruebas:\n"
    "1. Revisar requisitos y criterios de aceptación; señalar ambigüedades, supuestos y riesgos.\n"
    "2. Relacionar cada criterio con casos identificables y resultados esperados verificables.\n"
    "3. Diseñar casos positivos, negativos, de borde e integración; validar contratos de API y persistencia cuando estén definidos.\n"
    "4. Detallar precondiciones, preparación del entorno, datos sintéticos, pasos, comandos reproducibles y limpieza.\n"
    "5. Proponer automatización, aislamiento de pruebas unitarias y regresión para las correcciones.\n"
    "6. Generar pruebas Java/Quarkus solo si el código y los contratos disponibles permiten que sean coherentes; no inventar clases, métodos ni endpoints.\n"
    "7. No afirmar que ejecutaste pruebas ni comandos. Marca NO EJECUTADO salvo que el contexto incluya una salida real."
)
agent = Agent(role='Ingeniero de pruebas',
              goal="Diseñar una estrategia de pruebas medible, trazable y alineada con los riesgos del negocio.",
              backstory="Eres un ingeniero de pruebas con 20 años de experiencia en "
              "validación de requisitos, calidad de datos, automatización y gestión de riesgos.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'Genera el archivo testing_report.md que contiene riesgos y supuestos; matriz criterio-prueba-resultado; '
                    'casos positivos, negativos, de borde e integración; contratos de API y persistencia '
                    'cuando estén definidos; preparación, datos, comandos y limpieza; regresión para '
                    'correcciones; estrategia de automatización, criterios de entrada/salida y brechas. '
                    'Incluye código Java/Quarkus solo si puede basarse en el contexto disponible. Cada '
                    'bloque Java extraíble debe iniciar con // NombreTest.java y declarar package '
                    'pe.bcp.login;. Si faltan datos para un test ejecutable, explica qué falta en vez '
                    'de inventar código. Registra evidencia real o marca NO EJECUTADO; no afirmes '
                    'ejecuciones ni cobertura sin evidencia.'
                ), agent=agent)
