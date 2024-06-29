import os
import ctypes

# Get the directory path of the current module
module_dir = os.path.dirname(__file__)

# Construct the path to libhello.so
lib_path = os.path.join(module_dir, 'lib', 'libhello.so')

# Load the library
lib = ctypes.CDLL(lib_path)

# Define the function prototype
lib.EvaluateCELExpressionC.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.EvaluateCELExpressionC.restype = ctypes.c_char_p

def evaluate_email_expression(email_json, expression):
    # Convert Python strings to bytes
    email_json_b = email_json.encode('utf-8')
    expression_b = expression.encode('utf-8')

    # Call the C function
    result_b = lib.EvaluateCELExpressionC(email_json_b, expression_b)

    # Convert the result back to a Python string
    result = result_b.decode('utf-8')

    return result


if __name__ == '__main__':
    # Example usage
    email_json = '{"sender": "test@example.com"}'
    expression = 'email.sender.endsWith("@example.com")'

    result = evaluate_email_expression(email_json, expression)

    if result.startswith("error:"):
        print(f"Error: {result[6:]}")
    else:
        print(f"Expression result: {result}")

    # now to test for false
    expression = 'email.sender.endsWith("@!example.com")'
    result = evaluate_email_expression(email_json, expression)

    if result.startswith("error:"):
        print(f"Error: {result[6:]}")
    else:
        print(f"Expression result: {result}")