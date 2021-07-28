import json
import os
import pickle
from datetime import datetime
from typing import Any, Dict, List

import requests

from module.constants import HTTP_OK, UTF_8
from module.exception.RequestException import RequestException


def has_access_to_internet() -> bool:
    url: str = "https://www.google.com/"
    response = requests.get(url)

    if response.status_code == HTTP_OK:
        return True
    return False


def check_http_code_get_json(response: requests.models.Response) -> Dict:
    if response.status_code != HTTP_OK:
        print(response.json())
        raise RequestException(response.status_code)

    return response.json()


def remove_duplicates(items: List[Any]) -> List[Any]:
    return list(set(items))


def remove_none_items(items: List[Any]) -> List[Any]:
    return [item for item in items if item is not None]


def remove_new_line_items(items: List[str]) -> List[str]:
    return [item for item in items if item != "\n"]


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def replace_many(text: str, replaced_texts: List[str], replacing_text: str = "") -> str:
    for replaced_text in replaced_texts:
        text = text.replace(replaced_text, replacing_text)
    return text


def convert_bool_to_json(value: bool) -> str:
    return str(value).lower()


def convert_bool_to_string(value: bool) -> str:
    if value:
        return "Yes"
    return "No"


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


def get_filename(name: str, extension: str) -> str:
    return (name + "-" + datetime.now().strftime("%H%M%S") + extension).replace(" ", "")


def read_from_text_file(path: str) -> str:
    with open(path, "r", encoding=UTF_8) as file:
        return file.read()


def save_to_file(path: str, data: Any, mode: str = "w") -> None:
    with open(path, mode, encoding=UTF_8) as file:
        file.write(data)


def save_object_to_file(path: str, data: object) -> None:
    with open(path, "wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)


def read_object_from_file(path: str) -> Any:
    with open(path, "rb") as file:
        return pickle.load(file)
