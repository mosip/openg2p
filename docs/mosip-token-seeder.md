# MOSIP Token Seeder

## Overview

MOSIP Token Seeder (MTS) is a standalone service that outputs [MOSIP Token ID](https://docs.mosip.io/1.2.0/id-lifecycle-management/identifiers#token-id) for a given input list of UIN/VIDs after performing authentication with [IDA](https://docs.mosip.io/1.2.0/id-authentication). The service is a convenience module that makes it easy for [Relying Parties](https://docs.mosip.io/1.2.0/id-authentication#relying-parties-and-policies) to perform bulk authentication to onboard users to their systems. One of the indented use cases of MTS is to seed existing beneficiary registries for deduplication. Similarly, entities like banks can run the MTS service to onboard users.

Some of the features of MTS:

* Bulk upload.
* Support for multiple inputs and outputs (see diagram below). For instance, a CSV file may be uploaded, and the downloaded file will contain a column with tokens populated.
* [REST interface](mosip-token-seeder.md#api).
* PII at rest is encrypted. Further, the PII is erased after processing.
* Works in asynchronous mode - queues all the requests.

![](https://github.com/mosip/openg2p/raw/main/docs/.gitbook/assets/seeder.png)

## Inputs

1. Direct Plain KYC Request
2. CSV Upload
3. ODK based upload
4. JSON Array Upload
5. Google Sheets upload
6. Form.IO Sheets upload
7. VC

## Outputs

1. Direct Synchronous Response
2. CSV
3. JSON

## Delivery method

1. Synchronous Response
2. WebSub
3. SFTP
4. Download URL

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
* Source Index to keep the sequence of row intact.
* Expiring the processed data as soon as its downloaded or reaches the expiry after the processing.
* **Secrets management** - Save the credentials for SFTP/ODK etc.
* **Status management** - Various status of a token seeding request. (Uploaded/Processing/Completed/Archived)
* **Database** - Data persistence for the whole system
  * <mark style="color:purple;">Derby Or SQLite for local in-memory storage.</mark>
  * <mark style="color:purple;">Design should be open for external connect to any db like Postgres/Oracle/SQL Server</mark>
  * <mark style="color:purple;">DB access design should also allow a seamless integration with odoo/openG2P, in case core service is directly integrated there.</mark>

## API

| API                    | Input      | Output | Method | Notes                                                                                                                                                           |
| ---------------------- | ---------- | ------ | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /authtoken/authfields  |            | array  | GET    | Get the MOSIP Auth Fields                                                                                                                                       |
| /authtoken/status/{id} | GUID       | json   | GET    | Get the status of Token Seeding Request submitted earlier                                                                                                       |
| /authtoken/file/{id}   | GUID       | file   | GET    | Gets the file (csv/json) if the seeding is completed.                                                                                                           |
| /authtoken/json        | json       | json   | POST   | Takes in json array along with field mapping and process the token seeding.                                                                                     |
| /authtoken/csv         | file, json | json   | POST   | Takes in csv file along with field mapping and process the token seeding.                                                                                       |
| /authtoken/odk         | json       | json   | POST   | Takes in input in VC format and process the token seeding.                                                                                                      |
| /authtoken/vc          | json       | json   | POST   | Takes in odk setup configuration and credentials to enable real-time odk pull or setup a scheduled odk pull. Token seeding will be done subsequent to odk pull. |

### Token API&#x20;

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

### Version 0.1.0&#x20;

#### Features

* Input type __ :- _****_ csv, json
* Output type _:-_ csv, json
* Delivery Type __ :- download
* Asynchronous token seeding
* Status API
* Download API
* Authfield Mapping
* Output file expiration
* Dockerization

### Design

![](https://raw.githubusercontent.com/mosip/openg2p/main/docs/\_images/mosip-token-token-seeder-block-diagram.png)
