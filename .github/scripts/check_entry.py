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

import os
import json

from common import fail, set_action_output
from validator import validate_submission


def format_parsed_data(new_site: dict) -> str:
    """Formats the parsed data dictionary into a collapsible HTML block for GitHub comments."""
    json_str = json.dumps(new_site, indent=2)

    # Escape HTML to prevent possible injection breaking the <details> tag itself
    json_str = json_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Convert to HTML-safe single-line string for GITHUB_OUTPUT compatibility
    html_str = json_str.replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')

    return f"<details><summary><b>🔍 View Parsed Data</b></summary><br><code>{html_str}</code></details>"


def process_check():
    parsed_data_str = os.environ.get('PARSED_DATA', '{}')
    issue_id = int(os.environ['ISSUE_NUMBER'])
    raw_body = os.environ.get('RAW_ISSUE_BODY', '')

    new_site, errors = validate_submission(parsed_data_str, issue_id, raw_body)

    if errors:
        joined_errors = "<br>".join(f"• {err.replace('Validation Failed: ', '')}" for err in errors)
        fail(f"Please fix the following issues:<br>{joined_errors}")

    details_block = format_parsed_data(new_site)
    success_msg = f"✅ Validation Passed! The form is correctly filled and ready to be approved.<br><br>{details_block}"

    set_action_output("success", success_msg)


def try_process_check():
    try:
        process_check()
    except SystemExit:
        raise
    except Exception as e:
        fail(f"An unexpected error occurred during check: {e}")


if __name__ == "__main__":
    try_process_check()