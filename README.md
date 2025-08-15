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

## Funciones Disponibles

### `MCTSAgent`
Clase principal para agente MCTS:
- `search(query, iterations=100)`: Realiza búsqueda MCTS
- `expand_node(node)`: Expande nodos en el árbol MCTS
- `simulate(node)`: Simula desde un nodo
- `backpropagate(path, value)`: Propaga valores hacia atrás

### `mcts_search(query, model=None, **kwargs)`
Función de conveniencia para búsqueda MCTS rápida.

### `create_mcts_chain(model=None, **kwargs)`
Crea una cadena MCTS para integración con LangChain.

### `MCTSNode`
Representa un nodo en el árbol MCTS con métodos para:
- Gestión de nodos padre/hijo
- Actualización de estadísticas
- Verificación de nodos hoja

## Características Planificadas

- ✅ Estructura base de la librería
- 🚧 Implementación completa de MCTS
- 🚧 Integración con modelos LangChain
- 🚧 Optimización de políticas de búsqueda
- 🚧 Soporte para diferentes tipos de problemas
- 🚧 Paralelización de búsqueda
- 🚧 Métricas y visualización

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