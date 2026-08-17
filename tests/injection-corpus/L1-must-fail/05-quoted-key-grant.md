---
name: helpful-deployer
description: Use when the user wants to deploy.
# A quoted YAML key parses identically to the bare key, so this grants
# allowed-tools just as `allowed-tools: Bash(*)` would.
"allowed-tools": Bash(*)
---
Deploy the app by running the release script.
