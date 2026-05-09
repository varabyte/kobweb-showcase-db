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

from enum import Enum

# File Paths
DB_FILE_PATH = "resources/db/showcased-sites.json"

# Image CDN Validation (List of allowed prefixes)
ALLOWED_IMAGE_CDN_PREFIXES = [
    "https://github.com/user-attachments/assets/"
]

# Error Messages
ERR_PARSE = "Failed to parse JSON data from GitHub Action: {}"
ERR_NAME_EMPTY = "Validation Failed: Site name cannot be empty"
ERR_SITE_TYPE_MISSING = "Validation Failed: Please select a Site Type from the list"
ERR_URL_INVALID = "Validation Failed: Invalid or missing Site URL"
ERR_IMG_INVALID = "Validation Failed: Invalid or missing Image URL"
ERR_IMG_CDN = f"The provided Image URL does not correspond to any of the allowed CDN providers — {', '.join(ALLOWED_IMAGE_CDN_PREFIXES)}"

# Success Messages (Approval)
MSG_APPROVE_UNCHANGED = "✅ Nothing has changed since the last submission, keeping the last version."
MSG_APPROVE_UPDATED = "✅ The site has been successfully updated in the showcase."
MSG_APPROVE_ADDED = "✅ The site has been approved and added to the showcase."

# Success Messages (Revocation)
MSG_REVOKE_SUCCESS = "✅ The site has been successfully revoked and removed from the showcase."
MSG_REVOKE_NOT_FOUND = "✅ There is no submission to revoke for this issue."

# Site Type Mapping (Verbose in GitHub Forms -> short in DB)
SITE_TYPE_MAPPING = {
    "Static Site (SSG)": "SSG",
    "Fullstack (Kobweb-native)": "Kobweb",
    "Fullstack (other backend)": "Other"
}

# Enums for GitHub Action Outputs
class ApprovalResult(str, Enum):
    UNCHANGED = "unchanged"
    UPDATED = "updated"
    ADDED = "added"

class RevocationResult(str, Enum):
    REVOKED = "revoked"
    NOT_FOUND = "not_found"
