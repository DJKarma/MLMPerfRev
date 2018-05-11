# -*- coding: utf-8 -*-

UBL_TEMPLATE = '''<?xml version="1.0" encoding="utf-8"?>
<Invoice xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:un:unece:uncefact:documentation:2" xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
  <cbc:ProfileID>NL</cbc:ProfileID>
  <cbc:ID>{ID}</cbc:ID>
  <cbc:IssueDate>{IssueDate}</cbc:IssueDate>
  <cbc:Note></cbc:Note>
  <cbc:TaxCurrencyCode />
  <cac:ReceiptDocumentReference>
    <cbc:ID></cbc:ID>
    <cbc:DocumentType></cbc:DocumentType>
  </cac:ReceiptDocumentReference>
  <cac:AccountingSupplierParty>
    <cac:Party>
      <cbc:WebsiteURI>{WEBSITE_URI}</cbc:WebsiteURI>
      <cac:PartyIdentification>
        <cbc:ID schemeAgencyID="nl" schemeAgencyName="KvK">{KVK}</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyIdentification>
        <cbc:ID schemeAgencyID="nl" schemeAgencyName="BTW">{BTW}</cbc:ID>
      </cac:PartyIdentification>
      <cac:PartyName>
        <cbc:Name>{SUPPLIER_NAME}</cbc:Name>
      </cac:PartyName>
      <cac:PhysicalLocation>
        <cac:Address>
          <cbc:StreetName>{STREET_NAME}</cbc:StreetName>
          <cbc:CityName>{CITY_NAME}</cbc:CityName>
          <cbc:PostalZone>{POSTAL_ZONE}</cbc:PostalZone>
          <cac:AddressLine>
            <cbc:Line>{SUPPLIER_ADDRESS}</cbc:Line>
          </cac:AddressLine>
        </cac:Address>
      </cac:PhysicalLocation>
      <cac:PartyTaxScheme>
        <cbc:CompanyID>{BTW}</cbc:CompanyID>
        <cac:TaxScheme>
          <cbc:ID schemeAgencyName="" />
        </cac:TaxScheme>
      </cac:PartyTaxScheme>
      <cac:Contact>
        <cbc:Telephone>{TELE_PHONE}</cbc:Telephone>
        <cbc:Telefax>{TELE_FAX}</cbc:Telefax>
        <cbc:ElectronicMail>{ELECTRONIC_MAIL}</cbc:ElectronicMail>
      </cac:Contact>
    </cac:Party>
  </cac:AccountingSupplierParty>
  <cac:AccountingCustomerParty>
    <cac:Party>
      <cac:PartyName>
        <cbc:Name>{CUSTOMER_NAME}</cbc:Name>
      </cac:PartyName>
      <cac:PhysicalLocation>
        <cac:Address>
          <cbc:StreetName>{RECEIVER_STREET_NAME}</cbc:StreetName>
          <cbc:CityName>{RECEIVER_CITY_NAME}</cbc:CityName>
          <cbc:PostalZone>{RECEIVER_POSTAL_ZONE}</cbc:PostalZone>
          <cac:AddressLine>
            <cbc:Line>{RECEIVER_ADDRESS}</cbc:Line>
          </cac:AddressLine>
        </cac:Address>
      </cac:PhysicalLocation>
      <cac:Contact />
    </cac:Party>
  </cac:AccountingCustomerParty>
  <cac:PaymentMeans>
    <cbc:PaymentMeansCode />
    <cac:PayeeFinancialAccount>
      <cbc:ID>{IBAN}</cbc:ID>
      <cac:FinancialInstitutionBranch>
        <cac:FinancialInstitution>
          <cbc:ID>{BIC}</cbc:ID>
        </cac:FinancialInstitution>
      </cac:FinancialInstitutionBranch>
    </cac:PayeeFinancialAccount>
  </cac:PaymentMeans>
  <cac:PaymentTerms>
    <cbc:ID>0</cbc:ID>
    <cac:ValidityPeriod>
      <cbc:StartDate>{IssueDate}</cbc:StartDate>
      <cbc:EndDate>{EndDate}</cbc:EndDate>
    </cac:ValidityPeriod>
  </cac:PaymentTerms>
  <cac:TaxTotal>
    <cbc:TaxAmount currencyID="EUR">{TAX_AMOUNT}</cbc:TaxAmount>
  </cac:TaxTotal>
  <cac:LegalMonetaryTotal>
    <cbc:TaxExclusiveAmount currencyID="EUR">{TAX_EXCLUSIVE_AMOUNT}</cbc:TaxExclusiveAmount>
    <cbc:PayableAmount currencyID="EUR">{PAYABLE_AMOUNT}</cbc:PayableAmount>
  </cac:LegalMonetaryTotal>
  {UBL_INVOICE_LIST}
</Invoice>
'''

INVOICE_LINE_TEMPLATE = '''
  <cac:InvoiceLine>
    <cbc:ID>{INVOICE_ID}</cbc:ID>
    <cbc:InvoicedQuantity>{InvoicedQuantity}</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="EUR">{LineExtensionAmount}</cbc:LineExtensionAmount>
    <cac:TaxTotal>
      <cbc:TaxAmount currencyID="EUR">{TaxAmount}</cbc:TaxAmount>
      <cac:TaxSubtotal>
        <cbc:TaxableAmount currencyID="EUR">{TaxableAmount}</cbc:TaxableAmount>
        <cbc:TaxAmount currencyID="EUR">{TaxSubtotalAmount}</cbc:TaxAmount>
        <cbc:Percent>{Percent}</cbc:Percent>
        <cac:TaxCategory>
          <cac:TaxScheme>
            <cbc:Name />
          </cac:TaxScheme>
        </cac:TaxCategory>
      </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:SubInvoiceLine>
        <cbc:ID>{SUB_INVOICE_LINE_ID}</cbc:ID>
        <cac:PricingReference>
           <cac:OriginalItemLocationQuantity>
             <cac:Price>
               <cbc:PriceAmount currencyID="EUR">{PACKAGING_PRICE}</cbc:PriceAmount>
             </cac:Price>
             <cac:Package>
               <cbc:Quantity></cbc:Quantity>
               <cbc:PackagingTypeCode></cbc:PackagingTypeCode>
             </cac:Package>
           </cac:OriginalItemLocationQuantity>
        </cac:PricingReference>
    </cac:SubInvoiceLine>
    <cac:Item>
        <cbc:Name>{ItemName}</cbc:Name>
    </cac:Item>
  </cac:InvoiceLine>
'''
