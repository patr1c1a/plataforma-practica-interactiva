from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import re
from web.app.services.execution import run_tests
from web.app.services.exercise_catalog import (
    CATEGORY_TITLES,
    get_exercise_groups,
    get_category_functions,
    get_ordered_category_cards,
)
import ast

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def _split_type_parts(type_text: str) -> list[str]:
    return [part.strip() for part in type_text.split(";") if part.strip()]


def parse_problem_description(docstring: str | None) -> dict:
    if not docstring:
        return {
            "description": [],
            "suggestions": [],
            "examples": [],
            "parameters": [],
            "return_value": None,
        }

    marker_map = {
        "examples": re.compile(r"^-?Ejemplo(?:s)?:\s*$", re.IGNORECASE),
        "parameters": re.compile(r"^-Par(?:a|\u00e1)metro[s]?:\s*$", re.IGNORECASE),
        "return_value": re.compile(r"^-?Valor retornado:\s*$", re.IGNORECASE),
    }

    section_lines = {
        "description": [],
        "examples": [],
        "parameters": [],
        "return_value": [],
    }

    current_section = "description"
    for raw_line in docstring.splitlines():
        line = raw_line.rstrip()

        matched_section = None
        for section_name, pattern in marker_map.items():
            if pattern.match(line.strip()):
                matched_section = section_name
                break

        if matched_section:
            current_section = matched_section
            continue

        section_lines[current_section].append(line)

    description_paragraphs = []
    suggestions = []
    current_description = []
    current_suggestion = []
    suggestion_pattern = re.compile(r"^-?Sugerencia didáctica:\s*(.*)$", re.IGNORECASE)

    def flush_description() -> None:
        nonlocal current_description
        if current_description:
            description_paragraphs.append(
                _normalize_whitespace(" ".join(current_description))
            )
            current_description = []

    def flush_suggestion() -> None:
        nonlocal current_suggestion
        if current_suggestion:
            suggestions.append(_normalize_whitespace(" ".join(current_suggestion)))
            current_suggestion = []

    for line in section_lines["description"]:
        stripped = line.strip()
        if not stripped:
            flush_description()
            flush_suggestion()
            continue

        suggestion_match = suggestion_pattern.match(stripped)
        if suggestion_match:
            flush_description()
            flush_suggestion()

            suggestion_text = suggestion_match.group(1).strip()
            if suggestion_text:
                current_suggestion = [suggestion_text]
            else:
                current_suggestion = []
            continue

        if current_suggestion:
            current_suggestion.append(stripped)
            continue

        current_description.append(stripped)

    flush_description()
    flush_suggestion()

    examples = []
    for line in section_lines["examples"]:
        stripped = line.strip()
        if not stripped:
            continue

        if "->" in stripped:
            input_part, output_part = stripped.split("->", 1)
            examples.append(
                {
                    "input": _normalize_whitespace(input_part.strip()),
                    "output": _normalize_whitespace(output_part.strip()),
                }
            )
            continue

        if examples:
            examples[-1]["output"] = _normalize_whitespace(
                f"{examples[-1]['output']} {stripped}"
            )
        else:
            examples.append({"input": _normalize_whitespace(stripped), "output": ""})

    parameters = []
    parameter_patterns = [
        re.compile(r"^-([A-Za-z_]\w*)\s*\(([^)]*)\)\s*:\s*(.*)$"),
        re.compile(r"^-\(([^)]*)\)\s*([A-Za-z_]\w*)\s*:\s*(.*)$"),
    ]
    current_parameter = None

    for line in section_lines["parameters"]:
        stripped = line.strip()
        if not stripped:
            continue

        match = None
        match_variant = 0
        for index, pattern in enumerate(parameter_patterns):
            candidate = pattern.match(stripped)
            if candidate:
                match = candidate
                match_variant = index
                break

        if match:
            if current_parameter:
                current_parameter["description"] = _normalize_whitespace(
                    current_parameter["description"]
                )
                parameters.append(current_parameter)

            if match_variant == 0:
                parameter_name = match.group(1)
                parameter_type = _normalize_whitespace(match.group(2))
                parameter_description = match.group(3).strip()
            else:
                parameter_name = match.group(2)
                parameter_type = _normalize_whitespace(match.group(1))
                parameter_description = match.group(3).strip()

            current_parameter = {
                "name": parameter_name,
                "type": parameter_type,
                "type_parts": _split_type_parts(parameter_type),
                "description": parameter_description,
            }
        elif current_parameter:
            current_parameter["description"] = (
                f"{current_parameter['description']} {stripped}"
            )

    if current_parameter:
        current_parameter["description"] = _normalize_whitespace(
            current_parameter["description"]
        )
        parameters.append(current_parameter)

    return_value = None
    return_text = _normalize_whitespace(
        " ".join(line.strip() for line in section_lines["return_value"] if line.strip())
    )

    if return_text:
        return_type_match = re.match(r"^\(([^)]*)\)\s*(.*)$", return_text)
        if return_type_match:
            return_type = _normalize_whitespace(return_type_match.group(1))
            return_value = {
                "type": return_type,
                "type_parts": _split_type_parts(return_type),
                "description": _normalize_whitespace(return_type_match.group(2)),
            }
        else:
            return_value = {
                "type": "",
                "type_parts": [],
                "description": return_text,
            }

    return {
        "description": description_paragraphs,
        "suggestions": suggestions,
        "examples": examples,
        "parameters": parameters,
        "return_value": return_value,
    }


