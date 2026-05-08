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

from common import fail, get_text, load_db, save_db, set_action_output
from config import *


def process_approval():
    parsed_data_str = os.environ.get('PARSED_DATA', '{}')

    try:
        parsed_data = json.loads(parsed_data_str)
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)
    except Exception as e:
        fail(ERR_PARSE.format(e))

    issue_id = int(os.environ['ISSUE_NUMBER'])

    raw_site_url = get_text(parsed_data, 'entry-url').strip(' <>')
    if '](' in raw_site_url:
        raw_site_url = raw_site_url.split('](', 1)[1].split(')', 1)[0].strip()
    clean_site_url = raw_site_url if raw_site_url.startswith(('http://', 'https://')) else f"https://{raw_site_url}"

    raw_body = os.environ.get('RAW_ISSUE_BODY', '')
    clean_image_url = ""

    if 'src="' in raw_body:
        src_value = raw_body.split('src="', 1)[1].split('"', 1)[0].strip()
        if '](' in src_value:
            clean_image_url = src_value.split('](', 1)[1].split(')', 1)[0].strip()
        else:
            clean_image_url = src_value

    raw_features = get_text(parsed_data, 'entry-tags')
    clean_tags = [tag.strip() for tag in raw_features.split(';') if tag.strip() != 'None' and tag.strip()]

    entry_name = get_text(parsed_data, 'entry-title').strip()

    if not entry_name:
        fail(ERR_NAME_EMPTY)
    if not clean_site_url or clean_site_url == "https://":
        fail(ERR_URL_INVALID)
    if not clean_image_url:
        fail(ERR_IMG_INVALID)
    if not clean_image_url.startswith(ALLOWED_IMAGE_CDN_PREFIX):
        fail(ERR_IMG_CDN)

    new_entry = {
        "issueNumber": issue_id,
        "name": entry_name,
        "url": clean_site_url,
        "imageUrl": clean_image_url,
        "description": get_text(parsed_data, 'entry-description').strip(),
        "tags": clean_tags
    }

    entries = load_db()
    existing_index = next((i for i, entry in enumerate(entries) if entry.get("issueNumber") == issue_id), -1)

    if existing_index >= 0:
        if entries[existing_index] == new_entry:
            action_result = "unchanged"
            success_message = MSG_APPROVE_UNCHANGED
        else:
            entries[existing_index] = new_entry
            action_result = "updated"
            success_message = MSG_APPROVE_UPDATED
    else:
        entries.append(new_entry)
        action_result = "added"
        success_message = MSG_APPROVE_ADDED

    if action_result != "unchanged":
        save_db(entries)

    set_action_output(action_result, success_message)


if __name__ == "__main__":
    process_approval()
