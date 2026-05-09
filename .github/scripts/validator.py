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
from typing import Dict, Any, Tuple, Optional

from common import get_text
from config import *


def validate_submission(parsed_data_str: str, issue_id: int, raw_body: str) -> Tuple[Optional[Dict[str, Any]], list[str]]:
    try:
        parsed_data = json.loads(parsed_data_str)
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)
    except Exception as e:
        return None, [ERR_PARSE.format(e)]

    raw_site_url = get_text(parsed_data, 'live-url').strip(' <>')
    if '](' in raw_site_url:
        raw_site_url = raw_site_url.split('](', 1)[1].split(')', 1)[0].strip()
    clean_site_url = raw_site_url if raw_site_url.startswith(('http://', 'https://')) else f"https://{raw_site_url}"

    clean_image_url = ""
    if 'src="' in raw_body:
        src_value = raw_body.split('src="', 1)[1].split('"', 1)[0].strip()
        if '](' in src_value:
            clean_image_url = src_value.split('](', 1)[1].split(')', 1)[0].strip()
        else:
            clean_image_url = src_value

    site_type = get_text(parsed_data, 'site-type')
    features = get_text(parsed_data, 'core-features')
    custom_features = get_text(parsed_data, 'other-keywords')
    site_name = get_text(parsed_data, 'project-name').strip()

    errors = []

    if not site_type:
        errors.append(ERR_SITE_TYPE_MISSING)
    if not site_name:
        errors.append(ERR_NAME_EMPTY)
    if not clean_site_url or clean_site_url == "https://":
        errors.append(ERR_URL_INVALID)
    if not clean_image_url:
        errors.append(ERR_IMG_INVALID)
    elif not any(clean_image_url.startswith(prefix) for prefix in ALLOWED_IMAGE_CDN_PREFIXES):
        errors.append(ERR_IMG_CDN)

    if errors:
        return None, errors

    short_site_type = SITE_TYPE_MAPPING.get(site_type, site_type)

    raw_features = f"{features};{custom_features}"
    clean_tags = [tag.strip() for tag in raw_features.split(';') if tag.strip() != 'None' and tag.strip()]

    new_site = {
        "issueNumber": issue_id,
        "name": site_name,
        "url": clean_site_url,
        "imageUrl": clean_image_url,
        "description": get_text(parsed_data, 'project-description').strip(),
        "siteType": short_site_type,
        "tags": clean_tags
    }

    return new_site, []
