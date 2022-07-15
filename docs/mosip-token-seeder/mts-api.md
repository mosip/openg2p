# MTS API

{% swagger method="get" path="/authtoken/authfields" baseUrl="" summary="Get the MOSIP Auth Fields" %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-response status="200: OK" description="Success Response" %}
```javascript
{
  "id": null,
  "version": null,
  "responsetime": "2020-01-01T06:09:33.371Z",
  "metadata": null,
  "response": {
    "authFieldList": [
      {
        "fieldname": "name",
        "datatype": "string"
      },
      {...},
      {...}
    ]
  },
  "errors": null
}
```
{% endswagger-response %}

{% swagger-response status="200: OK" description="Error Response" %}
```javascript
{
  "id": "string",
  "version": "string",
  "metadata": {},
  "responsetime": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
  "errors": [
    {
      "errorCode": "string",
      "message": "string"
    }
  ],
 "response": null
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger method="get" path="/authtoken/status/{id}" baseUrl="" summary="Get the status of Token Seeding Request submitted" %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-parameter in="query" name="id" type="String" required="true" %}
Request Identifier 
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="Success Response" %}
```javascript
{
  "id": "string",
  "version": "string",
  "responsetime": "2020-01-01T06:09:33.371Z",
  "metadata": [],
  "response": {
	'request_identifier':'483d491c-6688-4042-ba90-ef813ff618db'
  },
  "errors": null
}
```
{% endswagger-response %}

{% swagger-response status="200: OK" description="Error Response" %}
```javascript
{
  "id": "string",
  "version": "string",
  "metadata": {},
  "responsetime": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
  "errors": [
    {
      "errorCode": "string",
      "message": "string"
    }
  ],
 "response": null
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger method="get" path="/authtoken/file/{id}" baseUrl="" summary="Gets the file (csv/json) if the seeding is completed" %}
{% swagger-description %}

{% endswagger-description %}

{% swagger-parameter in="query" name="id" type="String" required="true" %}
Request Identifier
{% endswagger-parameter %}

{% swagger-response status="200: OK" description="" %}
{% code title="" %}
```javascript
{filename}.json  
```
{% endcode %}
{% endswagger-response %}

{% swagger-response status="200: OK" description="Error Response" %}
```javascript
{
  "id": "string",
  "version": "string",
  "metadata": {},
  "responsetime": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
  "errors": [
    {
      "errorCode": "string",
      "message": "string"
    }
  ],
 "response": null
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger src="../.gitbook/assets/openapi.json" path="undefined" method="undefined" %}
[openapi.json](../.gitbook/assets/openapi.json)
{% endswagger %}

#### Failure details

| Error Code  | Error Message                                  | Error Description |
| ----------- | ---------------------------------------------- | ----------------- |
| ATS-REQ-001 | json is not in valid format                    |                   |
| ATS-REQ-002 | invalid vid construct                          |                   |
| ATS-REQ-003 | name is not provided                           |                   |
| ATS-REQ-004 | gender is empty                                |                   |
| ATS-REQ-005 | gender value is wrong                          |                   |
| ATS-REQ-006 | date of birth is empty                         |                   |
| ATS-REQ-007 | not a valid date format for date of birth      |                   |
| ATS-REQ-008 | address is empty                               |                   |
| ATS-REQ-009 | vid or its mapping not present                 |                   |
| ATS-REQ-010 | name or its mapping not present                |                   |
| ATS-REQ-011 | gender or its mapping not present              |                   |
| ATS-REQ-012 | dateOfBirth or its mapping not present         |                   |
| ATS-REQ-013 | phoneNumber or its mapping not present         |                   |
| ATS-REQ-014 | emailId or its mapping not present             |                   |
| ATS-REQ-015 | fullAddress or its mapping not present         |                   |
| ATS-REQ-016 | no auth request found for the given identifier |                   |
| ATS-REQ-017 | auth request not processed yet                 |                   |
| ATS-REQ-100 | unknown error                                  |                   |
| ATS-REQ-101 | none of the record form a valid request        |                   |
| ATS-REQ-102 | invalid input                                  |                   |
