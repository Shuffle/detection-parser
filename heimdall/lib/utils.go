package main

import (
	"encoding/base64"
	"strings"
	"regexp"
	"log"
	"time"
)

func Base64Decode(input string) (string, error) {
	encoded := strings.TrimSpace(input)
	encoded = strings.ReplaceAll(input, "\n", "")
	encoded = strings.ReplaceAll(input, "\r", "")

	// Add padding if necessary
	switch len(input) % 4 {
	case 2:
		encoded += "=="
	case 3:
		encoded += "="
	}
	decoded, err := base64.URLEncoding.DecodeString(encoded)
	if err != nil {
		return "", err
	}
	return string(decoded), nil

}

func extractEmail(input string) string {
	// Regular expression to match the email address in the input text
	re := regexp.MustCompile(`[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`)
	email := re.FindString(input)
	return email
}

// emailToMap converts an Email struct to a map for CEL evaluation
func emailToMap(email Email) map[string]interface{} {
	convertedEmail := map[string]interface{}{
		"sender":    email.Sender,
		"receiver":  email.Receiver,
		"headers":  []map[string]interface{}{},
        "attachments": []map[string]interface{}{},
		"subject": email.Subject,
		"bcc":     email.BCC,
		"cc":      email.CC,
		"body":    email.Body,
		"body_html": email.BodyHTML,
	}

    for _, attachment := range email.Attachments {
        convertedEmail["attachments"] = append(convertedEmail["attachments"].([]map[string]interface{}), map[string]interface{}{
            "filetype": attachment.FileType,
            "file_bytes": attachment.FileBytes,
            "filename": attachment.FileName,
        })
    }

	for _, header := range email.Headers {
		convertedEmail["headers"] = append(convertedEmail["headers"].([]map[string]interface{}), map[string]interface{}{
			"name":  header.Name,
			"value": header.Value,
		})
	}

    return convertedEmail
}

// add error handling later
func GmailToHeimdall(email Gmail ) Email {
	// return Email{
	// 	Sender: email.From,
	// 	Receiver: email.To,
	// 	Attachments: []Attachment{},
	// 	Header: email.Header,
	// 	Subject: email.Subject,
	// 	BCC: []string{},
	// 	CC: []string{},
	// 	Body: email.Body,
	// }

	heimdallEmail := Email{}
	// find "Delivered-To" header in Gmail.Payload.Headers
	for _, header := range email.Payload.Headers {
		if header.Name == "From" {
			// heimdallEmail.Receiver = header.Value
			heimdallEmail.Sender = extractEmail(header.Value)
		}

		if header.Name == "To" {
			heimdallEmail.Receiver = extractEmail(header.Value)
		}

		if header.Name == "Subject" {
			heimdallEmail.Subject = header.Value
		}

		if header.Name == "Date" {
			layout := "Mon, 02 Jan 2006 15:04:05 -0700"
			t, err := time.Parse(layout, header.Value)
			if err != nil {
				log.Printf("[WARNING]: failed to parse date: %v", err)
				header.Value = ""
			} else {
				heimdallEmail.ReceivedAt = int(t.Unix())
			}
		}

		if header.Name == "Bcc" {
			heimdallEmail.BCC = append(heimdallEmail.BCC, extractEmail(header.Value))
		}

		if header.Name == "Cc" {
			heimdallEmail.CC = append(heimdallEmail.CC, extractEmail(header.Value))
		}
	}

	for index, parts := range email.Payload.Parts {
		if parts.Body.Size == 0 {
			for newIndex, part := range parts.Parts {
				if newIndex == 0 {
					// base64 decode the body
					base64msg := part.Body.Data
					decoded, err := Base64Decode(base64msg)
					if err != nil {
						log.Printf("[WARNING]: failed to decode base64 (1): %v", err)
					} else {
						heimdallEmail.Body = decoded
					}
				} else {
					base64msg := part.Body.Data
					decoded, err := Base64Decode(base64msg)
					if err != nil {
						log.Printf("[WARNING]: failed to decode base64 (2): %v", err)
					} else {
						heimdallEmail.BodyHTML = string(decoded)
					}
				}
			}

			break
		}

		if index == 0 {
			// base64 decode the body
			base64msg := parts.Body.Data
			decoded, err := Base64Decode(base64msg)
			if err != nil {
				log.Printf("[WARNING]: failed to decode base64 (3): %v", err)
			} else {
				heimdallEmail.Body = string(decoded)
			}
		} else {
			base64msg := parts.Body.Data
			decoded, err := Base64Decode(base64msg)
			if err != nil {
				log.Printf("[WARNING]: failed to decode base64 (4): %v", err)
			} else {
				heimdallEmail.BodyHTML = string(decoded)
			}
		}
	}

	return heimdallEmail
}


