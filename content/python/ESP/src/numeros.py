##################################
#        TEMA: NÚMEROS           #
##################################


def menor(numero1, numero2):
    """
    Retorna el menor de dos números.
    Ejemplos:
        menor(numero1=3, numero2=1) -> 1
        menor(numero1=3, numero2=3) -> 3
    -Parámetros:
        -numero1 (numérico): Uno de los números a procesar.
        -numero2 (numérico): Otro de los números a procesar.
    -Valor retornado:
        (numérico) El menor de los dos números. numero1 si ambos son iguales.
    """
    pass


def valor_absoluto(numero):
    """
    Retorna el valor absoluto de un número.
    Ejemplos:
        valor_absoluto(numero=3) -> 3
        valor_absoluto(numero=-10) -> 10
    -Parámetro:
        -numero (numérico): Número cuyo valor absoluto se retornará.
    -Valor retornado:
        (numérico) El valor absoluto de `numero`.
    """
    pass


def buscar_mes(fecha):
    """
    Dada una fecha completa (incluyendo día, mes y año), retorna el mes.
    Ejemplos:
        buscar_mes(fecha=31122020) -> 12
        buscar_mes(fecha=5091946) -> 9
    -Parámetros:
        -fecha (int): Fecha a procesar, con formato ddmmaaaa o dmmaaaa (donde las "d" indican los dígitos del día,
        las "m" indican los dígitos del mes y las "a" indican los dígitos del año). Positivo.
    -Valor retornado:
        (int) Mes contenido en `fecha`.
    """
    pass


def sumar_multiplos(inferior, superior, n):
    """
    Suma los múltiplos de n que se encuentran en un intervalo cerrado de números enteros.
    Ejemplos:
        sumar_multiplos(inferior=0, superior=30, n=5) -> 105
        sumar_multiplos(inferior=-30, superior=0, n=5) -> -105
    -Parámetros:
        -inferior (int): Límite inferior del intervalo. Menor o igual que superior.
        -superior (int): Límite superior del intervalo. Mayor o igual que inferior.
        -n (int): número cuyos múltiplos se sumarán. Distinto de 0.
    -Valor retornado:
        (int) La suma de los números múltiplos de `n` que se encuentran entre `inferior` y `superior` (inclusive).
    """
    pass


def es_capicua(numero):
    """
    Evalúa si un número es capicúa o no. Los números capicúa son aquellos que se leen de igual manera, tanto de
    izquierda a derecha como de derecha a izquierda.
    Sugerencia didáctica: usar números únicamente, evitando otros tipos de datos.
    Ejemplos:
        es_capicua(numero=123321) -> True
        es_capicua(numero=1234) -> False
    -Parámetros:
        -numero (int): Número a evaluar. Positivo.
    -Valor retornado:
        (bool) True si el número es capicúa, False si no lo es.
    """
    pass


def es_bisiesto(anio):
    """
    Evalúa si un año es bisiesto según el calendario Gregoriano.
    Ejemplos:
        es_bisiesto(anio=2020) -> True
        es_bisiesto(anio=1800) -> False
    -Parámetro:
        -anio (int): Año a evaluar. Número positivo.
    -Valor retornado:
        (bool) True si el año es bisiesto. False si no lo es.
    """
    pass


def dias_en_mes(mes, anio):
    """
    Calcula la cantidad de días que tiene un mes determinado, en un año determinado (para el caso de que se trate
    de febrero en un año bisiesto).
    Sugerencia didáctica: separar el problema en partes, usando un algoritmo que determine si un año es bisiesto.
    Ejemplo:
        dias_en_mes(mes=11, anio=1981) -> 30
    -Parámetros:
        -mes (int): Número representando al mes. Entre 1 y 12.
        -anio (int): Número representando al año. Positivo.
    -Valor retornado:
        (int) Cantidad de días que tiene el mes.
    """
    pass


def contar_digitos(numero):
    """
    Cuenta la cantidad de dígitos en un número.
    Ejemplo:
        contar_digitos(numero=120) -> 3
    -Parámetro:
        -numero (int): Número cuyos dígitos se contarán. Positivo.
    -Valor retornado:
        (int) Cantidad de dígitos en `numero`.
    """
    pass


def suma_digitos_cuadrados(numero):
    """
    Calcula la suma de los cuadrados de cada uno de los dígitos de un número.
    Ejemplo:
        suma_digitos_cuadrados(numero=15) -> 26
    -Parámetro:
        -numero (int): Número cuyos dígitos se procesarán. Positivo.
    -Valor retornado:
        (int) La suma de los cuadrados de los dígitos de `numero`.
    """
    pass


def porcentaje_digitos_pares(numero):
    """
    Calcula el porcentaje que representan los dígitos pares sobre el total de dígitos de un número.
    Ejemplo:
        porcentaje_digitos_pares(numero=5555666555) -> 30.0
    -Parámetro:
        -numero (int): Número cuyos dígitos se evaluarán. Positivo.
    -Valor retornado:
        (float) Porcentaje de dígitos pares en `numero` (de 0 a 100).
    """
    pass


def es_pronico(numero):
    """
    Evalúa si un número es un número "prónico". Un número es considerado "prónico" si es el producto de
    dos números naturales consecutivos.
    Ejemplo:
        es_pronico(numero=56) -> True
        (56 puede expresarse como 7*8).
    -Parámetro:
        -numero (int): Número a evaluar. Mayor que 0.
    -Valor retornado:
        (bool) True si `numero` es prónico, False si no lo es.
    """
    pass


