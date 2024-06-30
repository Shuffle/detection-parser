# shuffle-email-rules/main.py
import json
from evaluate import evaluate_email_expression, evaluate_gmail_expression

def main():
    # Example usage
    email_json = '{"sender": "test@example.com"}'
    expression = 'email.receiver.endsWith("@example.com")'

    result = evaluate_email_expression(email_json, expression)

    if type(result) != bool:
        if result.startswith("error:"):
            print(f"Error: {result[6:]}")
    else:
        print(f"Expression result: {result}")

    # Now to test for false
    expression = 'email.sender.endsWith("@!example.com")'
    result = evaluate_email_expression(email_json, expression)

    if type(result) != bool:
        if result.startswith("error:"):
            print(f"Error: {result[6:]}")
    else:
        print(f"Expression result: {result}")

    expression = 'email.receiver.endsWith("@shuffler.io")'

    # now, testing for gmail
    gmail_test_dict = {
    "snippet": "Test",
    "payload": {
        "partId": "",
        "mimeType": "multipart/alternative",
        "filename": "",
        "headers": [
            {
                "name": "Date",
                "value": "Sun, 30 Jun 2024 11:42:06 -0700"
            },
            {
                "name": "Subject",
                "value": "Some fixes failed for Page indexing issues on site shuffler.io"
            },
            {
                "name": "From",
                "value": "Google Search Console Team <sc-noreply@google.com>"
            },
            {
                "name": "To",
                "value": "aditya@shuffler.io"
            },
            {
                "name": "Content-Type",
                "value": "multipart/alternative; boundary=\"0000000000005ee218061c1fd61d\""
            }
        ],
        "body": {
            "size": 0
        },
        "parts": [
            {
                "partId": "0",
                "mimeType": "text/plain",
                "filename": "",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": "text/plain; charset=\"UTF-8\"; format=flowed; delsp=yes"
                    }
                ],
                "body": {
                    "size": 5,
                    "data": "eHl6=="
                }
            },
            {
                "partId": "1",
                "mimeType": "text/html",
                "filename": "",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": "text/html; charset=\"UTF-8\""
                    },
                    {
                        "name": "Content-Transfer-Encoding",
                        "value": "quoted-printable"
                    }
                ],
                "body": {
                    "size": 5,
                    "data": "PGRpdj54eXo8L2Rpdj4="
                }
            }
        ]
    },
    "sizeEstimate": 5,
    "historyId": "xyz",
    "internalDate": "1719790003609"
}
    
    gmail_test = json.dumps(gmail_test_dict)

    result = evaluate_gmail_expression(gmail_test, expression)
    print(result)

if __name__ == '__main__':
    main()
