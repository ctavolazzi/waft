# OpenHands Secret Registry for Secure Secret Management

**Date**: 2026-01-14 20:55:00
**Context**: Using OpenHands Secret Registry to securely manage sensitive data
**Status**: 🔐 SECRET MANAGEMENT ENABLED

---

## What Is Secret Registry?

The Secret Registry provides a **secure way to handle sensitive data** in your agent's workspace. It:

- ✅ **Automatically detects** secret references in bash commands
- ✅ **Injects secrets** as environment variables when needed
- ✅ **Masks secret values** in command outputs to prevent accidental exposure
- ✅ **Supports static strings** or **callable functions** for dynamic secrets

**Key Benefits**:
- Secure secret handling
- Automatic masking in outputs
- Integration with external secret stores
- No accidental exposure

---

## How It Works

### Automatic Detection

The Secret Registry automatically:
1. **Detects secret references** in bash commands (e.g., `$SECRET_TOKEN`)
2. **Injects secrets** as environment variables when commands run
3. **Masks secret values** in command outputs to prevent exposure
4. **Tracks secret usage** for security auditing

### Secret Injection

Secrets are injected as environment variables:
```bash
# Agent runs: echo $SECRET_TOKEN
# Secret Registry injects: SECRET_TOKEN=my-secret-value
# Command output: [MASKED] (secret value hidden)
```

---

## Basic Usage

### Static Secrets

Provide secrets as static strings:

```python
conversation.update_secrets({
    "SECRET_TOKEN": "my-secret-token-value",
    "API_KEY": "sk-1234567890",
})
```

**Use in commands**:
```python
conversation.send_message("echo $SECRET_TOKEN")
conversation.run()
# Output: [MASKED] (secret value is hidden)
```

---

### Dynamic Secrets (SecretSource)

Provide secrets as callable functions for dynamic retrieval:

```python
from openhands.sdk.secret import SecretSource

class MySecretSource(SecretSource):
    def get_value(self) -> str:
        # Fetch from external secret store
        return fetch_secret_from_vault("my-secret-key")

conversation.update_secrets({
    "DYNAMIC_SECRET": MySecretSource(),
})
```

**Benefits**:
- Integration with external secret stores
- Dynamic secret retrieval
- Credential rotation support
- Centralized secret management

---

## Integration with Generation Script

**File**: `scripts/generate_tavern_game_with_skills.py`

**New Features**:
- ✅ `--secrets-file` flag to load secrets from JSON file
- ✅ Automatic detection of common environment variables
- ✅ Secret masking in command outputs
- ✅ Secure secret handling

**Usage**:

```bash
# Load secrets from JSON file
python scripts/generate_tavern_game_with_skills.py --secrets-file secrets.json

# Secrets file format (secrets.json):
{
  "GITHUB_TOKEN": "ghp_1234567890",
  "NPM_TOKEN": "npm_1234567890",
  "API_KEY": "sk-1234567890"
}

# Or use environment variables (automatically detected)
export GITHUB_TOKEN="ghp_1234567890"
export NPM_TOKEN="npm_1234567890"
python scripts/generate_tavern_game_with_skills.py
```

**Output**:
```
🔐 Loaded 3 secret(s) from secrets.json
   (Secret values will be masked in command outputs)

🔐 Loaded 2 secret(s) from environment variables
   (Secret values will be masked in command outputs)
```

---

## Use Cases

### 1. GitHub Token for Repository Operations

**Scenario**: Agent needs to push to GitHub

**Solution**:
```python
conversation.update_secrets({
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
})

conversation.send_message("git push https://$GITHUB_TOKEN@github.com/user/repo.git")
conversation.run()
# Token is masked in output
```

---

### 2. NPM Token for Package Publishing

**Scenario**: Agent needs to publish npm packages

**Solution**:
```python
conversation.update_secrets({
    "NPM_TOKEN": os.getenv("NPM_TOKEN"),
})

conversation.send_message("npm publish --access public")
conversation.run()
# Token is automatically injected and masked
```

