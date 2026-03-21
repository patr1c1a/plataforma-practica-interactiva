# Práctica Interactiva - Programación Desde Cero

Este repositorio contiene una plataforma educativa para practicar fundamentos de programación mediante ejercicios con validación automática basada en tests.

El proyecto está diseñado para cumplir dos objetivos:

- Proveer una **versión offline**, descargable y usable de forma independiente, para practicar ejercicios de programación en un entorno local y sin interfaz gráfica.
- Desarrollar una **versión web** que permita resolver los mismos ejercicios desde el navegador, reutilizando exactamente el mismo contenido y los mismos tests.

El foco del proyecto está puesto en el razonamiento algorítmico, la lectura de errores reales y la práctica cercana a un entorno profesional, evitando abstracciones innecesarias, dependencias externas y ayudas automáticas.

## Filosofía del proyecto

- Servir como continuación práctica del curso introductorio ofrecido en el canal "Programación Desde Cero".
- Priorizar fundamentos y razonamiento por sobre herramientas.
- Proveer en la versión offline un entorno que permita familiarizarse con la terminal.
- Mantener el proyecto simple y mantenible.

---

## Estructura general del repositorio

```raw
plataforma-practica-interactiva/
│
├── content/  # Contenido educativo (versión offline)
│├── python/
││├── ESP/
│└└── ENG/
│
├── web/      # Versión web
│
├── runtime/  # Directorios temporales de ejecución
│
├── requirements.txt  # Dependencias necesarias
│
├── LICENSE.md  # Licencia de uso
│
└── README.md
```

---

## Objetivo de los ejercicios

Esta herramienta permite practicar ejercicios de programación, desde un nivel inicial.

Los ejercicios se enfocan en desarrollar habilidades algorítmicas y de razonamiento lógico, así como aprender a trabajar con las bases de la programación y los tipos de datos fundamentales. No se centra en aprender los detalles de un lenguaje en particular.

Los ejercicios se dividen en temas para ayudar a practicar ciertos tipos y estructuras de datos, pero eso no excluye otras posibles soluciones (que podrían incluso ser más eficientes).

---

## Versión offline (contenido educativo)

La "versión offline" no requiere conexión a internet (se puede ejecutar totalmente "offline"). Basta con tener Python instalado y usar un editor de texto (o un IDE) para resolver los ejercicios y una terminal para ejecutar las pruebas que los verifican.

La versión offline del proyecto se encuentra en:

`content/python/`

Dentro de esta carpeta hay dos versiones equivalentes del mismo contenido:

- `ESP/` → versión en español  
- `ENG/` → versión en inglés  

Cada una de estas carpetas **puede usarse de forma independiente**, sin necesidad de la versión web.

### Cómo está planteado el proyecto offline

Se presenta una serie de funciones incompletas (sin su cuerpo), junto con documentación que indica cómo debería comportarse cada función.

Además, cada función tiene asociadas pruebas unitarias (tests).

El objetivo es completar el cuerpo de las funciones de acuerdo a la consigna, de manera que todas las pruebas pasen.

Al ejecutar los tests:

- si todos pasan, el ejercicio está correctamente resuelto;
- si alguno falla, se muestra el error real producido, junto con el valor esperado.

### Estructura de la versión offline

Dentro de `content/python/ESP` (y de forma análoga en `ENG`) se encuentran:

```raw
ESP/
├── src/   # Archivos con funciones incompletas
├── tests/   # Tests unitarios (no deben modificarse)
├── ejecutar_tests.py   # Runner para ejecutar múltiples categorías
├── LICENSE.md   # Licencia de uso
└── README.md   # Readme para usuarios de la versión offline
```

Los ejercicios están organizados por categorías con dificultad incremental:

1. Números  
2. Strings  
3. Listas y tuplas  
4. Conjuntos y diccionarios  

### Requisitos para usar la versión offline

- Python 3 instalado (no se requieren dependencias externas).
- Editor de texto o IDE.
- Terminal / línea de comandos (que puede estar incoporada en el IDE).

### Resolver un ejercicio en la versión offline

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

### Verificar los ejercicios (correr pruebas) en la versión offline

Para ejecutar las pruebas, es necesario ubicarse dentro de la carpeta ESP (o ENG) antes de correr los comandos.

Ejemplo:

```bash
cd content/python/ESP
```

#### Ejecutar una única prueba de un ejercicio

Ejemplo: ejecutar solo la prueba `test_menor` del archivo `tests_numeros.py`:

`python -m unittest -v tests/tests_numeros.py -k test_menor`

#### Ejecutar todas las pruebas de una categoría

Ejemplo: ejecutar todas las pruebas del archivo `tests_numeros.py`:

`python -m unittest -v tests/tests_numeros.py`

#### Ejecutar todos las pruebas del proyecto

Para ejecutar las pruebas de todas las categorías, utilizar el runner provisto:

`python ejecutar_tests.py`

---

## Versión web

La versión web del proyecto se encuentra en la carpeta:

`web/`

Esta versión permite:

- seleccionar tema claro/oscuro (con el oscuro siendo el tema por defecto),
- seleccionar una categoría de ejercicios,
- seleccionar un ejercicio a resolver,
- ejecutar las mismas pruebas que se usan en la versión offline,
- ver detalles sobre la ejecución de las pruebas,
- ver el progreso de ejercicios intentados o completados en cada categoría,
- exportar e importar el progreso de resolución de ejercicios,
- reiniciar un ejercicio o resetear el progreso completo.

La versión web reutiliza exactamente el mismo contenido y las mismas pruebas que la versión offline.

El contenido educativo no se duplica ni se modifica para adaptarse a la web.