def render_with_optional_fragment(
    request: Request,
    full_template: str,
    fragment_template: str,
    context: dict,
):
    """
    If it's an HTMX request, return only the fragment.
    If it's a normal request, return the whole page.
    """
    request_from_htmx = request.headers.get("hx-request") == "true"

    if request_from_htmx:
        return templates.TemplateResponse(fragment_template, context)

    return templates.TemplateResponse(full_template, context)


@router.get("/exercises")
def list_exercises(request: Request):
    exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(exercises)

    template_context = {
        "request": request,
        "exercise_groups": exercises,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "problem_description": None,
        "view": "exercise_list",
        "current_category": None,
    }

    return render_with_optional_fragment(
        request=request,
        full_template="index.html",
        fragment_template="fragments/exercise_list.html",
        context=template_context,
    )


@router.get("/exercises/{category}")
def list_category_exercises(request: Request, category: str):
    functions = get_category_functions(category)
    if functions is None:
        return HTMLResponse(status_code=404, content="Categoria no encontrada")

    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)
    selected_category_exercises = {category: functions}

    template_context = {
        "request": request,
        "exercise_groups": selected_category_exercises,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "problem_description": None,
        "view": "exercise_list",
        "current_category": category,
    }

    return render_with_optional_fragment(
        request=request,
        full_template="index.html",
        fragment_template="fragments/exercise_list.html",
        context=template_context,
    )


@router.get("/exercises/{category}/{function_name}")
def exercise_detail(request: Request, category: str, function_name: str):
    all_exercises = get_exercise_groups()
    category_cards = get_ordered_category_cards(all_exercises)
    base_path = Path("content/python/ESP/src")
    file_path = base_path / f"{category}.py"

    if not file_path.exists():
        return HTMLResponse(status_code=404, content="Categoria no encontrada")

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    function_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_node = node
            break

    if function_node is None:
        return HTMLResponse(status_code=404, content="Funcion no encontrada")

    # Get docstring (problem description)
    problem_description = ast.get_docstring(function_node)
    problem_sections = parse_problem_description(problem_description)

    # Get function signature
    args = [arg.arg for arg in function_node.args.args]
    function_signature = f"def {function_name}({', '.join(args)}):\n    "

    ordered_exercises = [
        (category_name, function)
        for category_name, function_names in all_exercises.items()
        for function in function_names
    ]
    current_index = ordered_exercises.index((category, function_name))
    previous_exercise = (
        ordered_exercises[current_index - 1] if current_index > 0 else None
    )
    next_exercise = (
        ordered_exercises[current_index + 1]
        if current_index < len(ordered_exercises) - 1
        else None
    )

    template_context = {
        "request": request,
        "category_name": category,
        "function_name": function_name,
        "problem_description": problem_description,
        "problem_sections": problem_sections,
        "function_signature": function_signature,
        "exercise_groups": all_exercises,
        "current_category": category,
        "current_exercise": function_name,
        "category_cards": category_cards,
        "category_titles": CATEGORY_TITLES,
        "view": "exercise_detail",
        "previous_exercise": previous_exercise,
        "next_exercise": next_exercise,
    }

    return render_with_optional_fragment(
        request=request,
        full_template="index.html",
        fragment_template="fragments/exercise_detail.html",
        context=template_context,
    )


@router.post("/exercises/{category}/{function_name}/run")
def run_exercise(
    request: Request, category: str, function_name: str, code: str = Form(...)
):
    result = run_tests(
        category=category,
        function_name=function_name,
        user_code=code,
    )

    return templates.TemplateResponse(
        "fragments/execution_result.html",
        {
            "request": request,
            "result": result,
        },
    )
