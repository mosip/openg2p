# MOSIP Token Seeder

## Initial thoughts

* We are addressing one of the last mile problems
* Token seeding - main function
* KYC fields in the form automatically populated
* Additional fields related to scheme may be present
* Seeder is agnostic to a scheme/registry/form as long as mandatory KYC fields are present.
* All the fields are forwarded to the department via Websub with attached MOSIP auth token.
* Auth failure handled — error message sent to Dept using the same Websub mechanism
* Data at rest (in WebSub) encoded using public key of subscribed department (like partner management in MOSIP).
* No persistence of PII data

## Octopus model architecture

A multi-point system which can cater any type of input and output to make the MOSIP Token Seeder effective in any possible use cases.

### Inputs

1. Direct Plain KYC Request
2. CSV Upload
3. ODK based upload
4. JSON Array Upload
5. Google Sheets upload
6. Form.IO Sheets upload
7. VC

### Outputs

1. Direct Synchronous Response
2. CSV
3. JSON

### Delivery method

1. Synchronous Response
2. WebSub
3. SFTP
4. Download URL

### Design considerations/open questions

* **Secrets management** - Save the credentials for SFTP/ODK etc.
* **Status management** - Various status of a token seeding request. (Uploaded/Processing/Completed/Archived)
* **Database** - Data persistence for the whole system
* **Processed CSV/JSON** - How do we persist the csv/json for which token generation is completed.
* **VC** - Should we be verifying the Digital Signature
* **VC** - Shouldn't we define a output fields?
* **Biometric inputs** - Should we consider Biometric inputs for the authentication?
* **Scheduled jobs** - Repeated tasks can be configured through a API call (for instance, Daily ODK Pull)
* **Status check** - API for querying on the status of a token seeding request.
* **MOSIP authentication fields** - API to fetch the list of MOSIP Authentication fields so that a mapper configuration can be generated to make CSV/JSON token seeder request.   &#x20;

### API

| API                                               | Input                                              | Output                                               | Method | Notes                                                     |
| ------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------- | ------ | --------------------------------------------------------- |
| /authtoken/authfields                             |                                                    | Array                                                | get    | Get the MOSIP Auth Fields                                 |
| /authtoken/status/{id}                            | GUID                                               | json                                                 | get    | Get the status of Token Seeding Request submitted earlier |
| /authtoken/file/{id}                              | GUID                                               | file                                                 | get    | Gets the file (csv/json) if the seeding is completed.     |
| /[authtoken](mosip-token-seeder.md#kyc-token-api) | ref [Input Type](mosip-token-seeder.md#input-type) | ref [Output Type](mosip-token-seeder.md#output-type) | post   | KYC Token generation service                              |

### KYC token API&#x20;

`/authtoken/input/{input-type}/output/{output-type}/delivery/{delivery-type}`

#### Input type

* `json`
* `odk`
* `csv`
* `vc`
* `form.io`
* `googlsheet`

#### Output type <a href="#output-type" id="output-type"></a>

* json
* csv

#### Delivery method

* websub
* download
* sftp

#### Sample API endpoint

* `/authtoken/input/json/output/json/delivery/websub`
* `/authtoken/input/csv/output/json/delivery/websup`
* `/authtoken/input/vc/output/json/delivery/sftp`
* `/authtoken/input/vc/output/csv/delivery/download`
* `/authtoken/input/csv/output/csv/delivery/sftp`



## Design
