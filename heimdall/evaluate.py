import os
import ctypes

from .errors import HeimdallEvaluationError

# Get the directory path of the current module
module_dir = os.path.dirname(__file__)

platform = os.uname().sysname.lower()
# get if the architecture is arm64 or amd64
architecture = "arm64" if (os.uname().machine == "aarch64" or os.uname().machine == "arm64" ) else "amd64"

binary_name = f"libshuffleemail_{platform}_{architecture}"

try:
    lib_path = os.path.join(module_dir, 'lib', 'binaries', binary_name)

    # Load the library
    lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"Failed to load the library: {e}")
    exit(1)

# Define the function prototype
lib.EvaluateCELExpressionC.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.EvaluateCELExpressionC.restype = ctypes.c_char_p

lib.HandleGmailMessageC.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.HandleGmailMessageC.restype = ctypes.c_char_p

def evaluate_email_expression(email_json, expression):
    # Convert Python strings to bytes
    email_json_b = email_json.encode('utf-8')
    expression_b = expression.encode('utf-8')

    # Call the C function
    result_b = lib.EvaluateCELExpressionC(email_json_b, expression_b)

    # Convert the result back to a Python string
    result = result_b.decode('utf-8')

    if result == "true":
        return True
    
    if result == "false":
        return False
    
    if result.lower().startswith("error:"):
        err = result[6:]
        raise HeimdallEvaluationError(err)

    return result

def evaluate_gmail_expression(email_json: str, expression: str):
    # Convert Python strings to bytes
    email_json_b = email_json.encode('utf-8')
    expression_b = expression.encode('utf-8')

    # Call the C function
    result_b = lib.HandleGmailMessageC(email_json_b, expression_b)

    # Convert the result back to a Python string
    result = result_b.decode('utf-8')

    if result == "true":
        return True
    
    if result == "false":
        return False
    
    if result.lower().startswith("error:"):
        err = result[6:]
        raise HeimdallEvaluationError(err)

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