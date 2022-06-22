# Home

## Overview

Key features of openg2p-ng system:

* Centralised beneficiary registries
* Deduplicated registries
* Beneficiary enrollment
* User verification at point of delivery
* Proof of delivery
* Integration with payment rails of a country
* Voucher based delivery
* Integration with departmental applications

## High level view

![](\_images/high-level-view.png)

## Beneficiary onboarding

* Self registration
* Agent based registration - one agent registering many in a village as part of self registration
* Survey/enumerator - carrying an App with filling forms.
  * ODK App with ability to download forms of multiple scheme
  * Off line authentication capability
* "last mile scenarios"

### Registration

* Registration is data collection for a scheme.
  * Registration can happen via
  * Existing data (from other schemes, databases, departments, digitized paper copies). Consent of beneficiary is required here.
  * Self registration.
  * Assisted registration on the ground by an officer/enumerator by meeting beneficiary in person and filling a form using Brollie tablet app.
* Registration does not mean eligibility.
* Self registration could be done in the following ways:
  * Online browser
  * App
  * USSD on mobile

### Authentication with ID Systems

* [MOSIP Authentication and KYC](mosip-authentication.md)

### Manual adjudication

## The last mile challenges

* Connectivity:
  * Voice (USSD, SMS) + data (3G, 4G)
  * Voice (USSD, SMS) + 2G
  * No mobile network
* Cell phone type:
  * Basic phone (only USSD, SMS)
  * Feature phone (camera, Bluetooth, USSD, SMS)
  * Smart phone
* Cell phone ownership:
  * No phone Personal
  * Family - a single member of the family shares the phone
  * Community
* Biometric
  * Worn-out fingerprint
  * Face identification issues with older population and siblings
  * …
* Education - usage of one’s identity.

## Concept of household/group

* Household
* Group
* Relationship between two registrants

## Scheme management

### Sharing data across schemes with consent

* Mismatch of data across schemes for the same field
* Data quality indicator

## Beneficiary management

* Change request of info by residents

## Eligibility engine

## Payments

## Proof of delivery

## Tech stack

| Software | Version | Comments               |
| -------- | ------- | ---------------------- |
| Odoo     | 12      | Currently. Move to 15. |
| Postgres |         |                        |
| Redis    |         |                        |
| ODK      | 9.6     |                        |

## Source code

Github repos:

## Glossary

* Enumerator
* Supervisor
* Enumeration area
* Social worker
* Social registry
* Beneficiary registry
* Disbursement list
* Household Survey team
* Questionnaire VC - Verifiable Credentials
