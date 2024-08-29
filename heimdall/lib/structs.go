package main

type GmailParts struct {
	Headers []struct {
		Name  string `json:"name"`
		Value string `json:"value"`
	}
	FileName string `json:"filename"`
	Body     struct {
		Data string `json:"data"`
		Size int    `json:"size"`
	}
	Parts []GmailParts `json:"parts"`
}

type Gmail struct {
	Payload struct {
		Headers []struct {
			Name  string `json:"name"`
			Value string `json:"value"`
		}
		FileName string       `json:"filename"`
		Parts    []GmailParts `json:"parts"`
	} `json:"payload"`
}

// Attachment struct for email attachments
type Attachment struct {
	FileType  string `json:"filetype"`
	FileBytes string `json:"file_bytes"` // Using string for simplicity, consider []byte for actual implementation
	FileName  string `json:"filename"`
}

type Domain struct {
	Domain string `json:"domain"`
}

type Email struct {
	Domain Domain `json:"domain"`
}

type Sender struct {
	Email Email `json:"email"`
}

// // Email struct for email details
// type Email struct {
// 	Sender      string       `json:"sender"`
// 	Receiver    string       `json:"receiver"`
// 	ReceivedAt  int       	 `json:"received_at"` // Unix timestamp
// 	Attachments []Attachment `json:"attachments"`
// 	Headers 	[]struct {
// 		Name string `json:"name"`
// 		Value string `json:"value"`
// 	} `json:"headers"`
// 	Subject     string       `json:"subject"`
// 	BCC         []string     `json:"bcc"`
// 	CC          []string     `json:"cc"`
// 	Body        string       `json:"body"`
// 	BodyHTML    string       `json:"body_html"`
// }