---

## Salida de tests en versión web

- La salida "Ver detalles" se sanitiza para no exponer internals de tests (rutas, nombres internos y frames de traceback).
- Se muestra al inicio `Tests ejecutados: X`, donde `X` es la cantidad de subtests ejecutados para ese ejercicio.

---

## Unit tests

Deben correrse desde la carpeta raíz del proyecto y dentro del entorno virtual, donde antes deben instalarse los paquetes necesarios: `pip install -r requirements.txt`.

Correr todos los unit tests: `python -m unittest discover -s web/tests -v`.

Correr solo un archivo de unit tests: `python -m unittest web.tests.archivo -v` (reemplazando "archivo" por el nombre del archivo, por ejemplo: "test_security_regressions").

---

## Sandbox de ejecución web

La versión web ejecuta las pruebas de usuarios en un contenedor Docker aislado por defecto.

### Construcción de imagen (primera vez)

Desde la raíz del proyecto:

`docker build -t plataforma-practica-interactiva-runner:latest -f web/sandbox_runner/Dockerfile .`

Solo se deberá volver a correr este comando si se modifica web/sandbox_runner/Dockerfile.

### Ejecución local del proyecto web

- Activar el entorno virtual
- Instalar dependencias: `pip install -r requirements.txt`
- Levantar la app (ejemplo): `uvicorn web.main:app --reload`
- Docker no es necesario para levantar la app.
- Docker sí es necesario para ejecutar código de usuarios cuando `EXECUTION_SANDBOX_PROVIDER=docker` (default).
- Verificar imagen Docker disponible (opcional, recomendado): `docker images | findstr plataforma-practica-interactiva-runner`
- Si algún proceso queda en ejecución, es necesario matar los procesos Python (ejemplo en Windows: `taskkill /F /IM python.exe`).

### Configuración del sandbox

- `EXECUTION_SANDBOX_PROVIDER`:
  - `docker` (default, recomendado para entorno expuesto a internet)
  - `local` (solo desarrollo local, sin aislamiento OS/container)
- `EXECUTION_ALLOW_LOCAL_IN_PROD`:
  - default: deshabilitado
  - habilita `local` en producción solo si vale `1`, `true` o `yes`
  - recomendado: mantener deshabilitado en internet público
- Restricción opcional para `local`:
  - `EXECUTION_LOCAL_MAX_MEMORY_BYTES`: límite de memoria del proceso hijo en bytes (solo POSIX/Linux)
  - `EXECUTION_LOCAL_MAX_FILE_BYTES`: tamaño máximo de archivos que puede generar el proceso hijo en bytes (solo POSIX/Linux).
  - `EXECUTION_LOCAL_MAX_PROCESSES`: límite de procesos hijo/subprocesos (solo POSIX/Linux).
  - `EXECUTION_LOCAL_MAX_CPU_SECONDS`: límite de CPU del proceso hijo en segundos (solo POSIX/Linux).
  - recomendado si se expone a internet con `local`: definir límites conservadores y ejecutar el servicio con un usuario sin privilegios.
- `EXECUTION_DOCKER_IMAGE`: imagen a usar (default `plataforma-practica-interactiva-runner:latest`)
- Limites opcionales:
  - `EXECUTION_DOCKER_CPUS` (default `0.5`)
  - `EXECUTION_DOCKER_MEMORY` (default `128m`)
  - `EXECUTION_DOCKER_PIDS` (default `64`)
  - El runner Docker se ejecuta con `--cap-drop ALL` y `--security-opt no-new-privileges`

### Límites y protecciones web (entorno público)

- `EXECUTION_ENABLED`:
  - default: `true`
  - si vale `0`, `false` o `no`, deshabilita temporalmente `/run` y responde `503`
  - útil como kill switch operativo sin redeploy de código
- Límite de requests de ejecución por cliente:
  - `RUN_RATE_LIMIT_WINDOW_SECONDS` (default `60`)
  - `RUN_RATE_LIMIT_MAX_REQUESTS`:
    - default local/dev: `20`
    - default producción: `8`
  - `RUN_RATE_LIMIT_MAX_TRACKED_CLIENTS`:
    - default local/dev: `5000`
    - default producción: `2000`
  - `TRUST_X_FORWARDED_PROTO` (default deshabilitado)
  - `TRUST_X_FORWARDED_FOR` (default deshabilitado)
  - `TRUSTED_PROXY_IPS` (lista de IPs confiables separadas por comas; aplica para `X-Forwarded-For` y `X-Forwarded-Proto`)
  - Recomendado: habilitar `TRUST_X_FORWARDED_FOR` y/o `TRUST_X_FORWARDED_PROTO` solo detrás de un reverse proxy confiable y configurando `TRUSTED_PROXY_IPS` (advertencia: si se activan y `TRUSTED_PROXY_IPS` queda vacío, la app puede confiar en headers enviados por clientes no confiables, inseguro para internet público)
- Límite global de ejecuciones simultáneas:
  - `RUN_MAX_CONCURRENT_EXECUTIONS`:
    - default local/dev: `4`
    - default producción: `1`
- Límite de tamaño de body para `/run`:
  - `RUN_MAX_REQUEST_BODY_BYTES` (default `65536`)
- CSP configurable:
  - `SECURITY_CONTENT_SECURITY_POLICY` (si no se define, se usa una política segura por defecto)

Correr sin Docker solo en local:

`EXECUTION_SANDBOX_PROVIDER=local uvicorn web.main:app --reload`

En PowerShell (Windows):

`$env:EXECUTION_SANDBOX_PROVIDER="local"; uvicorn web.main:app --reload`
