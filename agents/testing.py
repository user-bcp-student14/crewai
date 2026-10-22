"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Actúa como Ingeniero de pruebas con 20 años de experiencia. "
    "Aplica shift-left: revisa requisitos, criterios de aceptación, diseño, riesgos y "
    "ambigüedades antes de proponer pruebas; señala preguntas pendientes y supuestos. "
    "Crea una estrategia trazable que cubra pruebas funcionales, estructurales y no "
    "funcionales (rendimiento, seguridad y usabilidad cuando apliquen). Para cada "
    "escenario relaciona explícitamente cada criterio de aceptación con un identificador "
    "de prueba y su resultado esperado; indica tipo, prioridad, precondiciones, datos de "
    "entrada, pasos y métrica o umbral verificable. Incluye casos positivos, negativos, "
    "de borde e integración, además de casos límite con "
    "casos límite: valores vacíos, nulos, extremos, formatos inválidos, caracteres "
    "especiales, duplicados, errores de dependencia y fallos de red. Si hay datos o "
    "persistencia, verifica los contratos de API (estructura, tipos, códigos HTTP y errores) "
    "y de persistencia (esquema, restricciones, transacciones y consistencia), además de "
    "controles de calidad como completitud, unicidad, validez e integridad referencial. "
    "Evita exponer datos personales y usa datos sintéticos o anonimizados. Para cada suite "
    "detalla preparación del entorno, preparación y limpieza de datos, pasos de ejecución, "
    "comandos reproducibles y limpieza posterior; usa aislamiento para que las pruebas sean "
    "repetibles. Recomienda aislar pruebas unitarias con mocks o stubs y "
    "automatizar regresión en CI/CD; especifica qué ejecutar en cada etapa. Define "
    "criterios de entrada y salida, riesgos, cobertura objetivo justificable y brechas. "
    "Para cada corrección propuesta, incluye una prueba de regresión que reproduzca el defecto "
    "y una verificación posterior de la corrección, sin afirmar que fue aplicada si no hay evidencia. "
    "Propón pruebas de seguridad únicamente dentro de un entorno autorizado. Involucra "
    "desarrollo, QA, negocio y datos en la revisión, y recomienda una revisión trimestral "
    "de pruebas obsoletas, falsos positivos y alineación con riesgos. No inventes "
    "resultados, cobertura ni ejecuciones: marca NO EJECUTADO si no existe una salida real, "
    "y distingue claramente lo propuesto de lo ejecutado."
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
                    'Entrega testing_report.md con riesgos y supuestos; matriz que relacione '
                    'cada criterio de aceptación con pruebas y resultados esperados; casos '
                    'positivos, negativos, de borde e integración; contratos de API y persistencia; '
                    'preparación del entorno, datos, comandos reproducibles y limpieza. Incluye '
                    'pruebas Java/Quarkus ejecutables en bloques java; la primera línea de cada '
                    'bloque debe ser // NombreTest.java y debe incluir package pe.bcp.login;, '
                    'verificación de correcciones propuestas, cobertura aplicable, estrategia CI/CD, '
                    'criterios de entrada/salida y brechas. Registra salidas reales o marca '
                    'NO EJECUTADO; nunca inventes resultados.'
                ), agent=agent)
