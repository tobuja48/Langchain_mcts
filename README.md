# LangChain MCTS

🚧 **En Desarrollo** - Monte Carlo Tree Search integration for LangChain

Una librería que integra Monte Carlo Tree Search (MCTS) con LangChain para búsqueda y razonamiento avanzado con modelos de lenguaje.

## Estado del Proyecto

⚠️ **Esta librería está en desarrollo activo**. Todas las funciones actualmente retornan mensajes de "en desarrollo".

## Instalación

```bash
pip install langchain-mcts
```

## Uso Básico

```python
from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain

# Crear agente MCTS
agent = MCTSAgent()

# Realizar búsqueda MCTS
result = agent.search("¿Cuál es la mejor estrategia?")
print(result)  # 🚧 Esta función está en desarrollo - MCTS search functionality coming soon!

# Función de conveniencia
result = mcts_search("Mi query")
print(result)  # 🚧 MCTS search para 'Mi query' está en desarrollo - Coming soon!

# Crear cadena MCTS
chain = create_mcts_chain()
```

## 🆕 Nuevas funcionalidades implementadas

- **Implementación básica del algoritmo MCTS**: El núcleo del árbol de búsqueda Monte Carlo Tree Search (MCTS), con selección, expansión, simulación y retropropagación, ya está funcional para respuestas de modelos de lenguaje.
- **Integración directa con modelos de LangChain**: Ya puedes usar tus propios modelos (`BaseLanguageModel`) al crear agentes o ejecutar búsquedas MCTS.
- **Funciones de conveniencia mejoradas**: 
  - `mcts_search(query, model, iterations, seed_answers, ...)`: Ejecuta una búsqueda MCTS personalizada en una sola línea.
  - `create_mcts_chain(model, ...)`: Genera un agente MCTS configurado listo para integrarse en cadenas LangChain.
- **Sistema de evaluación y mejora de respuestas**: El agente puede solicitar una crítica, mejorar la respuesta paso a paso y puntuar su calidad automáticamente.
- **Soporte para respuestas semilla personalizadas**: Puedes dar respuestas iniciales para guiar la búsqueda.
- **Cobertura de tests y ejemplos de integración**: Se agregaron pruebas de integración y ejemplos de flujo de trabajo de extremo a extremo usando mocks.

## Ejemplo de uso actualizado

```python
from langchain_mcts import MCTSAgent, mcts_search, create_mcts_chain

# Crear agente con un modelo personalizado
agent = MCTSAgent(model=mi_llm)

# Realizar búsqueda avanzada MCTS
result = agent.search("¿Cuál es la mejor estrategia?", iterations=5)
print(result)

# Usar función de conveniencia
result = mcts_search("Mi query", model=mi_llm, iterations=3, seed_answers=["Respuesta 1", "Respuesta 2"])
print(result)

# Integración directa con LangChain
chain = create_mcts_chain(model=mi_llm)
```

## Funciones Disponibles

### `MCTSAgent`
Clase principal para agente MCTS:
- `search(query, iterations=100, seed_answers=None)`: Realiza búsqueda MCTS avanzada.
- Métodos internos para expansión, simulación, crítica y mejora de respuestas.

### `mcts_search(query, model, iterations=2, seed_answers=None, ...)`
Función de conveniencia para búsqueda MCTS rápida.

### `create_mcts_chain(model, ...)`
Crea una cadena MCTS para integración con LangChain.

### `MCTSNode`
Representa un nodo en el árbol MCTS con métodos para:
- Gestión de nodos padre/hijo
- Actualización de estadísticas
- Verificación de nodos hoja

### **Nuevos**
- Métodos para mejorar (`improve_answer`) y puntuar (`rate_answer`) respuestas con ayuda del modelo LLM.

## Características Planificadas (actualizado)

- ✅ Estructura base de la librería
- ✅ Implementación básica de MCTS y funciones de conveniencia
- ✅ Soporte para respuestas semilla personalizadas
- ✅ Evaluación y mejora automática de respuestas con LLM
- 🚧 Integración avanzada con modelos LangChain (cadenas y herramientas)
- 🚧 Optimización y tunning de políticas de búsqueda
- 🚧 Soporte para diferentes tipos de problemas y dominios
- 🚧 Paralelización de búsqueda y optimización de rendimiento
- 🚧 Métricas y visualización
- 🚧 Ejemplos avanzados de integración y tutoriales
- 🚧 Mejoras de interfaz para usuarios no técnicos

## Desarrollo

Para contribuir al desarrollo:

```bash
git clone https://github.com/tu-usuario/langchain-mcts
cd langchain-mcts
pip install -e .[dev]
```

Para ejecutar tests:

```bash
pytest tests/
```

## Dependencias

- `langchain>=0.1.0`
- `numpy>=1.20.0`

## Licencia

MIT

---

🔬 **Investigación en curso**: Esta librería forma parte de un proyecto de investigación en integración de algoritmos de búsqueda con modelos de lenguaje grandes.