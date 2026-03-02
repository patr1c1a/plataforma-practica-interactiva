import ast
from pathlib import Path
from threading import Lock

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

_catalog_cache_lock = Lock()
_catalog_cache_signature: tuple[tuple[str, int, int], ...] | None = None
_catalog_cache_data: dict[str, list[str]] | None = None


def _build_catalog_signature() -> tuple[tuple[str, int, int], ...]:
    signature_items: list[tuple[str, int, int]] = []

    for file_path in BASE_EXERCISES_PATH.glob("*.py"):
        stats = file_path.stat()
        signature_items.append((file_path.name, stats.st_mtime_ns, stats.st_size))

    signature_items.sort(key=lambda item: item[0])
    return tuple(signature_items)


def _build_exercise_groups() -> dict[str, list[str]]:
    exercises: dict[str, list[str]] = {}

    for file_path in BASE_EXERCISES_PATH.glob("*.py"):
        category = file_path.stem
        source_code = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        functions = [
            node.name for node in tree.body if isinstance(node, ast.FunctionDef)
        ]
        exercises[category] = functions

    return _order_exercises_by_category(exercises)


def _order_exercises_by_category(
    exercises: dict[str, list[str]],
) -> dict[str, list[str]]:
    ordered_exercises: dict[str, list[str]] = {}

    ordered_keys = [key for key in ORDERED_CATEGORIES if key in exercises]
    remaining_keys = sorted(key for key in exercises if key not in ORDERED_CATEGORIES)

    for key in ordered_keys + remaining_keys:
        ordered_exercises[key] = exercises[key]

    return ordered_exercises


def get_exercise_groups() -> dict[str, list[str]]:
    global _catalog_cache_signature, _catalog_cache_data

    signature = _build_catalog_signature()

    with _catalog_cache_lock:
        if _catalog_cache_data is None or _catalog_cache_signature != signature:
            _catalog_cache_data = _build_exercise_groups()
            _catalog_cache_signature = signature

        return {category: functions[:] for category, functions in _catalog_cache_data.items()}


def get_category_functions(category: str) -> list[str] | None:
    exercises = get_exercise_groups()
    functions = exercises.get(category)

    if functions is None:
        return None

    return functions[:]


def get_category_title(category: str) -> str:
    return CATEGORY_TITLES.get(category, category.capitalize())


def get_ordered_category_cards(
    exercises: dict[str, list[str]],
) -> list[dict[str, str | int]]:
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
