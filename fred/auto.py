# Re-running the entire process to restore variables
# Mostly generated with a few fixes


import re
import sys

# Example input text

input_text = """|
  type.inbound
  and any(attachments,
          .file_extension == "pdf"
          and any(file.explode(.),
                  (
                    (any(.scan.strings.strings, strings.icontains(., '/JavaScript')))
                    and (any(.scan.strings.strings, strings.icontains(., '/JS ('))))
                  )
          )

  and (
    (
      profile.by_sender().prevalence in ("new", "outlier")
      and not profile.by_sender().solicited
    )
    or (
      profile.by_sender().any_messages_malicious_or_spam
      and not profile.by_sender().any_false_positives
    )
  )

  // negate highly trusted sender domains unless they fail DMARC authentication
  and (
    (
      sender.email.domain.root_domain in $high_trust_sender_root_domains
      and (
        any(distinct(headers.hops, .authentication_results.dmarc is not null),
            strings.ilike(.authentication_results.dmarc, "*fail")
        )
      )
    )
    or sender.email.domain.root_domain not in $high_trust_sender_root_domains
  )
"""

def fix_text(input_text):
    replacements = [
        ".file_extension",
        "sender.",
        "attachments",
    ]

    for replacement in replacements:
        newreplacement = replacement.replace("", "")
        if not replacement.startswith("."):
            newreplacement = f".{replacement}"

        print("Replacement: ", replacement)
        input_text = input_text.replace(replacement, f"mail{newreplacement}", -1)

    input_text = input_text.replace("explode(.)", "explode()", -1)
    input_text = input_text.replace("$high_trust_sender_root_domains", "high_trust_sender_root_domains()", -1)
    replacements = [
        ".scan",
    ]

    for replacement in replacements:
        input_text = input_text.replace(replacement, f"attachment{replacement}", -1)

    # Debugging with:
    # $ python3 auto.py debug 102
    if len(sys.argv) > 2:
        number = 102 

        if sys.argv[1] == "debug":

            # Check is sys.argv[2] is a number
            try:
                number = int(sys.argv[2])
            except ValueError:
                pass

            print()
            print()
            print(f"'{input_text[number-20:number]}'{input_text[number]}'{input_text[number+1:number+20]}'")
            print()
            print()

    return input_text



# Regular expressions for different token types
token_patterns = [
    (r'\band\b|\bor\b|\bnot\b|\bany\b', 'LOGICAL_OPERATOR'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),

    (r'".*?"', 'STRING_LITERAL'),

    (r'file.[a-z_]+\(\)', 'FUNCTION_CALL'),
    (r'profile\.[a-z_]+\(\)\.\w+', 'FUNCTION_CALL'),
    (r'high_trust_sender_root_domains\(\)', 'FUNCTION_CALL'),
    (r'distinct\(.*?\)', 'FUNCTION_CALL'),

    (r'strings\.icontains\(.*?\)', 'FUNCTION_CALL'),
    (r'strings\.ilike\(.*?\)', 'FUNCTION_CALL'),

    (r'in', 'IN_OPERATOR'),
    (r',', 'COMMA'),

    (r'mail\.[A-Za-z_\.]+', 'STRING_LITERAL'),  
    (r'attachment\.[A-Za-z_\.]+', 'STRING_LITERAL'),  
    (r'=', 'STRING_LITERAL'),  
    (r'type\.\binbound\b|\boutbound\b', 'STRING_LITERAL'),  
    (r'//.*', 'COMMENT'),

    (r'\|', None),  # Ignore or handle the '|' character
    (r'\s+', None),  # Ignore spaces
]

# Tokenizer function
def tokenize(text):
    tokens = []
    idx = 0
    while idx < len(text):
        match = None
        for pattern, token_type in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(text, idx)
            if match:
                if token_type:
                    tokens.append((match.group(0), token_type))
                idx = match.end()
                break

        if not match:
            raise ValueError(f"Unexpected token at index {idx}: {text[idx]}")
    return tokens

