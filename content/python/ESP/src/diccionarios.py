##################################
# TEMA: CONJUNTOS Y DICCIONARIOS #
##################################


def hallar_repetidos(strings1, strings2):
    """
    Dadas dos listas de strings, retorna cuáles de esos strings están incluidos en ambas listas.
    Sugerencia didáctica: evitar iterar por las listas para lograr el cometido.
    Ejemplo:
        hallar_repetidos(strings1=["abc", "cde", "abc", "fff"], strings2=["cde", "aaa"]) -> {"cde"}
    -Parámetros:
        -strings1 (list; elementos: str): Lista con strings a procesar.
        -strings2 (list; elementos: str): Lista con strings a procesar.
    -Valor retornado:
        (set; elementos: str) Los strings que coinciden en `strings1` y `strings2`.
    """
    pass


def solo_una_mascota(perros, gatos):
    """
    Dada una lista de dueños de mascotas que tienen perros y otra lista de dueños que tienen gatos (donde un mismo
    nombre puede estar en ambas, en caso de tener ambas mascotas), retorna cuáles de esas personas tiene únicamente
    perro o únicamente gato, pero no ambos.
    Sugerencia didáctica: evitar iterar por las listas para lograr el cometido.
    Ejemplo:
         solo_una_mascota(perros=["Lucrecia Borges", "Juan Sebastián Balsa", "Cristóbal Colombraro"],
                          gatos=["Juan Sebastián Balsa", "Juan Jacobo Russo", "Ana Bologna", "Cristóbal Colombraro"])
        -> {"Lucrecia Borges", "Juan Jacobo Russo", "Ana Bologna"}
    -Parámetros:
        -perros (list; elementos: str): Lista con los nombres de dueños de perros.
        -gatos(list; elementos: str): Lista con los nombres de dueños de gatos.
    -Valor retornado:
        (set; elementos: str) Los nombres de aquellos dueños de mascota que solo tienen perros o solo tienen gatos
        pero no ambos.
    """
    pass


def elementos_unicos(tuplas):
    """
    Dada una cantidad indeterminada de tuplas que contienen números, retorna una tupla que combine todas las
    anteriores, pero donde cada número aparece una única vez (sin duplicados).
    Ejemplo:
        elementos_unicos(tuplas=[(1,2,3), (2,2,2,2), (3,4,5), (1,3,5,7,9)]) -> (1,2,3,4,5,7,9)
    -Parámetro:
        -tuplas (list; elementos: tuple, con elementos int): Lista conteniendo tuplas de números.
    -Valor retornado:
        (tuple; elementos: int) Tupla donde se combinan todos los números de las tuplas dadas, con una única
        ocurrencia de cada número.
    """
    pass


def listar_apellidos(alumnos):
    """
    Dada una lista conteniendo los nombres y apellidos de los alumnos de una institución, retorna una estructura que
    contiene los apellidos únicamente, sin repeticiones. Los nombres y apellidos de los alumnos están contenidos en un
    único string, separados por un espacio. Cada alumno puede tener más de un nombre pero solo un apellido, en la
    forma: "nombre(s) apellido".
    Ejemplo:
        listar_apellidos(alumnos=["Lara Ruiz", "Esteban Raúl Perez", "Francina Soto", "Lucas Perez"])
        -> {"Ruiz", "Perez", "Soto"}
    -Parámetro:
        -alumnos (list; elementos: str): Lista de alumnos.
    -Valor retornado:
        (set; elementos: str) Conjunto conteniendo los apellidos únicos en la lista alumnos.
    """
    pass


