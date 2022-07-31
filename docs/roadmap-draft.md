---
description: (Draft)
---

# Roadmap

## Overview

This is **draft** roadmap of OpenG2P from MOSIP point of view.

## Roadmap

![](https://raw.githubusercontent.com/mosip/openg2p/main/docs/\_images/openg2p\_roadmap.png)

****

* **Phase 1 - Last mile + Country requirements**
  * Verification of Beneficiary
    * Authentication at the point of delivery
    * QR code scanning
    * Mobile ID sharing
    * Identity linking via Tokenization using [MOSIP Token Seeder](mosip-token-seeder/)
  * Proof of Delivery
    * Non-digital/Physical: Joint selfie
    * Digital: Transaction ID/rails
  * PH Pilot
    * Beneficiary onboarding: QR code, Mobile ID sharing
    * Deduplication of registries - demographic and/or biometrics using an ABIS middleware and leveraging [MOSIP Token Seeder](mosip-token-seeder/)
    * Support to go live with IDA
    * Authentication at point of delivery
    * ID Provider (IDP) interface for Self Service Portal (SSP)
* **Phase 2 - Supplementary requirements**
  * Eligibility Management
    * Anonymous eligibility check (engine)
    * Query system on eligibility of potential beneficiaries for new scheme(s)
  * Others
    * Reporting
    * Consent framework
    * Disbursement: Payments integration, E-Voucher
* **Phase 3 - Supplementary low PRI requirements**
  * Datashare and Event Publishing
    * [Beckn protocol](https://becknprotocol.io/) can be used to share data
  * Token Translation
  * Others
    * Communication: Informative SMS/Email - To potential beneficiaries on eligibility for new scheme(s)
    * OpenID for login (OIDC)
    * Enhanced privacy and security



