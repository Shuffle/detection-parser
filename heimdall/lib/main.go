package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"encoding/json"
	"fmt"
	"github.com/google/cel-go/cel"
	"github.com/google/cel-go/checker/decls"
    "log"
    "unsafe"
)

// Attachment struct for email attachments
type Attachment struct {
	FileType  string `json:"filetype"`
	FileBytes string `json:"file_bytes"` // Using string for simplicity, consider []byte for actual implementation
	FileName  string `json:"filename"`
}

// Email struct for email details
type Email struct {
	Sender      string       `json:"sender"`
	Receiver    string       `json:"receiver"`
	Attachments []Attachment `json:"attachments"`
	Header      string       `json:"header"`
	Subject     string       `json:"subject"`
	BCC         []string     `json:"bcc"`
	CC          []string     `json:"cc"`
	Body        string       `json:"body"`
}

// emailToMap converts an Email struct to a map for CEL evaluation
func emailToMap(email Email) map[string]interface{} {
	convertedEmail := map[string]interface{}{
		"sender":    email.Sender,
		"receiver":  email.Receiver,
		"header":  email.Header,
        "attachments": []map[string]interface{}{},
		"subject": email.Subject,
		"bcc":     email.BCC,
		"cc":      email.CC,
		"body":    email.Body,
	}

    for _, attachment := range email.Attachments {
        convertedEmail["attachments"] = append(convertedEmail["attachments"].([]map[string]interface{}), map[string]interface{}{
            "filetype": attachment.FileType,
            "file_bytes": attachment.FileBytes,
            "filename": attachment.FileName,
        })
    }

    return convertedEmail
}

// EvaluateCELExpression evaluates a CEL expression against an email JSON
func EvaluateCELExpression(emailJSON string, expression string) (bool, error) {
	var email Email
	err := json.Unmarshal([]byte(emailJSON), &email)
	if err != nil {
		return false, fmt.Errorf("failed to parse JSON: %v", err)
	}

	env, err := cel.NewEnv(
		cel.Declarations(
			decls.NewVar("email", decls.NewMapType(decls.String, decls.Any)),
		),
	)
	if err != nil {
		return false, fmt.Errorf("failed to create CEL environment: %v", err)
	}

	ast, iss := env.Compile(expression)
	if iss.Err() != nil {
		return false, fmt.Errorf("failed to compile expression: %v", iss.Err())
	}

	prg, err := env.Program(ast)
	if err != nil {
		return false, fmt.Errorf("failed to create program: %v", err)
	}

	out, _, err := prg.Eval(map[string]interface{}{
		"email": emailToMap(email),
	})
	if err != nil {
		log.Printf("failed to evaluate expression: %v", err)
		return false, err
	}

	result, ok := out.Value().(bool)
	if !ok {
		return false, fmt.Errorf("expression did not return a boolean value")
	}

	return result, nil
}

//export EvaluateCELExpressionC
func EvaluateCELExpressionC(emailJSON *C.char, expression *C.char) *C.char {
	emailStr := C.GoString(emailJSON)
	exprStr := C.GoString(expression)
	result, err := EvaluateCELExpression(emailStr, exprStr)
	
	if err != nil {
		errStr := fmt.Sprintf("Error evaluating CEL expression: %s", err)
        log.Printf("Error evaluating CEL expression: %s", errStr)
		return C.CString(errStr)
	}
	
	if result {
		return C.CString("true")
	}
	return C.CString("false")
}

//export FreeCString
func FreeCString(str *C.char) {
    C.free(unsafe.Pointer(str))
}

func main() {
	// Main function is empty since we are creating a shared library
    expression := "email.sender == 'adityanrsinha@gmail.com'" // Example expression
    email := Email{
        Sender: "adityanrsinha@gmail.com",
    }

    emailJSON, err := json.Marshal(email)
    if err != nil {
        log.Fatalf("failed to marshal email: %v", err)
    }

    result, err := EvaluateCELExpression(string(emailJSON), expression)
    if err != nil {
        log.Fatalf("failed to evaluate expression: %v", err)
    }

    log.Printf("Result: %v\n", result)
}
