from pathlib import Path
import ast


BASE_EXERCISES_PATH = Path("content/python/ESP/src")
ORDERED_CATEGORIES = [
    "numeros",
    "strings",
    "listas",
    "diccionarios",
]

CATEGORY_TITLES = {
    "numeros": "Números",
    "strings": "Strings",
    "listas": "Listas y Tuplas",
    "diccionarios": "Conjuntos y Diccionarios",
}


def get_exercise_groups() -> dict[str, list[str]]:
    exercises: dict[str, list[str]] = {}

    for file_path in BASE_EXERCISES_PATH.glob("*.py"):
        category = file_path.stem

        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

        functions = [
            node.name
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        ]

        exercises[category] = functions

    return exercises


def get_category_functions(category: str) -> list[str] | None:
    file_path = BASE_EXERCISES_PATH / f"{category}.py"
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())

    return [
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]


def get_category_title(category: str) -> str:
    return CATEGORY_TITLES.get(category, category.capitalize())


def get_ordered_category_cards(exercises: dict[str, list[str]]) -> list[dict[str, str | int]]:
    ordered_keys = [key for key in ORDERED_CATEGORIES if key in exercises]
    remaining_keys = sorted(key for key in exercises if key not in ORDERED_CATEGORIES)

    cards: list[dict[str, str | int]] = []
    for category in ordered_keys + remaining_keys:
        cards.append(
            {
                "slug": category,
                "title": get_category_title(category),
                "count": len(exercises[category]),
            }
        )

    return cards
