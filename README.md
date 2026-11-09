# Taller de Programación Dinámica: Cambio de Monedas

Aplicación educativa para resolver el problema de cambio de monedas con **suministro ilimitado**, comparar programación dinámica con el método voraz y reconstruir una solución óptima.

## Ejecutar la aplicación

No requiere dependencias ni servidor. Abre `index.html` en un navegador moderno.

## Ejecutar las pruebas de Python

Requiere Python 3.10 o superior. Desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -v
```

## Implementación

La función `solve_coin_change(coins, amount)` de `src/coin_change.py` calcula la tabla de costos C y conserva las decisiones óptimas de la tabla P. Devuelve un objeto `CoinChangeResult` con:

- `minimum_coins`: cantidad mínima, o `None` si el monto es imposible.
- `one_solution()`: reconstruye una combinación óptima.
- `all_solutions(limit=1000)`: enumera combinaciones óptimas distintas con límite.
- `greedy_change(...)`: método voraz de referencia, no garantiza optimalidad.

## Recurrencia

Sea C[i][j] el mínimo número de monedas para formar j usando las primeras i denominaciones:

- C[i][0] = 0.
- C[0][j] = infinito para j > 0.
- Si d_i > j: C[i][j] = C[i-1][j].
- En otro caso: C[i][j] = min(C[i-1][j], 1 + C[i][j-d_i]).

El segundo término utiliza la misma fila i porque cada denominación puede reutilizarse ilimitadamente. P conserva las decisiones óptimas: ↑ para excluir y ← para incluir; en empates se conservan ambas.

## Caso de referencia

Con monedas {1, 5, 6, 9} y monto 11, el método voraz entrega 9 + 1 + 1 (3 monedas), mientras que programación dinámica encuentra 6 + 5 (2 monedas).

## Complejidad

El cálculo de C y P tarda O(nM) y usa O(nM) memoria, donde n es el número de denominaciones y M el monto objetivo. La enumeración de todas las soluciones óptimas puede ser exponencial; por eso tiene un límite configurable.

## Estructura

- `index.html`: interfaz interactiva.
- `src/coin_change.py`: algoritmo y reconstrucción.
- `tests/test_coin_change.py`: pruebas automatizadas.
- `.gitignore`: excluye cachés y entornos virtuales.