# Parser class to generate an AST
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    def eat(self, token_type):
        current = self.current_token()
        print("CURRENT: ", current)
        if current and current[1] == token_type:
            self.pos += 1
            return current[0]

        print(f"Unexpected token: {current}")
        return None 
        raise ValueError(f"Unexpected token: {current}")

    def parse_expression(self):
        """Parse an expression with 'and', 'or', 'not'."""
        result = self.parse_term()
        while self.current_token() and self.current_token()[1] == 'LOGICAL_OPERATOR':
            operator = self.eat('LOGICAL_OPERATOR')
            right = self.parse_term()
            result = (operator, result, right)

        return result

    def parse_term(self):
        """Parse a term which could be a function call or a parenthesized expression."""
        token = self.current_token()
        if token[1] == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr

        elif token[1] == 'FUNCTION_CALL':
            return self.eat('FUNCTION_CALL')

        #elif token[1] == 'LOGICAL_OPERATOR' and token[0] == 'not':
        elif token[1] == 'LOGICAL_OPERATOR':
            self.eat('LOGICAL_OPERATOR')
            return ('not', self.parse_term())

        elif token[1] == 'IN_OPERATOR':
            left = self.eat('FUNCTION_CALL')
            self.eat('IN_OPERATOR')
            right = self.parse_in_expression()
            return f"{left} in {right}"

        elif token[1] == 'STRING_LITERAL':
            print("TOKEN: ", token[0])

            if token[0] == "type.inbound" or token[1] == "type.outbound":

                self.pos += 1
                return "mail.%s" % token[0]

            eaten = self.eat('STRING_LITERAL')
            print("EATEN: ", eaten)
            print()
            return eaten

        else:
            raise ValueError(f"Unexpected term: {token}")

    def parse_in_expression(self):
        """Parse the list after 'in'."""
        items = []
        self.eat('LPAREN')
        while self.current_token()[1] != 'RPAREN':
            item = self.eat('STRING_LITERAL')
            items.append(item)
            if self.current_token()[1] == 'COMMA':
                self.eat('COMMA')

        self.eat('RPAREN')
        return f"({', '.join(items)})"


# Translator function to convert AST to Python code
def ast_to_python(ast):
    """Translate the AST to a valid Python expression."""

    if isinstance(ast, tuple):
        operator = ""
        left = ""
        right = ""

        print("Ast: ", ast)
        try:
            operator, left, right = ast
        except ValueError:
            operator, left = ast

        if operator == 'and':
            return f"({ast_to_python(left)} and {ast_to_python(right)})"
        elif operator == 'or':
            return f"({ast_to_python(left)} or {ast_to_python(right)})"
        elif operator == 'not':
            return f"(not {ast_to_python(left)})"
        elif operator == 'any':
            return "any"
            #return f"(not {ast_to_python(left)})"
            #return f"Not implemented"
    else:
        # If it's a function call or other terminal value, return it as is
        return ast

# Example: profile object with sample data
class Profile:
    def by_sender(self):
        return self

    def prevalence(self):
        return "new"

    def solicited(self):
        return False

    def any_messages_malicious_or_spam(self):
        return True

    def any_false_positives(self):
        return False

# Example: profile object with sample data
class File:
    def explode(self):
        return self

    def scan(self):
        return self

    def strings(self):
        return self

    def icontains(self, value):
        return True

    def file_extension(self):
        return "pdf"

# Sample profile object
profile = Profile()
file = File()

# Step 1: Tokenize the input text
input_text = fix_text(input_text)
tokens = tokenize(input_text)

# Step 2: Parse the tokens into an AST
parser = Parser(tokens)

ast = parser.parse_expression()
print("AST: ", ast)

# Step 3: Translate the AST into Python code
python_code = ast_to_python(ast)


# Step 4: Evaluate the generated Python code
python_code = """
import json
from types import SimpleNamespace

# Inject the mail object here somehow
mail_object = {
    "type": {
        "inbound": True,
        "outbound": False,
    }, 
    "attachments": [{
        "file_extension": "pdf",
        "explode": {
            "scan": {
                "strings": {
                    "strings": ["/JavaScript", "/JS ("]
                }
            }
        }
    }],
}

json_str = json.dumps(mail_object)

mail = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))

output = %s
""" % python_code
print("\n\n\nPYTHON CODE:\n", python_code)

globals_dict = globals()
result = exec(python_code, globals_dict)
print("VALUE: ", globals_dict["output"])

# Output the generated Python code and the evaluation result
#print(python_code, result)
