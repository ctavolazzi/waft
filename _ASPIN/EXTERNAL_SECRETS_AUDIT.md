# External Secrets Audit

## Internal Secrets Requiring Rotation
1. **API Key for Service A**  
   - Rotation Period: 6 months  
   - Last Rotated: 2026-01-09 18:32:01  

2. **Database Password for Service B**  
   - Rotation Period: 3 months  
   - Last Rotated: 2026-02-09 18:32:01  

## External Secrets Management Infrastructure
- **Service A - AWS Secrets Manager**  
   - Manages API keys and sensitive configuration data.
   - Encrypted storage and automatic rotation support.

- **Service B - HashiCorp Vault**  
   - Secret management tool for sensitive data including tokens and passwords.
   - Access policies for fine-grained controls.

- **Service C - Azure Key Vault**  
   - Used for key management and storing sensitive information necessary for applications.