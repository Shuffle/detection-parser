# shuffle-email-rules/__init__.py

from .evaluate import evaluate_email_expression
from .yaml_parser import parse_yaml_file

__all__ = ['evaluate_email_expression', 'evaluate_file_expression']
