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
    // "unsafe"
)

func EvaluateCELExpression(senderJSON string, expression string) (bool, error) {
	var sender Sender
	err := json.Unmarshal([]byte(senderJSON), &sender)
	if err != nil {
		return false, fmt.Errorf("failed to parse JSON: %v", err)
	}

	// Convert Sender struct to a map
	senderMap := map[string]interface{}{
		"email": map[string]interface{}{
			"domain": map[string]interface{}{
				"domain": sender.Email.Domain.Domain,
			},
			"email": sender.Email.Email,
		},
	}

	env, err := cel.NewEnv(
		cel.Declarations(
			decls.NewVar("sender", decls.NewMapType(decls.String, decls.Any)),
	))

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

	log.Printf("senderMap: %v\n", senderMap)

	out, _, err := prg.Eval(map[string]interface{}{
		"sender": senderMap,
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
func EvaluateCELExpressionC(senderJSON *C.char, expression *C.char) *C.char {
	senderStr := C.GoString(senderJSON)
	exprStr := C.GoString(expression)
	result, err := EvaluateCELExpression(senderStr, exprStr)
	
	if err != nil {
		errStr := fmt.Sprintf("Error: %s", err)
		return C.CString(errStr)
	}
	
	if result {
		return C.CString("true")
	}
	return C.CString("false")
}

// func HandleGmailMessage(gmailJSON string, expression string) (bool, error) {
// 	var gmail Gmail
// 	err := json.Unmarshal([]byte(gmailJSON), &gmail)
// 	if err != nil {
// 		return false, fmt.Errorf("failed to parse JSON (Gmail): %v", err)
// 	}

// 	heimdallEmail := GmailToHeimdall(gmail)
// 	emailMap := emailToMap(heimdallEmail)
// 	emailJSON, err := json.Marshal(emailMap)
// 	if err != nil {
// 		return false, fmt.Errorf("failed to marshal email: %v", err)
// 	}

// 	return EvaluateCELExpression(string(emailJSON), expression)
// }

//export HandleGmailMessageC
func HandleGmailMessageC(gmail *C.char, expression *C.char) *C.char {
	// gmailStr := C.GoString(gmail)
	// exprStr := C.GoString(expression)
	// result, err := HandleGmailMessage(gmailStr, exprStr)
	
	// if err != nil {
	// 	errStr := fmt.Sprintf("Error: %s", err)
	// 	return C.CString(errStr)
	// }
	
	// if result {
	// 	return C.CString("true")
	// }
	// return C.CString("false")

	return C.CString("false")
}

func main() {
	// Main function is empty since we are creating a shared library
    expression := "!(sender.email.domain.domain in ['twitter.com', 'privaterelay.appleid.com', 'stripe.com', 'x.com', 'twitter.discoursemail.com'])"
	sender := Sender{
		Email: Email{
			Domain: Domain{
				Domain: "twitter.com",
			},
		},
	}
	
	senderJSON, err := json.Marshal(sender)
	if err != nil {
		log.Fatalf("failed to marshal sender: %v", err)
	}

    result, err := EvaluateCELExpression(string(senderJSON), expression)
    if err != nil {
        log.Fatalf("failed to evaluate expression: %v", err)
    }

    log.Printf("Result: %v\n", result)
}
