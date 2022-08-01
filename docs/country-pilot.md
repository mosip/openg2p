---
description: (Draft)
---

# Country Pilot

## Overview

This section enlists the recommendations identified so far, wrt OpenG2P pilot for Countries.\
This is an evolving section with ongoing updates.

1. **Offline - ODK based**
   1. Overall recommendation is to adopt the offline mode of authentication with ODK based application, which enables quick data capture, onboarding and offline authentication
   2. Recommend not to have web based or client based auth application, as it brings in lots of dependencies wrt having a separate QR code scanner plugged in, dependency on internet connectivity etc.
   3. **Biometric data capture** to be de-prioritized as it brings in more complexity and infrastructure dependency on device(s)\
      PH requirement: For the pilot, fingerprint scanners will be deployed to pilot areas.
   4. TBD - Since there is no login by Operator and no session maintained during beneficiary onboarding, it is recommended to carry out Operator authentication for every form filled, to ensure authenticity of the data captured
   5. TBD - During beneficiary onboarding, beneficiary data scanned via QR code should be non-editable to avoid data tampering by Operator
   6. TBD **- Consent** in ODK form > Will this be a **checkbox** or **upload of form signed by Resident** or Mobile based Consent via consent token/framework?
   7. TBD - To ensure existing beneficiary data is reflected on the form at the time of data capture, Beneficiary ID of existing beneficiaries will be required. Do we have the Beneficiary ID available?
   8. TBD - III.2.2.2.11 - What's the difference between Client and Beneficiary?
2. **Reporting**:
   1. To enable reporting with Operator related KPIs, it is recommended to scan officer's QR code --**OR**-- Since ODK Collect app captures user data, that mapping (of user data to the forms) can be leveraged for Reporting. Assumption here will be that one tab will be assigned to one agent and Country maintains this at field level
   2. Further, it is recommended to use **Metabase** that uses **Odata** protocol for querying and viewing Reports
   3. Report wrt Counts of failed registration > This can be derived from the output of token seeder
   4. Other reports can be generated from data stored in **Authentication Result Data Repository (Odoo module)**
   5. TBD - II.5.2
   6. UBD - Need clarity
   7. **Pre-requisites**: **IAM (Odoo module), Reporting** tool/**system, Master data setup** to pre-exist, maybe via Odoo
3. **Scope of pilot**:
   1.  **TBD** - Offline authentication using ODK - Click [here](https://mosip.atlassian.net/browse/MOSIP-21658) for details

       \
       \


       \
       \
