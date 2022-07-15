# MOSIP Token Seeder

## Overview

MOSIP Token Seeder (**MTS**) is a standalone service that outputs [MOSIP Token ID](https://docs.mosip.io/1.2.0/id-lifecycle-management/identifiers#token-id) for a given input list of UIN/VIDs after performing authentication with [IDA](https://docs.mosip.io/1.2.0/id-authentication). The service is a convenience module that makes it easy for [Relying Parties](https://docs.mosip.io/1.2.0/id-authentication#relying-parties-and-policies) to perform bulk authentication to onboard users to their systems. One of the indented use cases of MTS is to seed existing beneficiary registries for deduplication. Similarly, entities like banks can run the MTS service to onboard users.

Some of the features of MTS:

* Bulk upload.
* Support for multiple inputs and outputs (see diagram below). For instance, a CSV file may be uploaded, and the downloaded file will contain a column with tokens populated.
* [REST interface](./#api).
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

### Delivery type

1. Synchronous Response
2. Web Sub
3. SFTP
4. Download URL

## Design

![](https://raw.githubusercontent.com/mosip/openg2p/main/docs/\_images/mosip-token-token-seeder-block-diagram.png)

## API

Ref [API](mts-api.md)

## Source code

Ref [GitHub](https://github.com/mosip/openg2p/tree/develop)

## User stories

Ref [Jira](https://mosip.atlassian.net/browse/MOSIP-23029)