def agregar_pelicula(peliculas, pelicula):
    """
    Agrega datos de una película a un diccionario y lo retorna modificado. Si la película ya existe, la reemplaza con
    los nuevos datos. Los datos que se almacenan de cada película son: nombre, director, año de estreno. El diccionario
    usa el nombre de cada película como claves y una lista con el resto de datos como valor.
    Ejemplo:
        agregar_pelicula(peliculas={"Joker": ["Todd Phillips", 2019],
                                    "Avatar": ["James Cameron", 2009]},
                         pelicula=("Lord of the rings: The two towers", "Peter Jackson", 2002))
        -> {"Joker": ["Todd Phillips", 2019],
            "Avatar": ["James Cameron", 2009],
            "Lord of the rings: The two towers": ["Peter Jackson", 2002]}
    -Parámetros:
        -peliculas (dict; clave: str; valor: list, con 2 elementos: str, int): Diccionario de películas.
        -pelicula (tuple; 3 elementos: str, str, int): Tupla con los datos de la película a agregar: nombre,
        director, año de estreno.
    -Valor retornado:
        (dict; clave: str; valor: list, con 2 elementos: str, int) El diccionario `peliculas` con el nuevo dato agregado.
    """
    pass


def domicilios_facturacion(ventas):
    """
    Dada una lista con datos de las compras hechas por clientes de una empresa a lo largo de un mes, la cual contiene
    tuplas con información de cada venta: (nombre del cliente, día del mes, monto de la compra, domicilio del cliente),
    retorna los domicilios de cada cliente al cual se le debe enviar una factura de compra. Cada cliente puede haber
    hecho más de una compra en el mes, por lo que cada domicilio debe aparecer una sola vez.
    Ejemplo:
        domicilios_facturacion(ventas=[("Nuria Costa", 5, 12780.78, "Calle Las Flores 355"),
                                       (Jorge Russo", 7, 699, "Mirasol 218"),
                                       ("Nuria Costa", 7, 532.90, "Calle Las Flores 355"),
                                       ("Julián Rodriguez", 12, 5715.99, "La Mancha 761"),
                                       ("Jorge Russo", 15, 958, "Mirasol 218")])
        -> {'Calle Las Flores 355', 'Mirasol 218', 'La Mancha 761'}
    -Parámetro:
        -(list; elementos: tuple, con elementos heterogéneos) ventas: Lista con tuplas representando cada una de las
        ventas del mes.
    -Valor retornado:
        (set; elementos: str) Conjunto conteniendo los domicilios a los cuales se debe enviar la factura.
    """
    pass


def mas_votados(votos, curso):
    """
    Dado un diccionario con los votos que se hicieron para seleccionar al "mejor compañero" en los cursos de un
    instituto educativo, y dado un número de curso, retorna los nombres de todos los alumnos que fueron votados, sin
    repeticiones. El diccionario tiene como claves los números de los cursos y como valores listas de strings con cada
    voto. Si el número de curso dado no se encuentra en el diccionario, retorna un conjunto vacío.
    Ejemplo:
        mas_votados(votos={1:["juan", "juan", "lorena", "juan", "lorena", "paula"],
                           2:["romina", "marcos", "guadalupe", "guadalupe"],
                           3:["lucas", "abril", "lucas", "abril", "abril", "serena", "abril"]},
                    curso=3)
        -> {"lucas", "abril", "serena"}
    -Parámetros:
        -votos (dict; clave: int; valor: list, con elementos str): Diccionario con los votos de cada curso, donde las
        claves son los números de curso y los valores son listas conteniendo cada uno de los votos. 
        -curso (int): Número del curso del cual se buscarán los nombres de compañeros votados.
    -Valor retornado:
        (set; elementos: str) Conjunto con los nombres de los alumnos votados en el curso.
    """
    pass


def ocurrencias_digitos(digitos):
    """
    Dada una lista que contiene dígitos numéricos, informa la cantidad de ocurrencias de cada dígito, indicando el
    valor 0 para los dígitos (entre el 0 y el 9) que no se encuentran en la lista.
    Sugerencia didáctica: evitar el uso de collections.Counter().
    Ejemplo:
        ocurrencias_digitos(digitos=[8, 9, 0, 4, 2, 2, 4, 1, 8, 2]) -> {0:1, 1:1, 2:3, 3:0, 4:2, 5:0, 6:0, 7:0, 8:2, 9:1}
    -Parámetro:
        -digitos (list; elementos: int): Lista cuyos elementos son dígitos numéricos (entre el 0 y el 9).
    -Valor retornado:
        (dict; clave: int; valor: int) Diccionario contabilizando las ocurrencias de cada dígito, donde las claves son
        los dígitos del 0 al 9.
    """
    pass


