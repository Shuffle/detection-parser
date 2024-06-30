# shuffle-email-rules/main.py

from evaluate import evaluate_email_expression

def main():
    # Example usage
    email_json = '{"sender": "test@example.com"}'
    expression = 'email.sender.endsWith("@example.com")'

    result = evaluate_email_expression(email_json, expression)

    if result.startswith("error:"):
        print(f"Error: {result[6:]}")
    else:
        print(f"Expression result: {result}")

    # Now to test for false
    expression = 'email.sender.endsWith("@!example.com")'
    result = evaluate_email_expression(email_json, expression)

    if result.startswith("error:"):
        print(f"Error: {result[6:]}")
    else:
        print(f"Expression result: {result}")

if __name__ == '__main__':
    main()
