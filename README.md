# Introduction

Email rules for everyone

## Installation

```bash
pip install shuffle-email-rules
```


## Usage

```python
from shuffle_email_rules.evaluate import evaluate_email_expression
email_json = '{"sender": "test@example.com"}'
expression = 'email.sender.endsWith("@example.com")'
result = evaluate_email_expression(email_json, expression)
print(result)
```

## To-do

Attach all binary .so files to the package to be uploaded to PyPI. Right now, only works on ARM"

