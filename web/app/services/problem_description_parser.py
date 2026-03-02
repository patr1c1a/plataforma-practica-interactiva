import re


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def _split_type_parts(type_text: str) -> list[str]:
    return [part.strip() for part in type_text.split(";") if part.strip()]


class ProblemDescriptionParser:
    def __init__(self) -> None:
        self._marker_map = {
            "examples": re.compile(r"^-?Ejemplo(?:s)?:\s*$", re.IGNORECASE),
            "parameters": re.compile(r"^-Par(?:a|\u00e1)metro[s]?:\s*$", re.IGNORECASE),
            "return_value": re.compile(r"^-?Valor retornado:\s*$", re.IGNORECASE),
        }
        self._suggestion_pattern = re.compile(
            r"^-?Sugerencia did(?:a|\u00e1)ctica:\s*(.*)$",
            re.IGNORECASE,
        )
        self._parameter_patterns = [
            re.compile(r"^-([A-Za-z_]\w*)\s*\(([^)]*)\)\s*:\s*(.*)$"),
            re.compile(r"^-\(([^)]*)\)\s*([A-Za-z_]\w*)\s*:\s*(.*)$"),
        ]

    def parse(self, docstring: str | None) -> dict:
        if not docstring:
            return {
                "description": [],
                "suggestions": [],
                "examples": [],
                "parameters": [],
                "return_value": None,
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
            for section_name, pattern in self._marker_map.items():
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

            suggestion_match = self._suggestion_pattern.match(stripped)
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
        current_parameter = None

        for line in section_lines["parameters"]:
            stripped = line.strip()
            if not stripped:
                continue

            match = None
            match_variant = 0
            for index, pattern in enumerate(self._parameter_patterns):
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
