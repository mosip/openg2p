# MOSIP Authentication

## Front end authentication

### Last mile scenarios

| Scenarios | Connectivity | Phone type | Phone ownership | ID type   |
| --------- | ------------ | ---------- | --------------- | --------- |
| R1        | 3G+          | Feature    | Personal        | USSD, SMS |
| R2        | 3G+          | Smart      | Personal        | Inji App  |
| R3        | 3G+          | Smart      | Family          | Inji App  |
| R4        | 3G+          | No phone   | -               | Card      |
| R5        | 2G           | Basic      | Personal        | USSD, SMS |
| R6        | 2G           | Feature    | Personal        | USSD, SMS |
| R7        | 2G           | Feature    | Family          | ?         |
| R8        | 2G           | No phone   | Card            |           |

### USSD Auth

* Enumerator authenticates beneficiary
  * Beneficiary types in a USSD message. Receives a token.
  * Enumerator reads the displayed token. Possible methods:
    * Using OCR.
    * Beneficiary sends the token by SMS to Enumerator (?)
  * Enumerator enters token in Brollie App.
  * The form gets filled automatically with necessary KYC information after verification from the server. (Can the the token be in signed verifiable credential format containing data such that connection to server is not required to fill the form? This may not be possible as USSD messages are limited in characters)
  * _How does the beneficiary verify that the enumerator is authentic?_

### Inji Auth

* Enumerator authenticates beneficiary&#x20;
  * Beneficiary generates a VID on her MOSIP Inji App.&#x20;
  * Beneficiary shares VC with Enumerator via Bluetooth.&#x20;
  * Enumerator verifies credentials on Brollie App.&#x20;
  * Clicks photograph of beneficiary.&#x20;
  * Brollie App authenticates the beneficiary using face matching.&#x20;
* The form gets filled automatically with necessary KYC information available in VC.
* &#x20;Enumerator uploads Auth information to server for backend authentication, issue of token and de-duplication



## Backend authentication