---

### 3. API Keys for External Services

**Scenario**: Agent needs to call external APIs

**Solution**:
```python
conversation.update_secrets({
    "EXTERNAL_API_KEY": os.getenv("EXTERNAL_API_KEY"),
})

conversation.send_message("curl -H 'Authorization: Bearer $EXTERNAL_API_KEY' https://api.example.com/data")
conversation.run()
# API key is masked in output
```

---

### 4. Dynamic Secrets from Vault

**Scenario**: Secrets stored in external vault (e.g., HashiCorp Vault)

**Solution**:
```python
from openhands.sdk.secret import SecretSource

class VaultSecretSource(SecretSource):
    def get_value(self) -> str:
        # Fetch from HashiCorp Vault
        return vault_client.read_secret("secret/my-app/api-key")["data"]["value"]

conversation.update_secrets({
    "VAULT_API_KEY": VaultSecretSource(),
})
```

---

## Security Features

### Automatic Masking

**Secret values are automatically masked** in command outputs:

```python
conversation.update_secrets({"SECRET_TOKEN": "my-secret-value"})
conversation.send_message("echo $SECRET_TOKEN")
conversation.run()

# Output: [MASKED] (not "my-secret-value")
```

**Prevents accidental exposure** in logs, traces, or outputs.

---

### Secret Detection

**Secret Registry detects secret references** in bash commands:

```python
# These are detected:
echo $SECRET_TOKEN
export API_KEY=$SECRET_TOKEN
curl -H "Authorization: Bearer $SECRET_TOKEN" https://api.example.com
```

**Secrets are injected** as environment variables automatically.

---

### Secure Storage

**Secrets are stored securely** in conversation state:
- Not logged in plain text
- Masked in outputs
- Encrypted in persistence (if supported)

---

## Best Practices

### 1. Use Environment Variables

**Prefer environment variables** for secrets:

```bash
# Set in environment
export GITHUB_TOKEN="ghp_1234567890"
export NPM_TOKEN="npm_1234567890"

# Script automatically detects common variables
python scripts/generate_tavern_game_with_skills.py
```

**Benefits**:
- No secrets in code
- Easy to rotate
- Secure by default

---

### 2. Use Secret Files (JSON)

**For multiple secrets**, use JSON file:

```json
{
  "GITHUB_TOKEN": "ghp_1234567890",
  "NPM_TOKEN": "npm_1234567890",
  "API_KEY": "sk-1234567890"
}
```

**Load in script**:
```bash
python scripts/generate_tavern_game_with_skills.py --secrets-file secrets.json
```

**Security**: Add `secrets.json` to `.gitignore`!

---

### 3. Use SecretSource for Dynamic Secrets

**For external secret stores**, use SecretSource:

```python
class MySecretSource(SecretSource):
    def get_value(self) -> str:
        # Fetch from external store
        return fetch_secret("my-secret-key")

conversation.update_secrets({
    "DYNAMIC_SECRET": MySecretSource(),
})
```

**Benefits**:
- Integration with vaults
- Credential rotation
- Centralized management

---

### 4. Rotate Secrets Regularly

**Rotate secrets regularly**:
- Update environment variables
- Update secret files
- Update SecretSource implementations

**Security**: Regular rotation reduces exposure risk.

---

## Integration with Other Features

### Secrets + Persistence

**Secrets are persisted**:
- Stored in conversation state
- Restored when resuming conversations
- Masked in persisted state

**Note**: Ensure persistence directory is secure!

---

### Secrets + Observability

**Secrets are masked in traces**:
- Secret values not exposed in traces
- Secret names visible (for debugging)
- Secure observability

**Example**:
```
Trace: echo $SECRET_TOKEN
Output: [MASKED]
```

---

### Secrets + Metrics

