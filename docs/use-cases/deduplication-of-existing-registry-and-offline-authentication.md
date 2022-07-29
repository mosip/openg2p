# Deduplication of Existing Registry & Offline Authentication

## Overview

Governments already have existing beneficiary registries that may contain duplicates or ghosts. \
A very basic requirement is to clean the registries by deduplicating their beneficiary lists, thereby avoiding double dipping. This can be enabled with **token seeding -** Wherein a unique alias token identifier referred as **** [Token ID](https://docs.mosip.io/1.2.0/id-lifecycle-management/identifiers#token-id) **** is generated and linked to the corresponding UIN for every authentication request. The [MOSIP Token Seeder ](https://docs.mosip.io/openg2p/mosip-token-seeder)(MTS) is a convenience module that supports the above requirement. Refer to [this Jira](https://mosip.atlassian.net/browse/MOSIP-21658) for possible work flows.

To enable the offline authentication flow, various entities and tools may be used for the varied operational functions. Refer below for details.

### Features and Tools:

| Block                                            | Feature                              | Tool/System                                                                                    |
| ------------------------------------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------- |
| ERP                                              | Program Management                   | <p>OpenG2P ERP System <br>EG: Odoo</p>                                                         |
|                                                  | Beneficiary Management               | <p>OpenG2P ERP System <br>EG: Odoo</p>                                                         |
|                                                  | Registration                         | <p>OpenG2P ERP System <br>EG: Odoo</p>                                                         |
|                                                  | Reporting                            | <p>OpenG2P ERP System <br>EG: Odoo</p>                                                         |
| Toolbox                                          | QR Code Scanning                     | ODK Collect with 3PT app EG: ID Pass                                                           |
|                                                  | Mobile ID Sharing                    | MOSIP Inji app with Google Nearby <_Under dev>_                                                |
| Disbursement Engine                              | Payments                             | Mifos                                                                                          |
| Deduplication Engine                             | Deduplicating registries             | <p>'- OpenG2P ERP System <br>EG: Odoo <br>- Integration with MTS &#x3C;<em>Under dev></em></p> |
| Mobile Tools                                     | Mobile Tools                         | <p>'- MOSIP Inji App<br>- ODK - Personnel login mechanism &#x3C;<em>TBD></em></p>              |
| Verification Service                             | Authentication                       | <p>'- IDA<br>- MTS &#x3C;<em>Under dev></em></p>                                               |
| E-Voucher Service                                | Voucher issuance                     | To be defined                                                                                  |
| Proof of Receipt                                 | Capture proof of delivery of benefit | <p>MOSIP - Joint selfie <br>&#x3C;<em>Under dev></em></p>                                      |
| <p>Discovery Specification/<br>Data Mediator</p> | Data storage & mediation             | To be defined                                                                                  |

### Flow Diagram:

![](https://raw.githubusercontent.com/mosip/openg2p/main/docs/\_images/openg2p\_offline\_authentication\_flow.png)
