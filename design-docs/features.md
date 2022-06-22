# Features

## Overview

The notes here capture the discussions around vision and roadmap for OpenG2P-NG. This is **work-in-progress**.

## Discussion

* Help showcase how ID can be used effectively
* Demonstrate:
  * MEC environment
  * Field deployment - Afghanistan or Ukraine (UNDP)
  * Philippines DSWD
    * Social Protection (equivalent of Social Security - food coupons, unemployment benefits, etc)
    * Other benefits or contexts
  * Other areas where IDs are involved
    * Onboarding new beneficiaries
    * Token seeding for existing registries
    * Proof of receipt - voucher
    * Proof of delivery - ?
* How do we on board a new beneficiary?
  * Who has a national ID
  * Who does not have a national ID
* Person who has is a beneficiary how do we link them to the national ID?
  * Deduplication
  * Removal of ghost beneficiaries
  * Identifying potential beneficiaries for a new program or scheme (ability to filter)
  * Seamless delivery
    * Self service
    * Assisted mode
* List of beneficiaries who are already there. How to choose them for a new program?
* Proof of receipt or delivery
* Monetary Benefits
  * Banked
    * Direct beneficiary transfer (DBT)
    * Monetary benefit - transferred to a bank account or wallet or pre-paid card (option to store some money which can be withdrawn and spent by the benifitiary)
    * Disbursement list
    * Registry of Person and Bank Accounts
      * Collect during onboarding of beneficiary (default preference)
      * Scheme provides the account details
      * GovStack - Person’s preference - Maintain the person to account map
      * Social Protection account (Ukraine)
  * Unbanked
    * Take money from an intermediary agent (kiosk, village officer, third party shop keeper)
    * Cash or Voucher/Coupon - Physical or Digital
    * Voucher - that can be used to collect the money
    * Agency Model
      * Agent is online - they can perform verification and record the transaction
      * Agent is offline
        * Problems:
          * Multiple claims are made
          * Amount is not shared with the resident
          * Whole amount might not be shared with the resident
        * Solutions:
          * OTP or Delivery PIN (provided the beneficiary has a phone and the contact details are listed and they have received the PIN)
          * Voucher acting as a PIN
            * Do we need vouchers? - Physical evidence to receive the money
            * Can we think of an alternate mechanism rather than voucher?
            * A officer is going to distribute a voucher and then an officer is verifying the voucher?
          * Presence verification by taking a Photograph (together mode | timestamped and attested photograph)
          * Resident is informed how much amount he or she should be receiving
* Non Monetary Benefits
  * Types
    * Health
      * Vaccination
      * Life Insurance
      * Medical Care
    * Agriculture
      * Fertilisers
      * Crops/Seeds
      * Agricultural Equipments, etc.
      * Free electricity for pumping water
    * Social Protection Department
      * Ration
      * Education
      * Construction of Houses/Toilets
      * LPG gas
      * Employment Programs
    * Subsidised Products (Eligibility Check)
      * Cashback
      * During delivery the cost is reduced
      * Money is provided to buy goods\*\*  
* Getting the List of eligible beneficiaries (beneficiary identification)
  * Surveys
  * Analysis of the data
  * Slice and dice the data (filter)
  * Applying and Sign up
