# Security Remediation Checklist

## Exposed Secrets
1. **API Key**
   - Description: This API key is used for accessing the internal services. 
   - Impact: If compromised, it could lead to unauthorized access.
   
2. **Database Password**
   - Description: Password for the main database.
   - Impact: Could allow attackers to manipulate data.
   
3. **Third-Party Service Token**
   - Description: Token used to authenticate with third-party services.
   - Impact: Could expose sensitive user data.
   
4. **SSH Key**
   - Description: SSH key for server access.
   - Impact: Could allow unauthorized server access.

## Phase 1: Rotation Instructions
1. **API Key**
   - Log in to the API management console.
   - Navigate to the API keys section.
   - Deactivate the old key and generate a new key.
   - Update all applications to use the new key.

2. **Database Password**
   - Access the database management interface.
   - Change the password to a strong, unique password.
   - Update connection strings in all relevant applications.

3. **Third-Party Service Token**
   - Log in to the third-party service dashboard.
   - Revoke the current token and create a new one.
   - Update the application configurations with the new token.

4. **SSH Key**
   - Generate a new SSH key pair.
   - Add the new public key to the server's authorized keys.
   - Revoke access of the old key by removing it from authorized keys.

## Notes
- Ensure to monitor logs for any suspicious activity after rotation.