**Secrets don't affect metrics**:
- No secret data in metrics
- Cost tracking unaffected
- Performance tracking unaffected

---

### Secrets + Delegation

**Secrets available to sub-agents**:
- Sub-agents inherit secrets
- Secrets masked in sub-agent outputs
- Secure delegation

---

## Troubleshooting

### Secrets Not Injected

**Problem**: Secrets not available in commands

**Solutions**:
1. Verify secrets are registered:
   ```python
   conversation.update_secrets({"MY_SECRET": "value"})
   ```

2. Check secret name matches:
   ```bash
   # Correct
   echo $MY_SECRET
   
   # Incorrect (wrong name)
   echo $MY_SECRET_TOKEN
   ```

3. Verify command uses bash syntax:
   ```bash
   # Correct
   echo $SECRET_TOKEN
   
   # Incorrect (not bash)
   echo SECRET_TOKEN
   ```

---

### Secrets Exposed in Output

**Problem**: Secret values visible in output

**Solutions**:
1. Verify Secret Registry is enabled (automatic)
2. Check secret is registered before use
3. Ensure command uses `$SECRET_NAME` syntax

---

### Secret File Not Found

**Problem**: `--secrets-file` not found

**Solutions**:
1. Verify file path is correct
2. Check file permissions
3. Ensure JSON format is valid

---

## Advanced Usage

### Custom SecretSource

**Create custom SecretSource** for external stores:

```python
from openhands.sdk.secret import SecretSource

class AWSSecretsManagerSource(SecretSource):
    def __init__(self, secret_name: str):
        self.secret_name = secret_name
    
    def get_value(self) -> str:
        import boto3
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=self.secret_name)
        return response['SecretString']

# Use in conversation
conversation.update_secrets({
    "AWS_SECRET": AWSSecretsManagerSource("my-app/api-key"),
})
```

---

### Multiple Secret Sources

**Combine multiple sources**:

```python
# Static secrets
static_secrets = {
    "STATIC_SECRET": "value",
}

# Dynamic secrets
dynamic_secrets = {
    "DYNAMIC_SECRET": MySecretSource(),
}

# Combine
conversation.update_secrets({**static_secrets, **dynamic_secrets})
```

---

## Security Considerations

### 1. Never Commit Secrets

**Never commit secrets to git**:
- Add `secrets.json` to `.gitignore`
- Use environment variables
- Use secret management services

---

### 2. Rotate Secrets Regularly

**Rotate secrets regularly**:
- Update environment variables
- Update secret files
- Update SecretSource implementations

---

### 3. Use Least Privilege

**Use least privilege**:
- Only provide secrets needed
- Use scoped tokens when possible
- Limit secret access

---

### 4. Monitor Secret Usage

**Monitor secret usage**:
- Track which secrets are used
- Audit secret access
- Alert on unusual usage

---

## Example: Complete Setup

```python
import os
from openhands.sdk.secret import SecretSource

# Static secrets from environment
env_secrets = {
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
    "NPM_TOKEN": os.getenv("NPM_TOKEN"),
}

# Dynamic secrets from vault
class VaultSecretSource(SecretSource):
    def get_value(self) -> str:
        return vault_client.read_secret("secret/api-key")["data"]["value"]

dynamic_secrets = {
    "VAULT_API_KEY": VaultSecretSource(),
}

# Combine and register
conversation.update_secrets({**env_secrets, **dynamic_secrets})

# Use in commands
conversation.send_message("git push https://$GITHUB_TOKEN@github.com/user/repo.git")
conversation.run()
# Token is masked in output
```

---

## Conclusion

**Secret Registry Benefits**:
- ✅ Secure secret handling
- ✅ Automatic masking
- ✅ Integration with external stores
- ✅ No accidental exposure

**Essential for**:
- Production deployments
- External API integration
- Repository operations
- Secure credential management

**This is essential for secure agent operations!**

---

**Secret Registry Guide Complete**: 2026-01-14 20:55:00