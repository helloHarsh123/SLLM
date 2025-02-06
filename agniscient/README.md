# Agniscient

A secure wrapper for LLM interactions that provides:
- Automatic PII anonymization
- Encrypted storage of conversation history
- Safe handling of sensitive data

## Installation
```bash
pip install agniscient
```

## Usage
```python
from agniscient import Config, SecureLLMClient

config = Config(
    openai_key="your-openai-key",
    our_key="your-encryption-key"
)

client = SecureLLMClient(config)
response = client.generate_response("Your prompt here")
```