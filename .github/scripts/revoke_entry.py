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
from config import MSG_REVOKE_SUCCESS, MSG_REVOKE_NOT_FOUND, RevocationResult


def process_revocation():
    issue_id = int(os.environ['ISSUE_NUMBER'])
    entries = load_db()
    original_length = len(entries)

    updated_entries = [entry for entry in entries if entry.get('issueNumber') != issue_id]

    if len(updated_entries) < original_length:
        save_db(updated_entries)
        action_result = RevocationResult.REVOKED.value
        success_message = MSG_REVOKE_SUCCESS
    else:
        action_result = RevocationResult.NOT_FOUND.value
        success_message = MSG_REVOKE_NOT_FOUND

    set_action_output(action_result, success_message)


def try_process_revocation():
    try:
        process_revocation()
    except SystemExit:
        raise
    except Exception as e:
        fail(f"An unexpected error occurred during revocation: {e}")


if __name__ == "__main__":
    try_process_revocation()
