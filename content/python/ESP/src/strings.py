##################################
#         TEMA: STRINGS          #
##################################


def cantidad_par_caracteres(cadena1, cadena2):
    """
    Indica si la cantidad de caracteres de dos strings (`cadena1` y `cadena2`) es par o no.
    Ejemplos:
        cantidad_par_caracteres(cadena1="aaaa", cadena2="aaaa") -> True
        cantidad_par_caracteres(cadena1="aaa", cadena2="aaaa") -> False
    -Parámetros:
        -cadena1 (str): Uno de los strings a procesar.
        -cadena2 (str): El otro string a procesar.
    -Valor retornado:
        (bool) True si la cantidad de caracteres de `cadena1` y la cantidad de caracteres de `cadena2` son, ambas,
        números pares. False si al menos uno de los dos strings tiene una cantidad impar de caracteres.
    """
    pass


def contar_ocurrencias(cadena, caracter):
    """
    Cuenta la cantidad de veces que `caracter` aparece en un `cadena`.
    Sugerencia didáctica: evitar el uso de count().
    Ejemplo:
        contar_ocurrencias(cadena="Esto es una frase", caracter="s") -> 3
    -Parámetros:
        -cadena (str): String donde contar ocurrencias de un carácter.
        -caracter (str): El carácter a contabilizar.
    -Valor retornado:
        (int) Cantidad de ocurrencias de `caracter` en `cadena`.
    """
    pass


def contar_vocales_totales(cadena):
    """
    Cuenta la cantidad de vocales (incluyendo repeticiones) que hay en el string `cadena`, teniendo en cuenta 
    mayúsculas como minúsculas. Las vocales del idioma español son: a, e, i, o, u.
    Sugerencia didáctica: evitar el uso de count().
    Ejemplo:
        contar_vocales_totales(cadena="Esto es una frase") -> 7
    -Parámetro:
        -cadena (str): String en el cual se contarán las vocales.
    -Valor retornado:
        (int) Cantidad total de vocales en `cadena`.
    """
    pass


def contar_vocales_unicas(cadena):
    """
    Cuenta la cantidad de vocales que hay en el string `cadena`. Cada vocal debe contarse una única vez, 
    indistintamente en su forma mayúscula o minúscula. Las vocales del idioma español son: a, e, i, o, u.
    Sugerencia didáctica: evitar el uso de count().
    Ejemplo:
        contar_vocales_unicas(cadena="Esto Es Una Frase") -> 4
    -Parámetro:
        -cadena (str): String en el cual se contarán las vocales.
    -Valor retornado:
        (int) Cantidad de vocales únicas en `cadena`.
    """
    pass


def reemplazar_caracter_con_asterisco(cadena, caracter):
    """
    Dado el string `cadena`, reemplaza por '*' a todas las ocurrencias de `caracter`.
    Sugerencia didáctica: evitar el uso de replace().
    Ejemplos:
        reemplazar_caracter_con_asterisco(cadena="esto es una frase", caracter="a") -> "esto es un* fr*se"
    -Parámetros:
        -cadena (str): El string donde se harán los reemplazos.
        -caracter (str): El carácter a reemplazar.
    -Valor retornado:
        (str) Un nuevo string con el contenido de `cadena`, donde todas las ocurrencias de `caracter` fueron
        reemplazadas por '*'.
    """
    pass


def invertir_cadena(cadena):
    """
    Invierte el orden de los caracteres del string `cadena`.
    Sugerencia didáctica: evitar usar rebanadas con paso negativo.
    Ejemplo:
        invertir_cadena(cadena="Esto es una frase!") -> "!esarf anu se otsE"
    -Parámetro:
        -cadena (str): String a invertir.
    -Valor retornado:
        (str) Un nuevo string con los caracteres de `cadena` en el orden inverso.
    """
    pass


def reemplazar_simbolos(cadena, nuevo_caracter):
    """
    Reemplaza todos los símbolos del string `cadena` por el carácter dado en `nuevo_caracter`.
    Se consideran "símbolos" a los caracteres que no son letras, dígitos ni espacios.
    Ejemplo:
        reemplazar_simbolos(cadena="--Esto es 1 frase donde reemplazaremos con @ cada símbolo", nuevo_caracter="@")
        -> "@@Esto es 1 frase donde reemplazaremos con @ cada símbolo"
    -Parámetros:
        -cadena (str): String donde se efectuarán los reemplazos.
    -Valor retornado:
        (str) Un string donde cada símbolo ha sido reemplazado por `nuevo_caracter`.
    """
    pass


def porcentaje_digitos_numericos(cadena):
    """
    Retorna el porcentaje que representan los dígitos numéricos sobre el total de caracteres del string `cadena`.
    Solo se retorna el número que representa el porcentaje, sin el símbolo % y sin redondear (en caso de tener
    decimales).
    Ejemplos:
        porcentaje_digitos_numericos(cadena="Tenemos 1 dígito") -> 6.25
        porcentaje_digitos_numericos(cadena="1984") -> 100
    -Parámetro:
        -cadena (str): String a procesar, que puede o no contener dígitos numéricos.
    -Valor retornado:
        (numérico) Porcentaje (número entre 0 y 100) de caracteres numéricos que posee `cadena`, sobre su cantidad
        total de caracteres.
    """
    pass