def contar_ocurrencias(listas):
    """
    Dada una tupla que contiene listas de caracteres, cuenta la cantidad de ocurrencias de cada carácter en todas las
    listas.
    Ejemplo:
        contar_ocurrencias(listas=(["i", "%", "u"],
                                   ["^", "%", "^", "s", "i", "i", "u"],
                                   ["a", "u"]))
        -> {"i":3, "%":2, "u":3, "s":1, "^":2, "a":1}
    -Parámetro:
        -listas (tuple; elementos: list, con elementos str): Tupla conteniendo listas cuyos elementos son caracteres
        (strings de longitud 1).
    -Valor retornado: 
       (dict; clave: str; valor: int) Diccionario contabilizando las ocurrencias de cada letra.
    """
    pass


def mayor_valor(ocurrencias):
    """
    Dado un diccionario con valores únicos de tipo numérico positivos, retorna cuál es la clave que corresponde al
    mayor valor. Si el diccionario está vacío, retorna string vacío. Cada valor solo ocurre una vez en el diccionario.
    Sugerencia didáctica: evitar el uso de max().
    Ejemplo:
        mayor_valor(ocurrencias={"a":1, "e":7, "i":4, "o":9, "u":3}) -> "o"
    -Parámetro:
        -ocurrencias (dict; clave: str; valor: int): Diccionario cuyas claves son letras y los valores son las
        ocurrencias de cada una. Solo existe un único valor mayor que todos.
    -Valor retornado:
        (str) Clave que tiene asociado el mayor valor, o string vacío si el diccionario es vacío.
    """
    pass


def epoca_de_siembra(vegetales, mes):
    """
    Dado un diccionario conteniendo los meses de siembra de diversos vegetales y el nombre de un mes, retorna qué
    vegetales pueden sembrarse en ese mes. La lista retornada conserva el orden en que los vegetales aparecen como
    claves en el diccionario.
    Ejemplo:
        epoca_de_siembra(vegetales={"espinaca": ["febrero","marzo"],
                                    "ajo": ["febrero","marzo","abril"],
                                    "berenjena": ["julio","agosto","septiembre"]},
                         mes="marzo")
        -> ["espinaca", "ajo"]
    -Parámetros:
        -vegetales (dict; clave: str; valor: list, con elementos str): Diccionario donde las claves son los nombres de
        diversos vegetales y los valores son listas con los meses en que cada vegetal puede sembrarse. 
        -mes (str): El mes para el cual se busca saber qué vegetales pueden sembrarse.
    -Valor retornado:
        (list; elementos: str) Lista con los vegetales que pueden sembrarse en el mes, respetando el orden en que los
        vegetales aparecen como claves en el diccionario `vegetales`.
    """
    pass


def invertir_diccionario(diccionario):
    """
    Dado un diccionario donde las claves son strings y los valores son strings, retorna un nuevo diccionario donde las
    claves pasan a ser los valores y los valores pasan a ser las claves. Si un mismo valor aparece más de una vez en
    el diccionario original, en el resultado ese valor deberá asociarse a una lista con todas las claves que lo tenían.
    Ejemplos:
        invertir_diccionario({"a": "x", "b": "y", "c": "x"}) 
        -> {"x": ["a", "c"], "y": ["b"]}
    -Parámetro:
        -diccionario (dict; clave: str; valor: str): Diccionario cuyas claves son strings y los valores son strings.
        Los valores pueden repetirse en distintas claves.
    -Valor retornado:
        (dict; clave: str; valor: list, con elementos str) Diccionario donde las claves son los valores contenidos en
        'diccionario' pasado por parámetro, y los valores son las claves de `diccionario` pasado por parámetro.
    """
    pass


