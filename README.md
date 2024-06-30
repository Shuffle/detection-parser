# Introduction

Email rules for everyone

## Installation

```bash
pip install shuffle-heimdall
```


## Usage

```python
from heimdall.evaluate import evaluate_email_expression
email_json = '{"sender": "test@example.com"}'
expression = 'email.sender.endsWith("@example.com")'
result = evaluate_email_expression(email_json, expression)
print(result)
```

## To-do

Works on most platforms. The power of heimdall should shine when you have a lot of emails to process but you want to write simple code that is also fast.