def clasificar_cadena_numerica(cadena):
    """
    Recibe un número en forma de string (`cadena`) y retorna un nuevo string, conteniendo los caracteres que
    representan dígitos múltiplos de 2 y dígitos múltiplos de 3, ambos grupos separados por un '$'. Si un dígito es
    múltiplo de 2 y de 3 al mismo tiempo, aparecerá a ambos lados del símbolo '$'.
    Ejemplo:
        clasificar_cadena_numerica(cadena="123456") -> "246$36"
        clasificar_cadena_numerica(cadena="2222") -> "2222$"
    -Parámetro:
        -cadena (str): String numérico a procesar. El string solo contendrá dígitos numéricos.
    -Valor retornado:
        (str) Nuevo string compuesto por la concatenación de los caracteres de `cadena` que son múltiplos de 2 (en su
        representación numérica), seguidos de un '$' a continuación, seguidos de  la concatenación de los caracteres
        de `cadena` que son múltiplos de 3.
    """
    pass


def caracteres_centrales(cadena):
    """
    Dado un string `cadena` de longitud impar, retorna los 3 caracteres centrales. Hay al menos 5 caracteres en
    el string `cadena`.
    Ejemplos:
        caracteres_centrales(cadena="AbcDefGhi") -> "Def"
        caracteres_centrales(cadena="A   A") -> "   "
    -Parámetro:
        -cadena (str) String a procesar. Tendrá 5 o más caracteres y su longitud será impar.
    -Valor retornado:
        (str) String de longitud 3 conteniendo los caracteres ubicados en el medio de `cadena`.
    """    
    pass


def es_palindromo(cadena):
    """
    Verifica si un string `cadena` es palíndromo, independientemente de mayúsculas y minúsculas.
    Se incluyen todos los caracteres, sean o no letras.
    Las letras acentuadas se consideran como caracteres diferentes de sus contrapartes no acentuadas.
    El string vacío no se considera palíndromo.
    Sugerencia didáctica: evitar las rebanadas con paso negativo y el uso de reversed().
    Ejemplos:
        es_palindromo(cadena="abba") -> True
        es_palindromo(cadena="baéceab") -> False
    -Parámetro:
        -cadena (str): El string a procesar.
    -Valor retornado:
        (bool) True si `cadena` es palíndromo. False si no lo es.
    """
    pass


def incluye_caracteres(cadena1, cadena2):
    """
    Indica si el string `cadena2` incluye todos los caracteres que componen al string `cadena1`.
    El orden de los caracteres no se tiene en cuenta.
    Se considera a la versión mayúscula y minúscula de una misma letra como caracteres diferentes.
    `cadena1` puede contener caracteres repetidos y, en ese caso, cuentan como un único carácter a buscar en `cadena2`.
    Ejemplos:
        incluye_caracteres(cadena1="super", cadena2="supermercado") -> True
        incluye_caracteres(cadena1="aaa", cadena2="rosa") -> True
    -Parámetros:
        -cadena1 (str): String cuyos caracteres deben buscarse en `cadena2`.
        -cadena2 (str): String donde se buscarán los caracteres de `cadena1`.
    -Valor retornado:
        (bool) True si `cadena2` incluye todos los caracteres de `cadena1`. False si no incluye a todos.
    """
    pass


def son_anagrama(cadena1, cadena2):
    """
    Indica si el string `cadena1` es un anagrama de `cadena2`.
    No se tienen en cuenta mayúsculas y minúsculas pero sí las repeticiones de letras.
    Los strings a comparar solo contendrán letras.
    Ejemplos:
        son_anagrama(cadena1="aval", cadena2="lava") -> True
        son_anagrama(cadena1="aval", cadena2="lavar") -> False
    -Parámetros:
        -cadena1 (str): String a procesar, para saber si es anagrama de `cadena2`.
        -cadena2 (str): String a procesar, para saber si es anagrama de `cadena1`.
    -Valor retornado:
        (bool) True si ambos strings son anagramas entre sí. False si no lo son.
    """
    pass


def cuantos_eliminar_para_anagrama(cadena1, cadena2):
    """
    Indica cuántos caracteres deben eliminarse para que `cadena1` y `cadena2` sean anagramas.
    No se tienen en cuenta mayúsculas y minúsculas pero sí las repeticiones de letras.
    Los strings a comparar solo contendrán letras.
    Ejemplo:
        cuantos_eliminar_para_anagrama(cadena1="avala", cadena2="lavar") -> 2
    -Parámetros:
        -cadena1 (str): Uno de los strings a procesar.
        -cadena2 (str): Otro string a procesar.
    -Valor retornado:
        (int) Cantidad de caracteres que deberían eliminarse para que ambos strings sean anagramas.
    """
    pass


