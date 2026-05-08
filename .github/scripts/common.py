# Copyright 2026 Tim Korelov (https://github.com/lifestreamy)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import sys

from config import DB_FILE_PATH


def fail(msg):
    print(f"::error::{msg}")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"error_msg={msg}\n")
    sys.exit(1)


def get_text(parsed_data, key):
    field = parsed_data.get(key, {})
    if isinstance(field, dict):
        text = field.get('text', '')
        return '' if text.strip(' _*') == 'No response' else text
    if isinstance(field, list):
        return ';'.join(field)
    return '' if field.strip(' _*') == 'No response' else str(field)


def load_db():
    try:
        with open(DB_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_db(data):
    os.makedirs(os.path.dirname(DB_FILE_PATH), exist_ok=True)
    with open(DB_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)


def set_action_output(action_result, success_message):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"action_result={action_result}\n")
        f.write(f"success_msg={success_message}\n")
