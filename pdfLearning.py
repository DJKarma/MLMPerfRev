import locale

import mapping
from epdfApi.epdf.models import MissingFieldDimensions, PatternDimensions, SnippetsLine, SnippetsWord
from vendor.identifier import VendorIdentifier
from xml.dom import minidom
import re

import Levenshtein
import sys
from django.forms.models import model_to_dict
import operator

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

locale.setlocale(locale.LC_NUMERIC, "nl_NL.utf8")


class PdfLearning(object):
    # def __init__(self, file_name, file_path, vendor_name, pdf_page_count):
    def __init__(self, pdf_file_name, pdf_file_path, xml_file_name, xml_file_path, pdf_text, vendor_name):
        self.pdf_fileName = pdf_file_name
        self.pdf_filePath = pdf_file_path
        self.xml_file_name = xml_file_name
        self.xml_file_path = xml_file_path
        self.pdf_text = pdf_text
        self.vendor_name = vendor_name
        self.MFSnippetList = []
        self.dimension_name_list = ['a_position', 'b_position', 'prefix1', 'prefix2', 'prefix3', 'topfix1', 'topfix2',
                                    'topfix3']
        self.missing_field_list = ['VendorKvKNumber', 'VendorVATNumber', 'VendorIBANNumber', 'VendorBICNumber',
                                   'VendorBankACNumber', 'CustomerCountry', 'InvoiceDate', 'InvoiceNumber']

    def learn_from_xml(self):
        xml_info = self.get_xml_info()

        latest_vendor_instance = MissingFieldDimensions.objects.filter(vendor_name=self.vendor_name).last()
        vendor_pdf_id = 1

        if latest_vendor_instance:
            latest_vendor_instance_dict = model_to_dict(latest_vendor_instance, fields=[field.name for field in latest_vendor_instance._meta.fields])
            vendor_pdf_id = latest_vendor_instance_dict["vendor_pdf_id"] + 1

        self.create_snippets_line_mode(vendor_pdf_id, xml_info)
        self.create_snippets_word_mode(vendor_pdf_id, xml_info)
        print "##done"
        return ''

    def create_snippets_line_mode(self, vendor_pdf_id, xml_info):
        total_lines = sum(1 for line in self.pdf_text.splitlines())

        line_index = 0
        snippet_line_list = []
        missing_field_dimension_list = []
        missing_field_dimension_db_list = []
        topfix1 = ''
        topfix2 = ''
        topfix3 = ''

        for line in self.pdf_text.splitlines():
            # print '##line:', line
            line_index += 1
            b_position = total_lines - line_index   # max - A + 1 TODO: recheck if +1 is required here
            # TODO: dynamic vendor_pdf_id
            result = {'vendor_name': self.vendor_name, 'vendor_pdf_id': vendor_pdf_id, 'field_value': line,
                      'a_position': line_index, 'b_position': b_position, 'topfix1': topfix1, 'topfix2': topfix2,
                      'topfix3': topfix3}
            topfix3 = topfix2
            topfix2 = topfix1
            topfix1 = line
            snippet_line_list.append(SnippetsLine(**result))

            # TODO run only during learning ie when xml is uploaded along with PDF
            missing_field_result = self.xml_dimension_matching(xml_info, result, 'line')
            if missing_field_result:
                missing_field_dimension_list.append(missing_field_result)

        SnippetsLine.objects.bulk_create(snippet_line_list)

        missing_field_dimension_list = list({v['field_name']: v for v in missing_field_dimension_list}.values())
        for missing_field_dimension in missing_field_dimension_list:
            missing_field_dimension_db_list.append(MissingFieldDimensions(**missing_field_dimension))

        MissingFieldDimensions.objects.bulk_create(missing_field_dimension_db_list)

    def create_snippets_word_mode(self, vendor_pdf_id, xml_info):
        total_words = sum(1 for word in self.pdf_text.split())

        line_index = 0
        snippet_word_list = []
        missing_field_dimension_list = []
        missing_field_dimension_db_list = []
        prefix1 = ''
        prefix2 = ''
        prefix3 = ''

        for word in self.pdf_text.split():
            # print '##line:', line
            line_index += 1
            b_position = total_words - line_index   # max - A + 1 TODO: recheck if +1 is required here
            # TODO: dynamic vendor_pdf_id
            result = {'vendor_name': self.vendor_name, 'vendor_pdf_id': vendor_pdf_id, 'field_value': word,
                      'a_position': line_index, 'b_position': b_position, 'prefix1': prefix1, 'prefix2': prefix2,
                      'prefix3': prefix3}
            prefix3 = prefix2
            prefix2 = prefix1
            prefix1 = word
            snippet_word_list.append(SnippetsWord(**result))

            # TODO run only during learning ie when xml is uploaded along with PDF
            missing_field_result = self.xml_dimension_matching(xml_info, result, 'word')
            if missing_field_result:
                missing_field_dimension_list.append(missing_field_result)

        SnippetsWord.objects.bulk_create(snippet_word_list)

        missing_field_dimension_list = list({v['field_name']: v for v in missing_field_dimension_list}.values())
        for missing_field_dimension in missing_field_dimension_list:
            missing_field_dimension_db_list.append(MissingFieldDimensions(**missing_field_dimension))

        MissingFieldDimensions.objects.bulk_create(missing_field_dimension_db_list)

    @staticmethod
    def xml_dimension_matching(xml_info, pdf_data_instance, snippet_type):
        # Get A position from of PDF text by comparing it with actual value
        pdf_data = pdf_data_instance.copy()

        for key, value in xml_info.iteritems():
            if snippet_type == 'line' and value == pdf_data['field_value']:
                result = {'field_name': key, 'field_value': value, 'snippet_type': snippet_type}
                result.update(pdf_data)
                return result
            elif snippet_type == 'word' and value in pdf_data['field_value']:
                result = {'field_name': key, 'field_value': value, 'snippet_type': snippet_type}
                result.update(pdf_data)
                return result

        # TODO check previous results of vendor_pdf_id and add missing_field_dimension, missing_field_dimension_value
        return

    def get_xml_info(self):
        xmldoc = minidom.parse(self.xml_file_path)

        # amount, date, invoice_number, TELE_PHONE, TELE_FAX, WEBSITE_URI, ACCOUNT_NUMBER, EMAIL, IBAN, BIC, BTW, KVK

        VendorName = self.get_xml_field(xmldoc, '_VendorName')
        VendorKvKNumber = self.get_xml_field(xmldoc, '_VendorKvKNumber')
        VendorVATNumber = self.get_xml_field(xmldoc, '_VendorVATNumber')
        VendorIBANNumber = self.get_xml_field(xmldoc, '_VendorIBANNumber')
        VendorBICNumber = self.get_xml_field(xmldoc, '_VendorBICNumber')
        VendorBankACNumber = self.get_xml_field(xmldoc, '_VendorBankACNumber')
        VendorAddress = self.get_xml_field(xmldoc, '_VendorAddress')
        VendorCountry = self.get_xml_field(xmldoc, '_VendorCountry')
        CustomerName = self.get_xml_field(xmldoc, '_CustomerName')
        # CustomerAddress = self.get_xml_field(xmldoc, '_CustomerAddress')
        CustomerCountry = self.get_xml_field(xmldoc, '_CustomerCountry')
        # Currency = self.get_xml_field(xmldoc, '_Currency')
        InvoiceDate = self.get_xml_field(xmldoc, '_InvoiceDate')
        InvoiceNumber = self.get_xml_field(xmldoc, '_InvoiceNumber')

        result = {'VendorName': VendorName, 'VendorKvKNumber': VendorKvKNumber, 'VendorVATNumber': VendorVATNumber,
                  'VendorIBANNumber': VendorIBANNumber, 'VendorBICNumber': VendorBICNumber,
                  'VendorBankACNumber': VendorBankACNumber,
                  'CustomerCountry': CustomerCountry, 'InvoiceDate': InvoiceDate, 'InvoiceNumber': InvoiceNumber}

        return result

    def get_xml_field(self, xmldoc, field_name):
        xml_elements = xmldoc.getElementsByTagName(field_name)
        field_value = xml_elements[0].childNodes[0]
        # print('#field_name nodeValue', field_value.nodeValue)
        result = field_value.nodeValue
        result = result.encode('ascii', 'ignore')      # convert unicode to simple string required for below method call
        self.get_position_dimension(field_name, result)
        return result

    # Get A position from of PDF text by comparing it with actual value
    def get_position_dimension(self, field_name, field_output_value):
        result = {"field_name": field_name[1:], "field_value": field_output_value,
                  "A": -1, "B": -1, "AX": -1, "BX": -1, "prefix": '', "topfix": '', "classification": ''}
        # print "##field_output_value", field_output_value
        line_index = 0
        topfix = ''

        for line in self.pdf_text.splitlines():
            # print '##line:', line
            line_index += 1
            word_index = 0
            line_spaceless = "".join(line.split())
            # print "##line", line
            # print "##line_spaceless", line_spaceless
            if field_output_value in line:
                result["A"] = line_index
                prefix = ''
                result["topfix"] = topfix
                topfix = line
                result["classification"] = PdfLearning.classify_field_using_regex(line)
            elif field_output_value in line_spaceless:
                result["A"] = line_index
                prefix = ''
                result["topfix"] = topfix
                topfix = line
                result["classification"] = PdfLearning.classify_field_using_regex(line)

            for word in line.split():
                word_index += 1
                # TODO: Levenshtein could also for fallback approach if line_index is not found (no exact match)
                if Levenshtein.ratio(field_output_value, word) > 0.5:
                    # print 'Levenshtein found at line:', line_index
                    # print 'Levenshtein found at word:', word_index
                    result["AX"] = word_index
                if result["AX"] != -1:
                    result["BX"] = word_index - result["AX"]        # max - AX
                    result["prefix"] = prefix
                prefix = word
                # Get prefix

        # if none found use Levenshtein distance for words separated by spaces
        # Levenshtein.ratio('hello world', 'hello')           # 0.625
        if result["A"] != -1:
            result["B"] = line_index - result["A"]          # max - A
        # print "##result", result

        return result

    @staticmethod
    def classify_field_using_regex(line):
        # TODO: make classification work for all fields, probably need to change regex pattern used
        kvk_pattern = re.compile('(?i)(?:kvk. *?)\s(\d{8})\s')
        kvk_pattern_found = kvk_pattern.match(line)
        # print "##kvk_pattern_found", kvk_pattern_found
        return kvk_pattern_found

    def create_update_dimensions_pattern(self, snippet_type):
        result_list = []

        # Clear all the existing Pattern for current vendor as it would be freshly generated again in below code
        PatternDimensions.objects.filter(vendor_name=self.vendor_name, snippet_type=snippet_type).delete()

        for missing_field in self.missing_field_list:
            # List of all IBAN etc with dimensions
            missing_field_instance_list = MissingFieldDimensions.objects.filter(vendor_name=self.vendor_name,
                                                field_name=missing_field, snippet_type=snippet_type).values()

            common_dimension_name = 'b_position'
            for dimension_name in self.dimension_name_list:
                foo_list = map(operator.itemgetter(dimension_name), missing_field_instance_list)
                are_all_equal = foo_list and foo_list[0] is not None and foo_list[1:] == foo_list[:-1]

                if are_all_equal is True:
                    common_dimension_name = dimension_name
                    continue

            # print "##missing_field_instance_list zero", missing_field_instance_list[0]
            dimension_value = missing_field_instance_list and missing_field_instance_list[0][common_dimension_name]
            if dimension_value:
                pattern_info = {'vendor_name': self.vendor_name, 'field_name': missing_field,
                                'snippet_type': snippet_type, 'dimension_name': common_dimension_name,
                                'dimension_value': missing_field_instance_list[0][common_dimension_name]}
                result_list.append(PatternDimensions(**pattern_info))

        PatternDimensions.objects.bulk_create(result_list)
        return ''

    @staticmethod
    def xml_reader(data):
        try:
            return data
        except ValueError:
            return ""

if __name__ == '__main__':
    # fileBaseName = 'De Klok Dranken '
    fileBaseName = "sligro"
    pdfCount = 1

    while pdfCount <= 2:
        fileName = fileBaseName + str(pdfCount)
        filePath = "ePDF/" + fileName + ".pdf"
        vendor_identifier = VendorIdentifier(fileName, filePath)

        extract_vendor = vendor_identifier.extract_vendor()
        vendor_name_identified = extract_vendor['vendor_name']
        pdfPageCount = extract_vendor['pdf_page_count']

        vendor_name_identified = mapping.SLIGRO
        # vendor_name_identified = mapping.DEKLOKDRANKEN
        if vendor_name_identified == mapping.INVALID:
            print "Cannot identify vendor quitting now"
        else:
            pdfLearner = PdfLearning(fileName, filePath, vendor_name_identified, pdfPageCount)
            pdfLearner.create_xml()
        pdfCount = pdfCount + 1