def asentar_pago(socios, numero):
    """
    Dado un diccionario con la información de socios de un club y el número de un socio, modifica el diccionario para
    indicar que ese socio tiene los pagos de la cuota social al día. El diccionario tiene como claves los números de
    socio y, como valores, listas con los datos del socio: [nombre, teléfono, estado de pagos (True si están al día,
    False en caso contrario)].
    Ejemplo:
        asentar_pago(socios={423:["Juana Saavedra", 4523114, True],
                             289:["Estela Gimenez", 6345112, False],
                             657:["Lautaro Ruiz", 4767992, False]},
                     numero=289)
        -> {423:["Juana Saavedra", 4523114, True],
            289:["Estela Gimenez", 6345112, True],
            657:["Lautaro Ruiz", 4767992, False]}
    -Parámetros:
        -socios (dict; clave: int; valor: list, con 3 elementos: str, int, bool): Diccionario con los datos de los 
        socios del club. Los números de socio son todos positivos.
        -numero (int): Número de socio a modificar.
    -Valor retornado:
        (dict; clave: int; valor: list, con 3 elementos: str, int, bool) Diccionario de socios en el cual se ha
        asentado el pago del socio correspondiente a numero, en caso de existir.
    """
    pass


def socios_morosos(socios):
    """
    Dado un diccionario con la información de socios de un club, retorna cuántos de ellos adeudan el pago de la cuota
    social. El diccionario tiene como claves los números de socio y, como valores, listas con los datos de ese socio:
    [nombre, teléfono, estado de pagos (True si están al día, False en caso contrario)].
    Ejemplo:
        socios_morosos(socios={423:["Juana Saavedra", 4523114, True],
                               289:["Estela Gimenez", 6345112, False],
                               657:["Lautaro Ruiz", 4767992, False]})
        -> 2
    -Parámetro:
        -socios (dict; clave: int; valor: list, con 3 elementos: str, int, bool): Diccionario con los datos de los
        socios del club. Las claves son todos números positivos.
    -Valor retornado:
        (int) Cantidad de socios que no tienen los pagos al día.
    """
    pass


def eliminar_socio(socios, nombre_socio):
    """
    Dado un diccionario con la información de socios de un club y el nombre de un socio, lo elimina del diccionario. El
    diccionario tiene como claves los números de socio y, como valores, listas con los datos de ese socio: [nombre,
    teléfono, estado de pagos (True si están al día, False en caso contrario)]. Si el nombre dado no corresponde a
    ningún socio, el diccionario no se modifica. 
    Ejemplo:
        eliminar_socio(socios={423:["Juana Saavedra", 4523114, True],
                               289:["Estela Gimenez", 6345112, False],
                               657:["Lautaro Ruiz", 4767992, False]},
                       nombre_socio="Estela Gimenez")
        -> {423:["Juana Saavedra", 4523114, True], 657:["Lautaro Ruiz", 4767992, False]}
    -Parámetros:
        -socios (dict; clave: int; valor: list, con 3 elementos: str, int, bool): Diccionario con los datos de los
        socios del club. Las claves son todos números positivos mayores que cero. Los nombres de socios no se repiten
        en los valores del diccionario.
        -nombre_socio (str): Nombre y apellido del socio a eliminar.
    -Valor retornado:
        (dict; clave: int; valor: list, con 3 elementos: str, int, bool) Diccionario de socios del cual se ha eliminado
        el socio, en caso de existir.
    """
    pass


def agrupar_por_longitud(cadenas):
    """
    Dada una lista de strings, los agrupa según su longitud. El resultado debe ser un diccionario donde:
    las claves son las longitudes (int), y los valores son listas con los strings que tienen esa longitud.
    El orden dentro de cada lista debe respetar el orden original.
    Ejemplo:
        agrupar_por_longitud(["a", "bb", "ccc", "dd", "e"])
        -> {1: ["a", "e"], 2: ["bb", "dd"], 3: ["ccc"]}
    -Parámetro:
        -cadenas (list; elementos: str): Lista de strings, de distintas longitudes.
    -Valor retornado:
        (dict; clave: int; valor: list, con elementos str) Diccionario donde las claves son números enteros que
        representan longitudes, y los valores son listas de los strings en `cadenas`, agrupados por longitud.
    """
    pass


