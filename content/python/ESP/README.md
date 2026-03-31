# Práctica Interactiva - Programación Desde Cero

## Qué es esta herramienta

Este proyecto es una herramienta con la cual practicar desafíos (o ejercicios) de programación, desde un nivel inicial, usando Python 3.

Puede entenderse como la continuación práctica del curso gratuito de introducción a la programación en el canal de youtube "Programación Desde Cero", y también como un paso previo a la resolución de ejercicios más complejos como los que se desarrollan en el libro "[24 Días, 24 Desafíos de Código](https://patriciaemiguel.com/libro24desafios/)".

La herramienta no requiere conexión a internet (se puede ejecutar totalmente "offline"). Basta con tener Python instalado y usar un editor de texto (o un IDE) para resolver los ejercicios y una terminal para ejecutar las pruebas que los verifican.

Los ejercicios se enfocan en desarrollar habilidades algorítmicas y de razonamiento lógico así como aprender a trabajar con las bases de la programación y los tipos de datos fundamentales. No se centra en aprender los detalles del lenguaje Python. Es por ello que se alienta a que desarrolles tus propias soluciones evitando utilizar algunas herramientas que provee el lenguaje.

Los desafíos se dividen en temas para ayudarte a practicar ciertos tipos y estructuras de datos, pero eso no excluye
otras posibles soluciones (que podrían incluso ser más eficientes).

## Enfoque didáctico

Por cada categoría temática se presenta una serie de funciones incompletas (sin su cuerpo), y documentación que detalla cómo debería comportarse cada función. Además, cada función tiene una serie de pruebas (tests) unitarias relacionaas a ella. Necesitarás completar el cuerpo de las funciones de acuerdo a la consigna de cada una, de manera que todas las pruebas pasen.

Las pruebas se correrán para evaluar si la función devuelve el resultado esperado.

Los ejercicios están divididos en las siguientes categorías o temas: _números, strings, listas y tuplas, conjuntos y diccionarios_; lo que significa que se sugiere resolverlos utilizando estos tipos de datos con el fin de practicar las
bases. Pero también pueden resolverse en otras formas, siempre que los tests pasen exitosamente.

Aunque es posible comenzar por cualquiera de los temas propuestos, el siguiente orden permite resolverlos con
dificultad incremental:

1. Números
2. Strings
3. Listas y tuplas
4. Conjuntos y diccionarios

Esto implica que los ejercicios del módulo `numeros.py` pueden resolverse sin utilizar strings, listas, conjuntos ni
diccionarios. Los ejercicios del módulo strings pueden requerir manipulación de números. Los ejercicios de listas y
tuplas pueden necesitar manipulación de números y de strings además de listas y tuplas. Los ejercicios de conjuntos pueden requerir la manipulación números, strings, listas y tuplas, además de conjuntos. Finalmente, los ejercicios de diccionarios pueden requerir cualquiera de los temas anteriores (conjuntos, listas, tuplas, strings y números).

## Cómo está organizada esta herramienta

- La carpeta **ESP** contiene dos carpetas: **src** y **tests**.
  - La carpeta **/ESP/src** contiene un archivo asociado a cada categoría y en cada archivo se encuentran varias funciones cuya única instrucción es `pass`, que deberás completar con tu código.
  - La carpeta **/ESP/tests** contiene las pruebas unitarias. Hay un archivo de pruebas por cada archivo de categoría temática en `*/ESP/src`. Cada archivo tiene una función por ejercicio, con un nombre que empieza por "test_" y continúa con el nombre del ejercicio.
  
Podrás ejecutar las pruebas unitarias de cualquier ejercicio para evaluar si la solución dada es la correcta.

Inicialmente, todas las pruebas deberían fallar. El objetivo es escribir el cuerpo de las funciones en los archivos dentro de `/ESP/src` (reemplazando la instrucción `pass` por tu código) para hacer que las pruebas pasen.

