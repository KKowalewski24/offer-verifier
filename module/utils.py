import json
import os
import pickle
import subprocess
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List

import requests

from module.constants import HTTP_OK, UTF_8
from module.exception.RequestException import RequestException


def run_main(main: Callable[[], None]) -> None:
    if check_if_exists_in_args("--type"):
        check_types_check_style()
    elif check_if_exists_in_args("--build"):
        compile_to_pyc()
    else:
        main()


def check_types_check_style() -> None:
    subprocess.call(["mypy", "."])
    subprocess.call(["flake8", "."])


def compile_to_pyc() -> None:
    subprocess.call(["python", "-m", "compileall", "."])


def check_if_exists_in_args(arg: str) -> bool:
    return arg in sys.argv


def has_access_to_internet() -> bool:
    url: str = "https://www.google.com/"
    response = requests.get(url)
    return True if response.status_code == HTTP_OK else False


def check_http_code_get_json(response: requests.models.Response) -> Dict:
    if response.status_code != HTTP_OK:
        print(response.json())
        raise RequestException(response.status_code)

    return response.json()


def display_and_log_info(logger_instance: Any, text: str) -> None:
    print(text)
    logger_instance.info(text)


def display_and_log_warning(logger_instance: Any, text: str) -> None:
    print(text)
    logger_instance.warning(text)


def display_and_log_error(logger_instance: Any, text: str) -> None:
    print(text)
    logger_instance.error(text)


def list_to_string(items: List) -> str:
    return " ".join(items)


def flat_map_list(items: List, callback: Callable[[int, List], List] = lambda x, y: y) -> List:
    return [sub_item for index, sub_items in enumerate(items) for sub_item in callback(index, sub_items)]


def add_value_to_all_items(items: List[str], value: str) -> List[str]:
    return [item + value for item in items]


def remove_duplicates(items: List[Any]) -> List[Any]:
    return list(set(items))


def remove_none_items(items: List[Any]) -> List[Any]:
    return [item for item in items if item is not None]


def remove_new_line_items(items: List[str]) -> List[str]:
    return [item for item in items if item != "\n"]


def is_valid_item(item: Any) -> bool:
    return item is not None and len(item) != 0


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def replace_many(text: str, replaced_texts: List[str], replacing_text: str = "") -> str:
    for replaced_text in replaced_texts:
        text = text.replace(replaced_text, replacing_text)
    return text


def convert_bool_to_json(value: bool) -> str:
    return str(value).lower()


def convert_bool_to_string(value: bool) -> str:
    return "Yes" if value else "No"


def remove_dict_entry_by_key(dictionary: Dict, key_to_delete: str) -> Dict:
    return {
        key: value
        for key, value in dictionary.items()
        if key != key_to_delete
    }


def remove_dict_entry_by_key_if_contains_key(dictionary: Dict, condition_key: str,
                                             key_to_delete: str) -> Dict:
    if condition_key in dictionary.keys():
        return remove_dict_entry_by_key(dictionary, key_to_delete)
    return dictionary


def format_json(data: Dict) -> str:
    return json.dumps(data, indent=4)


def to_string_class_formatter(variables: List, variables_names: List,
                              separator: str = "\t") -> str:
    if len(variables) != len(variables):
        raise Exception("Both arrays must have equal size")

    result: str = ""
    for i in range(len(variables)):
        result += variables_names[i] + ": " + str(variables[i]) + separator

    return result


def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename(name: str, extension: str = "") -> str:
    return (name + "-" + datetime.now().strftime("%H%M%S__%f") + extension).replace(" ", "")


def read_from_text_file(path: str) -> str:
    with open(path, "r", encoding=UTF_8) as file:
        return file.read()


def save_to_file(path: str, data: Any, mode: str = "w") -> None:
    with open(path, mode, encoding=UTF_8) as file:
        file.write(data)


def save_json_to_file(path: str, data: Dict) -> None:
    with open(path, "w", encoding=UTF_8) as file:
        file.write(json.dumps(data, default=lambda o: o.__dict__, indent=4))


def read_json_from_file(path: str) -> Dict:
    with open(path, encoding=UTF_8) as file:
        return json.load(file)


def replace_unsupported_characters(text: str, begin: int = 0, end: int = 256) -> str:
    text_as_list = list(text)
    for index, char in enumerate(text_as_list):
        if not begin <= ord(char) < end:
            text_as_list[index] = " "

    return "".join(text_as_list)


def break_string(text: str, max_line_length: int) -> List[str]:
    result: List[str] = []
    for line_number in range(1, _calculate_lines_number(text, max_line_length) + 1):
        predicted_last_index = max_line_length * line_number
        last_index: int = predicted_last_index if predicted_last_index <= len(text) else len(text)

        if line_number == 1:
            result.append(_set_text_result(text, 0, last_index))
        else:
            result.append(_set_text_result(text, (max_line_length * (line_number - 1)), last_index))

    return result


def _calculate_lines_number(text: str, max_line_length: int) -> int:
    new_lines_number = int(len(text) / max_line_length)
    if len(text) % max_line_length != 0:
        new_lines_number = new_lines_number + 1

    return new_lines_number


def _set_text_result(text: str, begin_index: int, end_index: int) -> str:
    end_line: str = ("\n" if text[end_index - 1] == " " else "-\n")
    return text[begin_index:end_index] + (end_line if len(text) > end_index else "")