def romano_a_arabigo(romano):
    """
    Dado un número romano, retorna su equivalente en números arábigos en base decimal (usando reglas simplificadas).
    Las equivalencias utilizadas son: I=1, V=5, X=10, L=50, C=100, D=500, M=1000.
    Reglas:
    Una letra repetida hasta 3 veces: se suma.
    I delante de V o X significa restar 1.
    X delante de L o C significa restar 10.
    C delante de D o M significa restar 100.
    Ejemplo:
        romano_a_arabigo(romano="MCMLXXIV") -> 1974
    -Parámetro:
        -romano (str): Número romano a convertir. En mayúsculas. Es un número romano válido. Su equivalente en arábigo
        está entre 1 y 3999.
    -Valor retornado:
        (int) Número arábigo en base 10, equivalente a `romano`.
    """
    pass


def numero_telefonico(telefono):
    """
    Dado un número de teléfono conteniendo letras, lo retorna con sus equivalentes en números. El número dado solo
    contendrá números, letras mayúsculas, '-', '(' y ')'. Solo se convertirán las letras, dejando los números y otros
    símbolos sin modificación.
    Las equivalencias utilizadas son:
    A-B-C=2;
    D-E-F=3;
    G-H-I=4;
    J-K-L=5;
    M-N-O=6;
    P-Q-R-S=7;
    T-U-V=8;
    W-X-Y-Z=9;
    Ejemplo:
        numero_telefonico(telefono="(325)444-TEST") -> "(325)444-8378"
    -Parámetro:
        -telefono (str): Un número telefónico que puede contener letras mayúsculas, números, guiones y paréntesis.
    -Valor retornado:
        (str) El número telefónico con sus letras convertidas a números.
    """
    pass


def cadenas_isomorficas(cadena1, cadena2):
    """
    Dados dos strings, define si son isomórficos o no. Dos strings, `a` y `b`, son isomórficos si puede reemplazarse
    cada carácter de `a` para obtener `b`. Todas las ocurrencias de un carácter deben ser reemplazadas con otro
    carácter, conservando su orden. No puede haber dos caracteres que sean reemplazados por el mismo carácter, pero sí
    es válido que un carácter se reemplace a sí mismo. Se asume que ambos strings tienen igual longitud y están
    compuestos por caracteres ascii válidos.
    Ejemplos:
        cadenas_isomorficas(cadena1="papel", cadena2="vivaz") -> True
        (Pues pueden hacerse los reemplazos 'p'='v'; 'a'='i'; 'p'='v'; 'e'='a'; 'l'='z').
        cadenas_isomorficas(cadena1="papel", cadena2="yoyos") -> False
        (Pues pueden hacerse los reemplazos 'p'='y'; 'a'='o'; 'p'='y'; pero al intentar reemplazar 'e'='o' sucede que
        la 'o' ya era reemplazo de la letra 'a').
    -Parámetros:
        -cadena1 (str): String a comparar. len(cadena1) == len(cadena2).
        -cadena2 (str): String para evaluar si es isomórfico con respecto `cadena1`.
    -Valor retornado:
        (bool) True si los strings son isomórficos, False si no lo son.
    """
    pass


def patron_de_palabras(patron, palabras):
    """
    Dado un patrón y un string compuesto por palabras, indica si el string sigue el patrón, de manera que
    haya una biyección entre cada letra del patrón y cada palabra del string. Se considera que el string "sigue" el
    patrón si cada letra del mismo puede reemplazarse con una palabra del string y una misma letra del patrón no
    reemplaza a dos palabras diferentes. Cada palabra del string debe tener una letra correspondiente en el
    patrón y cada letra del patrón debe corresponder a una palabra.
    Ejemplos:
        patron_de_palabras(patron="xyyx", palabras="casa mar mar casa") -> True
        (Pues puede asociarse 'x'='casa'; 'y'='mar').
        patron_de_palabras(patron="xyyx", palabras="casa mar mar cerro") -> False
        (Pues 'x' no puede asociarse al mismo tiempo con 'casa' y con 'cerro').
    -Parámetros:
        -patron (str): Patrón a verificar. Solo contiene letras minúsculas.
        -palabras (str): String con palabras. Las palabras estarán separadas por un único espacio y no habrá espacios
        al inicio ni al final del string. `palabras` contendrá solo letras minúsculas y el carácter ' '.
    -Valor retornado:
        (bool) True si las palabras del string siguen el patrón dado. False en caso contrario o si alguno de los
        strings es vacío.
    """
    pass
