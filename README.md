# Introduction

Detection rule parser for everyone with focus on Email

## Installation

```bash
pip3 install shuffle-heimdall
```


## Usage

```python
from heimdall.evaluate import evaluate_email_expression
sender = """{
    "email": {
        "domain": {
            "domain": "shuffler.io"
        },
        "email": "support@shuffler.io"
    }
}"""

expression = 'sender.email.domain.domain == "twitter.com"'
result = evaluate_email_expression(sender, expression)
print(result)

## Try out file based evaluation
from heimdall.evaluate import evaluate_file_expression

file_path = "rules/impersonation_of_twitter.yml"

sender = """{
    "email": {
        "domain": {
            "domain": "nottwitter.com"
        }
    }
}"""

result = evaluate_file_expression(file_path, sender)
print(result)
```

To see more examples, check out the [main.py](./heimdall/main.py) file.

## To-do

Works on most platforms. The power of heimdall should shine when you have a lot of emails to process but you want to write simple code that is also fast.

- [ ] Add support for outlook API result
- [x] Add support for gmail API result (`evaluate_gmail_expression()`)
- [ ] Add support for gmail API when in mass
- [ ] Make setup.py pull the right binary during install instead of having everything in the repo.


## Dev

1. Building the package
```bash
python3 setup.py sdist bdist_wheel
```
