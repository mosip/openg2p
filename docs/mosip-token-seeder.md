# MOSIP Token Seeder

## Overview

![](https://github.com/mosip/openg2p/raw/main/docs/.gitbook/assets/seeder.png)

## Overview

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
  * <mark style="color:purple;">Derby Or SQLite for local in-memory storage.</mark>
  * <mark style="color:purple;">Design should be open for external connect to any db like Postgres/Oracle/SQL Server</mark>&#x20;
  * <mark style="color:purple;">DB access design should also allow a seamless integration with odoo/openG2P, in case core service is directly integrated there.</mark> &#x20;
* **Processed CSV/JSON** - How do we persist the csv/json for which token generation is completed.
* **VC** - Should we be verifying the Digital Signature
* **VC** - Shouldn't we define a output fields?
* **Biometric inputs** - Should we consider Biometric inputs for the authentication?
* **Scheduled jobs** - Repeated tasks can be configured through a API call (for instance, Daily ODK Pull)
* **Status check** - API for querying on the status of a token seeding request.
* **MOSIP authentication fields** - API to fetch the list of MOSIP Authentication fields so that a mapper configuration can be generated to make CSV/JSON token seeder request.   &#x20;
* <mark style="color:purple;">Queue Management - Avoid using external systems for any queue implementation</mark>
* <mark style="color:purple;">Decoupled Seeder Service - The seeder service should be separate enough</mark>&#x20;
* <mark style="color:purple;">Programing language - Python</mark>
* <mark style="color:purple;">Framework - Fast API</mark>

<mark style="color:purple;"></mark>

### API

| API                    | Input      | Output | Method | Notes                                                                                                                                                            |
| ---------------------- | ---------- | ------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /authtoken/authfields  |            | array  | GET    | Get the MOSIP Auth Fields                                                                                                                                        |
| /authtoken/status/{id} | GUID       | json   | GET    | Get the status of Token Seeding Request submitted earlier                                                                                                        |
| /authtoken/file/{id}   | GUID       | file   | GET    | Gets the file (csv/json) if the seeding is completed.                                                                                                            |
| /authtoken/json        | json       | json   | POST   | Takes in json array along with field mapping and process the token seeding.                                                                                      |
| /authtoken/csv         | file, json | json   | POST   | Takes in csv file along with field mapping and process the token seeding.                                                                                        |
| /authtoken/odk         | json       | json   | POST   | Takes in input in VC format and process the token seeding.                                                                                                       |
| /authtoken/vc          | json       | json   | POST   | Takes in odk setup configuration and credentials to enable real-time odk pull or setup a scheduled odk pull.  Token seeding will be done subsequent to odk pull. |

### KYC token API&#x20;

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



### Design

****

**Token seeder request flow**

1. Validate the request input
2. Do a scan for the input.
3. Split the input and validate
4. If valid&#x20;
   1. Create Identifier
   2. Create Default status equals "Submitted"
   3. Split the input, convert to JSON and persist with the status "Submitted"
   4. Return status submitted with the identifier
5. Else
   1. Return Error

#### Notes

* SourceIndex to keep the sequence of row intact.
* Expiring the processed data as soon as its downloaded or reaches the expiry after the processing.
