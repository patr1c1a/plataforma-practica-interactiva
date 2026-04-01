#############################
# NO MODIFICAR ESTE ARCHIVO #
#############################

import unittest
from src.strings import *


class TestsFuncionesStrings(unittest.TestCase):

    def test_cantidad_par_caracteres(self):
        pruebas = {
            "Argumentos usados: cadena1='aaa', cadena2='aaa'": [
                cantidad_par_caracteres("aaa", "aaa"),
                False,
            ],
            "Argumentos usados: cadena1='aaa', cadena2='aaaa'": [
                cantidad_par_caracteres("aaa", "aaaa"),
                False,
            ],
            "Argumentos usados: cadena1='aaaa', cadena2='aaa'": [
                cantidad_par_caracteres("aaaa", "aaa"),
                False,
            ],
            "Argumentos usados: cadena1='aaaa', cadena2='aaaa'": [
                cantidad_par_caracteres("aaaa", "aaaa"),
                True,
            ],
            "Argumentos usados: cadena1='', cadena2='aaaa'": [
                cantidad_par_caracteres("", "aaaa"),
                True,
            ],
            "Argumentos usados: cadena1='aaaa', cadena2=''": [
                cantidad_par_caracteres("aaaa", ""),
                True,
            ],
            "Argumentos usados: cadena1='', cadena2=''": [
                cantidad_par_caracteres("", ""),
                True,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_contar_ocurrencias(self):
        pruebas = {
            "Argumentos usados: cadena='Esto es una frase', caracter='s'": [
                contar_ocurrencias("Esto es una frase", "s"),
                3,
            ],
            "Argumentos usados: cadena='Esto es una frase', caracter='x'": [
                contar_ocurrencias("Esto es una frase", "x"),
                0,
            ],
            "Argumentos usados: cadena='Esto es una frase', caracter='e'": [
                contar_ocurrencias("Esto es una frase", "e"),
                2,
            ],
            "Argumentos usados: cadena='Esto es una frase', caracter='E'": [
                contar_ocurrencias("Esto es una frase", "E"),
                1,
            ],
            "Argumentos usados: cadena='', caracter='a'": [
                contar_ocurrencias("", "a"),
                0,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_contar_vocales_totales(self):
        pruebas = {
            "Argumento usado: cadena='Esto es una frase'": [
                contar_vocales_totales("Esto es una frase"),
                7,
            ],
            "Argumento usado: cadena='aeiou'": [contar_vocales_totales("aeiou"), 5],
            "Argumento usado: cadena='AEIOU'": [contar_vocales_totales("AEIOU"), 5],
            "Argumento usado: cadena='abcdEfgHijkLMnOPqrsTuVwXyz'": [
                contar_vocales_totales("abcdEfgHijkLMnOPqrsTuVwXyz"),
                5,
            ],
            "Argumento usado: cadena='zzz'": [contar_vocales_totales("zzz"), 0],
            "Argumento usado: cadena='123'": [contar_vocales_totales("123"), 0],
            "Argumento usado: cadena=''": [contar_vocales_totales(""), 0],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_contar_vocales_unicas(self):
        pruebas = {
            "Argumento usado: cadena='Esto Es Una Frase'": [
                contar_vocales_unicas("Esto Es Una Frase"),
                4,
            ],
            "Argumento usado: cadena='aeiou'": [contar_vocales_unicas("aeiou"), 5],
            "Argumento usado: cadena='aeiouAEIOU'": [
                contar_vocales_unicas("aeiouAEIOU"),
                5,
            ],
            "Argumento usado: cadena='aaeeiioouuAAEEIIOOUU'": [
                contar_vocales_unicas("aeiouAEIOU"),
                5,
            ],
            "Argumento usado: cadena='abcdEfgHijkLMnOPqrsTuVwXyz'": [
                contar_vocales_unicas("abcdEfgHijkLMnOPqrsTuVwXyz"),
                5,
            ],
            "Argumento usado: cadena='zzz'": [contar_vocales_unicas("zzz"), 0],
            "Argumento usado: cadena='123'": [contar_vocales_unicas("123"), 0],
            "Argumento usado: cadena=''": [contar_vocales_unicas(""), 0],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_reemplazar_caracter_con_asterisco(self):
        pruebas = {
            "Argumentos usados: cadena='esto es una frase', caracter='a'": [
                reemplazar_caracter_con_asterisco("esto es una frase", "a"),
                "esto es un* fr*se",
            ],
            "Argumentos usados: cadena='esto es una frase', caracter='u'": [
                reemplazar_caracter_con_asterisco("esto es una frase", "u"),
                "esto es *na frase",
            ],
            "Argumentos usados: cadena='Esto es una frase', caracter='E'": [
                reemplazar_caracter_con_asterisco("Esto es una frase", "E"),
                "*sto es una frase",
            ],
            "Argumentos usados: cadena='esto es una frase', caracter='z'": [
                reemplazar_caracter_con_asterisco("esto es una frase", "z"),
                "esto es una frase",
            ],
            "Argumentos usados: cadena='esto es una frase', caracter=''": [
                reemplazar_caracter_con_asterisco("esto es una frase", ""),
                "esto es una frase",
            ],
            "Argumentos usados: cadena='', caracter='a'": [
                reemplazar_caracter_con_asterisco("", "a"),
                "",
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_invertir_cadena(self):
        pruebas = {
            "Argumento usado: cadena='Esto es una frase!'": [
                invertir_cadena("Esto es una frase!"),
                "!esarf anu se otsE",
            ],
            "Argumento usado: cadena='aaaa'": [invertir_cadena("aaaa"), "aaaa"],
            "Argumento usado: cadena='a'": [invertir_cadena("a"), "a"],
            "Argumento usado: cadena=''": [invertir_cadena(""), ""],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_reemplazar_simbolos(self):
        pruebas = {
            "Argumentos usados: cadena='--Esto es 1 frase donde reemplazaremos con @ cada símbolo', "
            "nuevo_caracter='@'": [
                reemplazar_simbolos(
                    "--Esto es 1 frase donde reemplazaremos con @ cada símbolo", "@"
                ),
                "@@Esto es 1 frase donde reemplazaremos con @ cada símbolo",
            ],
            "Argumentos usados: cadena='Esto es una frase', nuevo_caracter='*'": [
                reemplazar_simbolos("Esto es una frase", "*"),
                "Esto es una frase",
            ],
            "Argumentos usados: cadena='Esto es una frase!', nuevo_caracter='-'": [
                reemplazar_simbolos("Esto es una frase!", "-"),
                "Esto es una frase-",
            ],
            "Argumentos usados: cadena='/$Esto/ es@ una# frase=', nuevo_caracter='@'": [
                reemplazar_simbolos("/$Esto/ es@ una# frase=", "@"),
                "@@Esto@ es@ una@ frase@",
            ],
            "Argumentos usados: cadena='1234', nuevo_caracter='}'": [
                reemplazar_simbolos("1234", "}"),
                "1234",
            ],
            "Argumentos usados: cadena='@@@', nuevo_caracter='@'": [
                reemplazar_simbolos("@@@", "@"),
                "@@@",
            ],
            "Argumentos usados: cadena=' ', nuevo_caracter='*'": [
                reemplazar_simbolos(" ", "*"),
                " ",
            ],
            "Argumentos usados: cadena='', nuevo_caracter='*'": [
                reemplazar_simbolos("", "*"),
                "",
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_porcentaje_digitos_numericos(self):
        pruebas = {
            "Argumento usado: cadena='Tenemos 1 dígito'": [
                porcentaje_digitos_numericos("Tenemos 1 dígito"),
                6.25,
            ],
            "Argumento usado: cadena='1984'": [
                porcentaje_digitos_numericos("1984"),
                100,
            ],
            "Argumento usado: cadena='Esto es una frase'": [
                porcentaje_digitos_numericos("Esto es una frase"),
                0,
            ],
            "Argumento usado: cadena=''": [porcentaje_digitos_numericos(""), 0],
            "Argumento usado: cadena='abc1'": [
                porcentaje_digitos_numericos("abc1"),
                25,
            ],
            "Argumento usado: cadena='Matemática: 10'": [
                porcentaje_digitos_numericos("Matemática: 10"),
                14.285714285714286,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_clasificar_cadena_numerica(self):
        pruebas = {
            "Argumento usado: cadena='123456'": [
                clasificar_cadena_numerica("123456"),
                "246$36",
            ],
            "Argumento usado: cadena='2222'": [
                clasificar_cadena_numerica("2222"),
                "2222$",
            ],
            "Argumento usado: cadena='1234567890'": [
                clasificar_cadena_numerica("1234567890"),
                "24680$3690",
            ],
            "Argumento usado: cadena='3333'": [
                clasificar_cadena_numerica("3333"),
                "$3333",
            ],
            "Argumento usado: cadena='6666'": [
                clasificar_cadena_numerica("6666"),
                "6666$6666",
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_caracteres_centrales(self):
        pruebas = {
            "Argumento usado: cadena='AbcDefGhi'": [
                caracteres_centrales("AbcDefGhi"),
                "Def",
            ],
            "Argumento usado: cadena='A   A'": [caracteres_centrales("A   A"), "   "],
            "Argumento usado: cadena='bAAAb'": [caracteres_centrales("bAAAb"), "AAA"],
            "Argumento usado: cadena='AAAAA'": [caracteres_centrales("AAAAA"), "AAA"],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_es_palindromo(self):
        pruebas = {
            "Argumento usado: cadena='abba'": [es_palindromo("abba"), True],
            "Argumento usado: cadena='baéceab'": [es_palindromo("baéceab"), False],
            "Argumento usado: cadena='aba'": [es_palindromo("aba"), True],
            "Argumento usado: cadena='aa'": [es_palindromo("aa"), True],
            "Argumento usado: cadena='a'": [es_palindromo("a"), True],
            "Argumento usado: cadena=''": [es_palindromo(""), False],
            "Argumento usado: cadena='Aba'": [es_palindromo("Aba"), True],
            "Argumento usado: cadena='ab'": [es_palindromo("ab"), False],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_incluye_caracteres(self):
        pruebas = {
            "Argumentos usados: cadena1='super', cadena2='supermercado'": [
                incluye_caracteres("super", "supermercado"),
                True,
            ],
            "Argumentos usados: cadena1='aaa', cadena2='rosa'": [
                incluye_caracteres("aaa", "rosa"),
                True,
            ],
            "Argumentos usados: cadena1='abc', cadena2='abecedario'": [
                incluye_caracteres("abc", "abecedario"),
                True,
            ],
            "Argumentos usados: cadena1='e', cadena2='celular'": [
                incluye_caracteres("e", "celular"),
                True,
            ],
            "Argumentos usados: cadena1='abcf', cadena2='abecedario'": [
                incluye_caracteres("abcf", "abecedario"),
                False,
            ],
            "Argumentos usados: cadena1='Plt', cadena2='pelota'": [
                incluye_caracteres("Plt", "pelota"),
                False,
            ],
            "Argumentos usados: cadena1='Plt', cadena2='Pelota'": [
                incluye_caracteres("Plt", "Pelota"),
                True,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_son_anagrama(self):
        pruebas = {
            "Argumentos usados: cadena1='aval', cadena2='lava'": [
                son_anagrama("aval", "lava"),
                True,
            ],
            "Argumentos usados: cadena1='aval', cadena2='lavar'": [
                son_anagrama("aval", "lavar"),
                False,
            ],
            "Argumentos usados: cadena1='aaa', cadena2='aaa'": [
                son_anagrama("aaa", "aaa"),
                True,
            ],
            "Argumentos usados: cadena1='Aaa', cadena2='aaa'": [
                son_anagrama("aaa", "aaa"),
                True,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_cuantos_eliminar_para_anagrama(self):
        pruebas = {
            "Argumentos usados: cadena1='avala', cadena2='lavar'": [
                cuantos_eliminar_para_anagrama("avala", "lavar"),
                2,
            ],
            "Argumentos usados: cadena1='aval', cadena2='lava'": [
                cuantos_eliminar_para_anagrama("aval", "lava"),
                0,
            ],
            "Argumentos usados: cadena1='aval', cadena2='lavar'": [
                cuantos_eliminar_para_anagrama("aval", "lavar"),
                1,
            ],
            "Argumentos usados: cadena1='avala', cadena2='lava'": [
                cuantos_eliminar_para_anagrama("avala", "lava"),
                1,
            ],
            "Argumentos usados: cadena1='AVAL', cadena2='lavaran'": [
                cuantos_eliminar_para_anagrama("AVAL", "lavaran"),
                3,
            ],
            "Argumentos usados: cadena1='aval', cadena2='LAVA'": [
                cuantos_eliminar_para_anagrama("aval", "LAVA"),
                0,
            ],
            "Argumentos usados: cadena1='abc', cadena2='def'": [
                cuantos_eliminar_para_anagrama("abc", "def"),
                6,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_invertir_palabras(self):
        pruebas = {
            "Argumentos usados: cadena='Esto es una frase.'": [
                invertir_palabras("Esto es una frase."),
                "otsE se anu .esarf",
            ],
            "Argumentos usados: cadena='otsE se anu !esarf'": [
                invertir_palabras("otsE se anu !esarf"),
                "Esto es una frase!",
            ],
            "Argumentos usados: cadena='palabra'": [
                invertir_palabras("palabra"),
                "arbalap",
            ],
            "Argumentos usados: cadena='123'": [invertir_palabras("123"), "321"],
            "Argumentos usados: cadena='a b c'": [invertir_palabras("a b c"), "a b c"],
            "Argumentos usados: cadena=''": [invertir_palabras(""), ""],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_longitud_ultima_palabra(self):
        pruebas = {
            "Argumento usado: cadena='esto es una frase'": [
                longitud_ultima_palabra("esto es una frase"),
                5,
            ],
            "Argumento usado: cadena='   espacios   '": [
                longitud_ultima_palabra("   espacios   "),
                8,
            ],
            "Argumento usado: cadena='palabra'": [
                longitud_ultima_palabra("palabra"),
                7,
            ],
            "Argumento usado: cadena='   esto   es   una   frase   '": [
                longitud_ultima_palabra("   esto   es   una   frase   "),
                5,
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_convertir_a_titulo(self):
        pruebas = {
            "Argumento usado: cadena='esto es una frase'": [
                convertir_a_titulo("esto es una frase"),
                "Esto Es Una Frase",
            ],
            "Argumento usado: cadena='ESTO ES UNA FRASE'": [
                convertir_a_titulo("ESTO ES UNA FRASE"),
                "Esto Es Una Frase",
            ],
            "Argumento usado: cadena='Esto Es Una Frase'": [
                convertir_a_titulo("Esto Es Una Frase"),
                "Esto Es Una Frase",
            ],
            "Argumento usado: cadena='palabra'": [
                convertir_a_titulo("palabra"),
                "Palabra",
            ],
            "Argumento usado: cadena='Palabra'": [
                convertir_a_titulo("Palabra"),
                "Palabra",
            ],
            "Argumento usado: cadena='    esto es una frase'": [
                convertir_a_titulo("    esto es una frase"),
                "    Esto Es Una Frase",
            ],
            "Argumento usado: cadena='esto es una frase   '": [
                convertir_a_titulo("esto es una frase   "),
                "Esto Es Una Frase   ",
            ],
            "Argumento usado: cadena='esto   es   una   frase'": [
                convertir_a_titulo("esto   es   una   frase"),
                "Esto   Es   Una   Frase",
            ],
            "Argumento usado: cadena='1esto 2es 3una 4frase'": [
                convertir_a_titulo("1esto 2es 3una 4frase"),
                "1Esto 2Es 3Una 4Frase",
            ],
            "Argumento usado: cadena='esto1 es2 una3 frase4'": [
                convertir_a_titulo("esto1 es2 una3 frase4"),
                "Esto1 Es2 Una3 Frase4",
            ],
            "Argumento usado: cadena='e1s2t3o4 e1s2 u1n2a3 f1r2a3s4e5'": [
                convertir_a_titulo("e1s2t3o4 e1s2 u1n2a3 f1r2a3s4e5"),
                "E1s2t3o4 E1s2 U1n2a3 F1r2a3s4e5",
            ],
            "Argumento usado: cadena='esto_es_una_frase'": [
                convertir_a_titulo("esto_es_una_frase"),
                "Esto_Es_Una_Frase",
            ],
            "Argumento usado: cadena='They're my best friend's siblings'": [
                convertir_a_titulo("They're my best friend's siblings"),
                "They're My Best Friend's Siblings",
            ],
            "Argumento usado: cadena=''": [convertir_a_titulo(""), ""],
            "Argumento usado: cadena=' '": [convertir_a_titulo(" "), " "],
            "Argumento usado: cadena='123'": [convertir_a_titulo("123"), "123"],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_cifrar_cesar(self):
        pruebas = {
            "Argumentos usados: cadena='esto es una frase', n=2": [
                cifrar_cesar("esto es una frase", 2),
                "guvq gu woc htcug",
            ],
            "Argumentos usados: cadena='abc123 xyz987!', n=4": [
                cifrar_cesar("abc123 xyz987!", 4),
                "efg123 bcd987!",
            ],
            "Argumentos usados: cadena='esto es una frase', n=6": [
                cifrar_cesar("esto es una frase", 6),
                "kyzu ky asg lxgyk",
            ],
            "Argumentos usados: cadena='123', n=8": [cifrar_cesar("123", 8), "123"],
            "Argumentos usados: cadena='esto es una frase', n=27": [
                cifrar_cesar("esto es una frase", 27),
                "esto es una frase",
            ],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_rotar_n_posiciones(self):
        pruebas = {
            "Argumentos usados: cadena='Esto es una frase', n=6": [
                rotar_n_posiciones("Esto es una frase", 6),
                " fraseEsto es una",
            ],
            "Argumentos usados: cadena='palabra', n=3": [
                rotar_n_posiciones("palabra", 3),
                "brapala",
            ],
            "Argumentos usados: cadena='palabra', n=10": [
                rotar_n_posiciones("palabra", 10),
                "brapala",
            ],
            "Argumentos usados: cadena='Esto es una frase', n=0": [
                rotar_n_posiciones("Esto es una frase", 0),
                "Esto es una frase",
            ],
            "Argumentos usados: cadena='palabra', n=7": [
                rotar_n_posiciones("palabra", 7),
                "palabra",
            ],
            "Argumentos usados: cadena='', n=5": [rotar_n_posiciones("", 5), ""],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)

    def test_comprimir_RLE(self):
        pruebas = {
            "Argumento usado: cadena='aaabbc'": [comprimir_RLE("aaabbc"), "a3b2c"],
            "Argumento usado: cadena='abcde'": [comprimir_RLE("abcde"), "abcde"],
            "Argumento usado: cadena='abbccc'": [comprimir_RLE("abbccc"), "ab2c3"],
            "Argumento usado: cadena='a'": [comprimir_RLE("a"), "a"],
            "Argumento usado: cadena='aaaa'": [comprimir_RLE("aaaa"), "a4"],
            "Argumento usado: cadena='Aaaa'": [comprimir_RLE("Aaaa"), "Aa3"],
            "Argumento usado: cadena='a$bb&&&&&c'": [
                comprimir_RLE("a$bb&&&&&c"),
                "a$b2&5c",
            ],
            "Argumento usado: cadena=''": [comprimir_RLE(""), ""],
        }
        for prueba, (a, b) in pruebas.items():
            with self.subTest(prueba=prueba):
                self.assertEqual(a, b, prueba)