Ejemplo: en `/ESP/src/numeros.py` se encuentra el ejercicio (función) `valor_absoluto` y en `/ESP/tests/tests_numeros.py` se encuentran las pruebas de ese ejercicio, en la función `test_valor_absoluto`.

## Cómo usar esta herramienta

Pre-requisito: Python 3 deberá estar instalado en el sistema (la versión mínima requerida es la 3.4).

A fin de resolver los ejercicios, solo deben modificarse las funciones dentro de los archivos en `/ESP/src`. Los archivos de `/ESP/tests` no deben modificarse.

Luego de agregar el algoritmo de una o más funciones dentro de los archivos de `/ESP/src`, necesitarás ejecutar las pruebas para determinar si pasan o fallan. Cuando las pruebas pasen, mostrarán "ok" en su resultado; si alguna prueba falla, mostrará qué función se ejecutó, qué argumentos se usaron para invocarla, qué retornó y cuál era el valor de retorno esperado.

Las pruebas podrán ejecutarse de tres formas:

- para una única función,
- para todas las funciones dentro de un archivo de `/ESP/src`,
- para más de un archivo de `/ESP/src` al mismo tiempo.

### Cómo resolver los ejercicios

Usando un editor de texto o un IDE, abrir alguno de los archivos de `/ESP/src` (de la categoría elegida). Ejemplo: `numeros.py`.

Cada ejercicio está representado por una función en el código de ese archivo. Ejemplo: `valor_absoluto()`.

Para saber cómo resolver cada ejercicio:

- La documentación (_docstrings_) de cada función indica lo que se espera que haga el algoritmo, provee ejemplos y un detalle de los parámetros y valor de retorno.
- La función de tests relacionada contiene las pruebas que muestran los casos que debe cumplir el algoritmo.

Dentro del archivo seleccionado den `/ESP/src`, reemplazar la instrucción `pass` de una o más funciones con el algoritmo que resuelva el ejercicio.

Para resolver los ejercicios, solo se deben modificar los cuerpos de las funciones de los archivos en `/ESP/src`. La firma de las funciones no debe modificarse, ni tampoco los archivos dentro de `/ESP/tests`.

Finalmente, ejecutar las pruebas de los ejercicios completados, para evaluar si pasan o fallan.

### Cómo ejecutar las pruebas

Es posible correr las pruebas para una sola función (esto es, un solo ejercicio), para todas las funciones de una categoría temática, o para todas las categorías a la vez.

Para ejecutar las pruebas se puede utilizar una terminal o también configurar el IDE de preferencia. En el caso de la terminal, se deberá cambia al directorio ("CD") de la carpeta del proyecto (ejemplo: si el proyecto se encuentra en C:/ESP será esa la carpeta donde deberás situarte) y luego ejecutar el comando de python correspondiente.

**Nota 1:** dependiendo de cómo se haya instalado Python, podría ser necesario reemplazar el comando "python" por "python3" o algún otro comando.

**Nota 2:** En caso de utilizar Pycharm, las configuraciones se deben crear desde el menú superior "Run > Edit Configurations" y luego "Add new run configuration".

#### Ejecutar las pruebas de una única función/ejercicio

En una terminal o línea de comandos, ejecutar el siguiente comando:

`python -m unittest -v ruta/al/archivo.py -k funcion_de_pruebas`

donde _ruta/al/archivo.py_ debe reemplazarse con la ruta desde la carpeta raíz del proyecto hasta el archivo de pruebas que contiene las pruebas que se ejecutarán (ej.: **tests/tests_numeros.py**) y _funcion_de_pruebas_ debe  reemplazarse con la función de pruebas a ejecutar (ej.: **test_valor_absoluto**). Por ejemplo, para ejecutar las pruebas de la función del ejercicio **valor_absoluto** de la categoría _numeros_:

`python -m unittest -v tests/tests_numeros.py -k test_valor_absoluto`

