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

# File Paths
DB_FILE_PATH = "resources/db/data.json"

# Image CDN Validation
ALLOWED_IMAGE_CDN_PREFIX = "https://github.com/user-attachments/assets/"

# Error Messages
ERR_PARSE = "Failed to parse JSON data from GitHub Action: {}"
ERR_NAME_EMPTY = "Validation Failed: Entry name cannot be empty"
ERR_URL_INVALID = "Validation Failed: Invalid or missing Entry URL"
ERR_IMG_INVALID = "Validation Failed: Invalid or missing Image URL"
ERR_IMG_CDN = f"The provided Image URL does not correspond to the GitHub CDN — \"{ALLOWED_IMAGE_CDN_PREFIX}\""

# Success Messages (Approval)
MSG_APPROVE_UNCHANGED = "✅ Nothing has changed since the last submission, keeping the last version."
MSG_APPROVE_UPDATED = "✅ The entry has been successfully updated in the database."
MSG_APPROVE_ADDED = "✅ The entry has been approved and added to the database."

# Success Messages (Revocation)
MSG_REVOKE_SUCCESS = "✅ The entry has been successfully revoked and removed from the database."
MSG_REVOKE_NOT_FOUND = "✅ There is no submission to revoke for this issue."