def es_primo(numero):
    """
    Evalúa si un número es primo.
    Ejemplo:
        es_primo(numero=7) -> True
    -Parámetro:
        -numero (int): Número a evaluar. Positivo.
    -Valor retornado:
        (bool) True si `numero` es primo. False si no lo es.
    """
    pass


def factorial(numero):
    """
    Calcula el factorial de un número.
    Ejemplo:
        factorial(numero=4) -> 24
    -Parámetro:
        -numero (int): Número cuyo factorial se calculará. Positivo.
    -Valor retornado:
        (int) El factorial de `numero`.
    """
    pass


def suma_primeros_n_fibonacci(n):
    """
    Calcula la sumatoria de los primeros n números de la sucesión de Fibonacci.
    Se considera que los dos primeros números en la sucesión son 0 y 1.
    Ejemplo:
        suma_primeros_n_fibonacci(n=6) -> 12
    -Parámetros:
        -n (int): Cantidad de números Fibonacci a sumar. Mayor o igual que 2.
    -Valor retornado:
        (int) Sumatoria de los primeros `n` números de la sucesión de Fibonacci.
    """
    pass


def mayor_divisor(numero):
    """
    Calcula el mayor divisor entero de un número, exceptuando al propio número.
    Ejemplo:
        mayor_divisor(numero=182) -> 91
    -Parámetros:
        -numero (int): Número cuyo mayor divisor se calculará. Positivo.
    -Valor retornado:
        (int) Mayor número que divide a `numero` sin arrojar resto.
    """
    pass


def mcd_euclides(m, n):
    """
    Calcula el máximo común divisor entre m y n usando el algoritmo de Euclides.
    Método de Euclides: al dividir m por n (números enteros), se obtiene un cociente q y un residuo r. Se ha demostrado
    que el máximo común divisor de m y n es el mismo que el de n y r.
    Ejemplo:
        mcd_euclides(m=60, n=24) -> 12
    -Parámetros:
        -m (int): Número positivo.
        -n (int): Número entero no negativo.
    -Valor retornado:
        (int) Mayor divisor común entre `m` y `n`.
    """
    pass


def obtener_mes(dias_transcurridos, anio):
    """
    Obtiene el número de mes correspondiente, dada la cantidad de días transcurridos desde el 1 de enero de un año 
    en particular (teniendo en cuenta la posibilidad de que sea bisiesto).
    Sugerencia didáctica: separar el problema en partes, usando un algoritmo que obtenga la cantidad de días en un mes.
    Ejemplo:
        obtener_mes(dias_transcurridos=200, anio=1969) -> 7
        (el día consecutivo número 60 en un año bisiesto representa el 29 de febrero, mientras que en un año no
        bisiesto representa el 1 de marzo).
    -Parámetros:
        -dias_transcurridos (int): Número de días transcurridos desde el 1 de enero (entre 1 y 366). Positivo.
        -anio (int): Número de año (bisiesto o no). Positivo.
    -Valor retornado:
        (int) Número de mes (entre 1 y 12) correspondiente a `dias_transcurridos` en el `anio` dado.
    """
    pass


def es_disarium(numero):
    """
    Evalúa si un número es "disarium". Un número es considerado "disarium" si, elevando cada dígito a su respectiva
    posición dentro del número (la primera posición desde la izquierda se considera la 1) y luego sumando esos
    resultados, se obtiene el número original.
    Sugerencia didáctica: separar el problema en partes, usando un algoritmo para contar los digitos de un número.
    Ejemplo:
        es_disarium(numero=518) -> True
        (518 es un número disarium, ya que 5**1=5, 1**2=1, 8**3=512, y 5+1+512=518).
    -Parámetro:
        -numero (int): Número cuyos dígitos se procesarán. Positivo.
    -Valor retornado:
        (bool) True si `numero` es "disarium", False si no lo es.
    """
    pass


def ordenar_monedas(cantidad):
    """
    Indica cuántos "escalones" pueden formarse con una `cantidad` específica de monedas que se ordenarán en forma de
    "escalera", donde cada escalón "n" debe estar formado por exactamente "n" monedas. El último escalón puede estar
    incompleto.
    Ejemplo:
        ordenar_monedas(cantidad=5) -> 2
        (Con 5 monedas pueden formarse solo 2 escalones completos, ya que no hay suficientes para el tercero:
        ¤
        ¤ ¤
        ¤ ¤
        )
    -Parámetro:
        -cantidad (int): Cantidad de monedas a usar. Positivo.
    -Valor retornado:
        (int) Cantidad máxima de escalones completos que pueden formarse con la `cantidad` de monedas dada.
    """
    pass


def cantidad_unos_solos(numero):
    """
    Cuenta, de un número, la cantidad de dígitos 1 que no están seguidos de otro 1 consecutivo.
    Sugerencia didáctica: evitar convertir el número o sus dígitos a otros tipos de datos.
    Ejemplos:
        cantidad_unos_solos(numero=141211) -> 2
        cantidad_unos_solos(numero=11411211) -> 0
    -Parámetro:
        -numero (int): Número cuyos dígitos se evaluarán. Positivo.
    -Valor retornado:
        (int) Cantidad de dígitos 1 no consecutivos en `numero`.
    """
    pass
