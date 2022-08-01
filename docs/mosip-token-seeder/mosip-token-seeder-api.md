---
description: >-
  MOSIP Token Seeder API is a toolkit for generating MOSIP auth token in bulk
  for the enrolled users.
---

# MOSIP Token Seeder API

Email: [Support](mailto:info@mosip.io) Web: [Support](https://mosip.io/contact.php) License: [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/)

## Authtoken (JSON) <a href="#mosip-token-seeder-default" id="mosip-token-seeder-default"></a>

```http
POST /authtoken/json HTTP/1.1

Content-Type: application/json
Accept: application/json
```

### `POST /authtoken/json`

```json
{
  "id": "string",
  "version": "string",
  "metadata": "string",
  "requesttime": "2019-08-24T14:15:22Z",
  "request": {
    "output": "string",
    "deliverytype": "string",
    "authdata": [
      {}
    ],
    "mapping": {
      "vid": "vid",
      "name": [
        "fname","lname"
      ],
      "gender": "gender",
      "dob": "dob",
      "phoneNumber": "phoneNumber",
      "emailId": "emailId",
      "fullAddress": [
        "fullAddress"
      ]
    },
    "lang": "string"
  }
}
```

#### 200 Response

```json
{
  "id": "mosip.token.seeder",
  "version": "1.0",
  "metadata": {},
  "responsetime": "2022-07-14T19:17:14.940894",
  "errors": [
    {
      "errorCode": "string",
      "errorMessage": "string"
    }
  ],
  "response": {
       "request_identifier" :"[GUID]"
  }
}
```

## Authtoken (CSV)

```http
POST /authtoken/csv HTTP/1.1

Content-Type: multipart/form-data
Accept: application/json
```

### `POST /authtoken/csv`

```yaml
request: {
  "id": "string",
  "version": "string",
  "metadata": "string",
  "requesttime": "2019-08-24T14:15:22Z",
  "request": {
    "output": "string",
    "deliverytype": "string",
    "mapping": {
      "vid": "vid",
      "name": [
        "name"
      ],
      "gender": "gender",
      "dob": "dob",
      "phoneNumber": "phoneNumber",
      "emailId": "emailId",
      "fullAddress": [
        "fullAddress"
      ]
    },
    "lang": "string"
  }
}
csv_file: string
```

#### 200 Response

```json
{
  "id": "mosip.token.seeder",
  "version": "1.0",
  "metadata": {},
  "responsetime": "2022-07-14T19:17:14.940894",
  "errors": [
    {
      "errorCode": "string",
      "errorMessage": "string"
    }
  ],
  "response": {
       "request_identifier" :"[GUID]"
  }
}
```

## Authtoken (ODK)

```http
POST /authtoken/odk HTTP/1.1

Content-Type: application/json
Accept: application/json
```

### `POST /authtoken/odk`

```yaml
{
    "id": "string",
    "version": "string",
    "metadata": "",
    "requesttime": "2022-06-21T10:10:10.121Z",
    "request": {
        "output":"json",
        "deliverytype":"download",
        "lang":"eng",
        "odkconfig":{
            "odataurl":"https://odk.openg2p.mosip.net/v1/projects/1/forms/meals_program.svc",
            "baseurl":"odk.openg2p.mosip.net",
            "version":"v1",
            "projectid":"1",
            "formid":"meals_program",
            "email":"xxxxx@xxx.com",
            "password":"xxxxxxxx",  
            "startdate":"",
            "enddate":""
            },
        "mapping": {
            "vid" : "pcn",
            "phoneNumber": "phone",
            "emailId" : "email",
            "name" : ["fullName"],
            "gender" : "gender",
            "fullAddress" : ["address", "city", "state"],
            "dob":"dateOfBirth"
           
        }
    }
}
```

#### 200 Response

```yaml
{
  "id": "mosip.token.seeder",
  "version": "1.0",
  "metadata": {},
  "responsetime": "2022-07-14T19:17:14.940894",
  "errors": [
    {
      "errorCode": "string",
      "errorMessage": "string"
    }
  ],
  "response": {
       "request_identifier" :"[GUID]"
  }
}
```

## Fetch Status

```http
GET /authtoken/status/{id} HTTP/1.1

Accept: application/json
```

### `GET /authtoken/status/{id}`

#### Parameters <a href="#fetch_status_authtoken_status__id__get-parameters" id="fetch_status_authtoken_status__id__get-parameters"></a>

| Name | In                 | Type | Required | Description |
| ---- | ------------------ | ---- | -------- | ----------- |
| id   | request identifier | any  | true     | none        |

#### 200 Response

```json
{
  "id": "mosip.token.seeder",
  "version": "1.0",
  "metadata": {},
  "responsetime": "2022-07-14T19:17:14.940894",
  "errors": [
    {
      "errorCode": "string",
      "errorMessage": "string"
    }
  ],
  "response": {
  "status":"processed"
  }
}
```

## Download File

```http
GET /authtoken/file/{id} HTTP/1.1

Accept: application/json
```

### `GET /authtoken/file/{id}`

#### Parameters <a href="#download_file_authtoken_file__id__get-parameters" id="download_file_authtoken_file__id__get-parameters"></a>

| Name | In                  | Type   | Required | Description |
| ---- | ------------------- | ------ | -------- | ----------- |
| id   | request\_identifier | string | true     | none        |

#### 200 Response

```json
file
```

## Failure Details

| Error Code  | Error Message                                  |
| ----------- | ---------------------------------------------- |
| ATS-REQ-001 | json is not in valid format                    |
| ATS-REQ-002 | invalid vid construct                          |
| ATS-REQ-003 | name is not provided                           |
| ATS-REQ-004 | gender is empty                                |
| ATS-REQ-005 | gender value is wrong                          |
| ATS-REQ-006 | date of birth is empty                         |
| ATS-REQ-007 | not a valid date format for date of birth      |
| ATS-REQ-008 | address is empty                               |
| ATS-REQ-009 | vid or its mapping not present                 |
| ATS-REQ-010 | name or its mapping not present                |
| ATS-REQ-011 | gender or its mapping not present              |
| ATS-REQ-012 | dateOfBirth or its mapping not present         |
| ATS-REQ-013 | phoneNumber or its mapping not present         |
| ATS-REQ-014 | emailId or its mapping not present             |
| ATS-REQ-015 | fullAddress or its mapping not present         |
| ATS-REQ-016 | no auth request found for the given identifier |
| ATS-REQ-017 | auth request not processed yet                 |
| ATS-REQ-18  | no odk baseurl provided                        |
| ATS-REQ-19  | no email provided                              |
| ATS-REQ-20  | no password provided                           |
| ATS-REQ-21  | no odk project id provided                     |
| ATS-REQ-22  | no odk form id provided                        |
| ATS-REQ-23  | no submissions found for odk pull              |
| ATS-REQ-100 | unknown error                                  |
| ATS-REQ-101 | none of the record form a valid request        |
| ATS-REQ-102 | invalid input                                  |

