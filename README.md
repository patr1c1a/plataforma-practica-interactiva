# Plataforma de Ejercicios de Programación

Este repositorio contiene una plataforma educativa para practicar fundamentos de programación mediante ejercicios con validación automática basada en tests.

El proyecto está diseñado para cumplir dos objetivos:

- Proveer una **versión offline**, descargable y usable de forma independiente, para practicar ejercicios de programación en un entorno local y sin interfaz gráfica.
- Desarrollar una **versión web** que permita resolver los mismos ejercicios desde el navegador, reutilizando exactamente el mismo contenido y los mismos tests.

El foco del proyecto está puesto en el razonamiento algorítmico, la lectura de errores reales y la práctica cercana a un entorno profesional, evitando abstracciones innecesarias, dependencias externas y ayudas automáticas.

---

## Estructura general del repositorio

```raw
plataforma-ejercicios/
│
├── content/  # Contenido educativo (versión offline)
│├── python/
││├── ESP/
│└└── ENG/
│
├── web/      # Versión web (en desarrollo)
│
├── runtime/  # Directorios temporales de ejecución
│
└── README.md
```

---

## Versión offline (contenido educativo)

La versión offline del proyecto se encuentra en:

`content/python/`

Dentro de esta carpeta hay dos versiones equivalentes del mismo contenido:

- `ESP/` → versión en español  
- `ENG/` → versión en inglés  

Cada una de estas carpetas **puede usarse de forma independiente**, sin necesidad de la versión web.

---

## Objetivo de los ejercicios (versión offline)

Este proyecto intenta ser una herramienta con la cual practicar ejercicios de programación, desde un nivel inicial.

Los ejercicios se enfocan en desarrollar habilidades algorítmicas y de razonamiento lógico, así como aprender a trabajar con las bases de la programación y los tipos de datos fundamentales. No se centra en aprender los detalles de un lenguaje en particular.

Los ejercicios se dividen en temas para ayudar a practicar ciertos tipos y estructuras de datos, pero eso no excluye otras posibles soluciones (que podrían incluso ser más eficientes).

---

## Cómo está planteado el proyecto offline

Se presenta una serie de funciones incompletas (sin su cuerpo), junto con documentación que indica cómo debería comportarse cada función.

Además, cada función tiene asociadas pruebas unitarias (tests).

El objetivo es completar el cuerpo de las funciones de acuerdo a la consigna, de manera que todas las pruebas pasen.

Al ejecutar los tests:

- si todos pasan, el ejercicio está correctamente resuelto;
- si alguno falla, se muestra el error real producido, junto con el valor esperado.

---

## Estructura de la versión offline

Dentro de `content/python/ESP` (y de forma análoga en `ENG`) se encuentran:

```raw
ESP/
├── src/ # Archivos con funciones incompletas
├── tests/ # Tests unitarios (no deben modificarse)
├── ejecutar_tests.py # Runner para ejecutar múltiples categorías
└── soluciones_propuestas.md
```

Los ejercicios están organizados por categorías con dificultad incremental:

1. Números  
2. Strings  
3. Listas y tuplas  
4. Conjuntos y diccionarios  

---

## Cómo usar la versión offline

### Requisitos

- Python 3 instalado.
- No se requieren dependencias externas.

### Resolver un ejercicio

Seleccionar el archivo relacionado al tema sobre el cual se desea trabajar (números, strings, listas y tuplas, conjuntos y diccionarios).

En cada archivo hay funciones que representan cada ejercicio. Estas funciones tienen varias partes:

- La firma: indicando nombre de la función y parámetros.
- Documentación: que explica lo que la función debe hacer y retornar. Incluye ejemplos, lista de parámetros y valor de retorno.
- La instrucción "pass" que solo permite que el código ejecute aunque un ejercicio no haya sido resuelto.

Para resolver un ejercicio, el algoritmo debe escribirse en reemplazo de la palabra clave "pass" (la cual debe eliminarse).

Finalmente, se deben correr las pruebas para verificar la solución. Las pruebas pueden ejecutarse:

- para una sola función (ejercicio),
- para un archivo completo,
- para los 4 archivos.

### Importante

Para ejecutar las pruebas, es necesario ubicarse **dentro de la carpeta ESP (o ENG)** antes de correr los comandos.

Ejemplo:

```bash
cd content/python/ESP
```

### Ejecutar una única prueba de un ejercicio

Ejemplo: ejecutar solo la prueba `test_menor` del archivo `tests_numeros.py`:

`python -m unittest -v tests/tests_numeros.py -k test_menor`

### Ejecutar todas las pruebas de una categoría

Ejemplo: ejecutar todas las pruebas del archivo `tests_numeros.py`:

`python -m unittest -v tests/tests_numeros.py`

### Ejecutar todos las pruebas del proyecto

Para ejecutar las pruebas de todas las categorías, utilizar el runner provisto:

`python ejecutar_tests.py`

## Versión web (en desarrollo)

La versión web del proyecto se encuentra en la carpeta:

`web/`

Esta versión permite:

- seleccionar una categoría de ejercicios,
- seleccionar un ejercicio a resolver,
- ejecutar las mismos pruebas que se usan en la versión offline,
- ver los errores reales producidos por el código,
- ver el progreso de ejercicios intentados o completados en cada categoría,
- reiniciar un ejercicio o resetear el progreso completo,
- exportar e importar el progreso de resolución de ejercicios,
- seleccionar tema claro/oscuro (con el oscuro siendo el tema por defecto).

La versión web reutiliza exactamente el mismo contenido y las mismas pruebas que la versión offline.

El contenido educativo no se duplica ni se modifica para adaptarse a la web.

## Filosofía del proyecto

- Priorizar fundamentos y razonamiento por sobre herramientas.
- Trabajar con errores reales y feedback no simplificado.
- Proveer en la versión offline un entorno que permita familiarizarse con la terminal.
- Mantener el proyecto simple y mantenible.

## Unit tests

Deben correrse desde la carpeta raíz del proyecto y dentro del entorno virtual, donde antes deben instalarse los paquetes necesarios: `pip install -r requirements.txt`.

Correr unit tests: `python -m unittest discover -s web/tests -v`.
