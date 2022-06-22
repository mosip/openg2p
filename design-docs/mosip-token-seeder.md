# MOSIP Token Seeder



## Overview

* We are addressing one of the last mile problems
* Token seeding - main function
* Off line authentication using QR code
* No biometric collection
* KYC fields in the form automatically populated
* Additional fields related to scheme may be present
* Seeder is agnostic to a scheme/registry/form as long as mandatory KYC fields are present.
* All the fields are forwarded to the department via Websub with attached MOSIP auth token.
* Auth failure handled — error message sent to Dept using the same Websub mechanism
* Data at rest (in WebSub) encoded using public key of subscribed department (like partner management in MOSIP).
* Part of openg2p umbrella
* No persistence of PII data
* Data security and private at ODK Center - **TBD**

## Design
