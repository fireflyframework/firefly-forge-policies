# Contribute a policy

Explain the behavior the policy should change and which projects need it. Keep instructions specific enough for a coding worker to act on. A recommendation must describe its intended practice; a quality gate must provide an executable check with a bounded timeout.

Keep IDs stable, validate `catalog.json`, and run the configured tests before opening a pull request. Include the expected result and any required project tools. Avoid claims that a prompt guarantees compliance or that a green command establishes every production capability.

Review changes to executable commands for permissions, credential exposure and failure behavior. Keep secrets, local machine paths, dependency directories and private planning material out of the repository.