**Para hacer lo mismo utilizando una configuración de Pycharm:** selecciona la opción "Module name" (al editar configuraciones) y luego da clic en "..." para abrir un nuevo diálogo donde deberás escribir el nombre del archivo de la categoría a ejecutar (ej.: tests_numeros) y seleccionarlo del menú desplegable. Luego, en "Additional Arguments", ingresar "-k test_nombre_funcion" (reemplazando con el nombre de la función a ejecutar). Verifica que la opción "Add contents to PYTHONPATH" esté tildada.

#### Ejecutar todas las pruebas de una categoría

`python -m unittest -v ruta/al/archivo.py`

donde _ruta/al/archivo.py_ debe reemplazarse con la ruta desde la carpeta raíz del proyecto hasta el archivo de pruebas que contiene las pruebas que se ejecutarán (ej.: **tests/tests_numeros.py**). Por ejemplo, para ejecutar las pruebas de los ejercicios de la categoría _numeros_:

`python -m unittest -v tests/tests_numeros.py`

**Para hacer lo mismo utilizando una configuración de Pycharm:** selecciona la opción "Module name" y luego da clic en "..."  para abrir un nuevo diálogo donde deberás escribir el nombre del archivo de la categoría a ejecutar (ej.: **tests_numeros**) y seleccionarlo del menú desplegable. Verifica que la opción "Add contents to PYTHONPATH" esté tildada.

#### Ejecutar las pruebas de más de una categoría a la vez

Para ejecutar las pruebas de más de una categoría (o incluso todas las categorías al mismo tiempo), corre el archivo **ejecutar_tests.py**. En caso de ejecutar mediante terminal o línea de comandos, primero se deberá configurar la variable de entorno **PYTHONPATH** para que apunte a la carpeta del proyecto. Para evitar configurarla de manera definitiva, existe la opción de hacerlo de forma temporal, en cada sesión de la terminal. Para ello abre la terminal, CD al directorio del proyecto y luego ejecuta el siguiente comando:

`export PYTHONPATH="$PWD"` si estás en Linux/Mac, o

`set PYTHONPATH=%cd%` si estás en Windows.

A continuación, corre **ejecutar_tests.py** usando:

`python ejecutar_tests.py`

Si se utiliza Pycharm, será suficiente con correr el archivo **ejecutar_tests.py**, seleccionándolo y luego presionando Ctrl+Mayús+F10 o simplemente dando clic al botón "Run".

Si deseas obviar la ejecución de alguna categoría de pruebas, comenta (anteponiendo un #) la línea correspondiente en el archivo **ejecutar_tests.py**. La línea a comentar se verá como esta: `suite.addTests(loader.loadTestsFromModule(categoria_a_obviar))`.

## Abordaje sugerido

En proyectos profesionales, es probable que mucho de lo que se ejercita en estos desafíos se resuelva mediante herramientas predefinidas del lenguaje.

Pero, a fines educativos, limitar el uso de herramientas es una técnica válida para desarrollar el pensamiento algorítmico.

Por eso, se recomienda que, cuando practiques con esta herramienta, crees tus propios algoritmos, a fin de ejercitar el razonamiento lógico y las estructuras básicas de la programación. Con esa intención, en algunas funciones se sugiere evitar ciertas herramientas y encontrar soluciones alternativas.

Todos los desafíos planteados en este proyecto pueden ser resueltos sin necesidad de importar bibliotecas o módulos
adicionales (solo modificando el cuerpo de cada función).

Además, las categorías planteadas sugieren ciertos tipos y estructuras de datos para ayudar a reforzar el pensamiento
algorítmico, incluso cuando podrían encontrarse soluciones alternativas más eficientes. De todas formas, nada impide que resuelvas los ejercicios de la forma en que te parezca mejor, ya que estos temas son solo una sugerencia para guiar la práctica.