def invertir_palabras(cadena):
    """
    Invierte los caracteres de cada palabra en el string `cadena`.
    Separador de palabras: un único espacio.
    El string no contendrá espacios al principio ni al final. Puede contener símbolos o dígitos y en ese caso se
    considerarán de la misma forma que las letras.
    Sugerencia didáctica: evitar el uso de split().
    Ejemplo:
        invertir_palabras(cadena="Esto es una frase.") -> "otsE se anu .esarf"
    -Parámetros:
        -cadena (str): String formado por palabras que serán invertidas.
    -Valor retornado:
        (str) Un nuevo string donde cada palabra de `cadena` se encuentra invertida, sin modificar su posición
        original dentro de `cadena`.
    """
    pass


def longitud_ultima_palabra(cadena):
    """
    Retorna la longitud de la última palabra de un string `cadena`.
    Separador de palabras: uno o más espacios.
    Ejemplos:
        longitud_ultima_palabra(cadena="esto es una frase") -> 5
        longitud_ultima_palabra(cadena="   espacios   ") -> 8
    -Parámetro:
        -cadena (str): String compuesto por letras y espacios.
    -Valor retornado:
        (int) Cantidad de caracteres de la última palabra de `cadena`.
    """
    pass


def convertir_a_titulo(cadena):
    """
    Convierte la primera letra de cada palabra del string `cadena` a mayúsculas y el resto a minúsculas.
    Separador de palabras: cualquier símbolo (excluyendo letras y números), excepto apóstrofos.
    No debe modificarse la cantidad de espacios.
    Sugerencia didáctica: evitar el uso de title().
    Ejemplos:
        convertir_a_titulo(cadena="esto es una frase") -> "Esto Es Una Frase"
        convertir_a_titulo(cadena="ESTO ES UNA FRASE") -> "Esto Es Una Frase"
    -Parámetro:
        -cadena (str): String a convertir.
    -Valor retornado:
        (str) Un nuevo string con el contenido de `cadena`, donde la primera letra de cada palabra es mayúscula y el
        resto son minúsculas.
    """
    pass


def cifrar_cesar(cadena, n):
    """
    Reemplaza cada letra del string `cadena` por otra del alfabeto, que se encuentre `n` posiciones hacia la derecha.
    Los corrimientos son circulares (si el alfabeto termina antes de poder correr la cantidad de lugares necesarios,
    se vuelve a comenzar desde la letra "a").
    La cadena puede contener letras minúsculas, símbolos y dígitos. El cifrado solo se realizará sobre las letras,
    dejando al resto de caracteres sin modificación.
    La cantidad de corrimientos (n) será un número entre 1 y 27.
    Ejemplos:
        cifrar_cesar(cadena="esto es una frase", n=2) -> "guvq gu woc htcug"
        cifrar_cesar(cadena="abc123 xyz987!", n=4) -> "efg123 bcd987!"
    -Parámetros:
        -cadena (str): String a cifrar.
        -n (int): Cantidad de posiciones que se moverá cada carácter dentro del alfabeto español de 27 letras.
    -Valor retornado:
        (str) Un nuevo string donde cada letra de `cadena` ha sido reemplazado por otra del alfabeto, ubicada `n`
        posiciones hacia la derecha.
    """
    pass


def rotar_n_posiciones(cadena, n):
    """
    Dado un string `cadena`, rota cada carácter `n` posiciones a la derecha, en forma circular (volviendo al principio
    al llegar al final).
    Los caracteres pueden ser letras, dígitos o símbolos.
    `n` no está necesariamente limitado a la longitud de cadena (puede ser mayor).
    Ejemplos:
        rotar_n_posiciones(cadena="Esto es una frase", n=6) -> " fraseEsto es una"
        rotar_n_posiciones(cadena="palabra", n=3) -> "brapala"
    -Parámetros:
        -cadena (str): String a partir del cual se producirán las rotaciones.
        -n (int): Cantidad de posiciones que se moverá cada carácter dentro del string.
    -Valor retornado:
        (str) Un nuevo string donde cada carácter de `cadena` se ha desplazado `n` posiciones hacia la derecha.
    """
    pass


def comprimir_RLE(cadena):
    """
    Comprime al string `cadena` utilizando la codificación RLE ("Run-Length Encoding").
    RLE: por cada grupo de caracteres consecutivos repetidos, se almacenará una única ocurrencia del carácter,
    seguida del número de ocurrencias en caso de que sea mayor que 1 (ejemplo: 'aaab' se comprime como 'a3b').
    El string solo estará compuesto por letras y/o símbolos.
    Ejemplos:
        comprimir_RLE(cadena="aaabbc") -> "a3b2c"
        comprimir_RLE(cadena="abcde") -> "abcde"
    -Parámetro:
        -cadena (str): String a comprimir.
    -Valor retornado:
        (str) String `cadena` comprimido mediante RLE.
    """
    pass
