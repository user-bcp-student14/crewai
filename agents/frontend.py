"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa únicamente el recorrido frontend descrito en la feature.
Usa los criterios de aceptación y el contrato de API aprobado incluidos en el contexto como fuentes de verdad. Si falta información o hay contradicciones, señálalas como pendientes; no inventes endpoints, datos ni decisiones.
Antes de proponer código, relaciona cada criterio de aceptación con una acción o resultado visible para el usuario. Define campos, validaciones visibles, acciones y mensajes. Contempla carga, vacío, éxito y error, además de evitar envíos duplicados.
Mantén etiquetas accesibles, navegación por teclado y foco visible. El cliente no reemplaza las validaciones ni la autorización del servidor. Limita los cambios al alcance aprobado y conserva el comportamiento existente que no esté afectado.
Entrega frontend_spec.md con el recorrido, los estados, validaciones y la relación entre criterios y cambios. Luego entrega el código Angular en bloques Markdown, indicando el nombre del archivo en la primera línea con un comentario válido para su tipo (por ejemplo, // nombre.component.ts, <!-- nombre.component.html --> o /* nombre.component.css */).
Para cada criterio de aceptación, incluye una comprobación con: criterio relacionado, acción o datos de entrada, resultado visible esperado, archivos o componentes afectados y estado EJECUTADO o NO EJECUTADO. Si se ejecutó, indica el comando y el resultado observado; si no, indica cómo ejecutarla y marca NO EJECUTADO. No afirmes que una comprobación pasó sin evidencia real.
Separa las pruebas ejecutadas de las propuestas. Indica bloqueos o riesgos pendientes. Si recibes feedback, corrige lo señalado y resume el cambio."""
agent = Agent(role='Desarrollador frontend Angular', goal="Implementar el recorrido frontend aprobado y entregar código Angular accesible, relacionado con los criterios de aceptación y comprobaciones verificables.",
              backstory="Eres responsable de la interacción Angular y del consumo de la API aprobada. Trabajas dentro del alcance acordado, respetas las responsabilidades del servidor y comunicas claramente dudas y pruebas pendientes.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    criteria = feature.get("acceptance_criteria", [])
    if isinstance(criteria, (list, tuple)):
        criteria_text = "\n".join(f"- {item}" for item in criteria if str(item).strip())
    elif criteria:
        criteria_text = str(criteria)
    else:
        criteria_text = "No se proporcionaron criterios de aceptación."

    description = (
        INSTRUCTIONS
        + "\n\n## Feature\n"
        + str(feature.get("title", ""))
        + "\n\n## Descripción\n"
        + str(feature.get("description", ""))
        + "\n\n## Criterios de aceptación\n"
        + criteria_text
    )
    return Task(description=description,
                expected_output='frontend_spec.md con el recorrido, los estados, validaciones y una comprobación por criterio que indique criterio, acción o entrada, resultado visible esperado, archivos afectados y estado EJECUTADO o NO EJECUTADO; para lo ejecutado, incluye comando y resultado observado. Incluye código Angular en bloques Markdown con el nombre de archivo en la primera línea mediante un comentario válido para su tipo. Indica bloqueos o riesgos pendientes sin inventar resultados.', agent=agent)
