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

from common import fail, load_db, save_db, set_action_output
from config import *
from validator import validate_submission

def process_approval():
    parsed_data_str = os.environ.get('PARSED_DATA', '{}')
    issue_id = int(os.environ['ISSUE_NUMBER'])
    raw_body = os.environ.get('RAW_ISSUE_BODY', '')

    new_site, errors = validate_submission(parsed_data_str, issue_id, raw_body)

    if errors:
        joined_errors = "<br>".join(f"• {err.replace('Validation Failed: ', '')}" for err in errors)
        fail(f"Please fix the following issues:<br>{joined_errors}")

    sites = load_db()
    existing_index = next((i for i, site in enumerate(sites) if site.get("issueNumber") == issue_id), -1)

    if existing_index >= 0:
        if sites[existing_index] == new_site:
            action_result = ApprovalResult.UNCHANGED.value
            success_message = MSG_APPROVE_UNCHANGED
        else:
            sites[existing_index] = new_site
            action_result = ApprovalResult.UPDATED.value
            success_message = MSG_APPROVE_UPDATED
    else:
        sites.append(new_site)
        action_result = ApprovalResult.ADDED.value
        success_message = MSG_APPROVE_ADDED

    if action_result != ApprovalResult.UNCHANGED.value:
        save_db(sites)

    set_action_output(action_result, success_message)

def try_process_approval():
    try:
        process_approval()
    except SystemExit:
        raise
    except Exception as e:
        fail(f"An unexpected error occurred during approval: {e}")

if __name__ == "__main__":
    try_process_approval()
