import locale

import mapping
from epdfApi.epdf.models import PatternDimensions
from vendor.identifier import VendorIdentifier
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

locale.setlocale(locale.LC_NUMERIC, "nl_NL.utf8")


class PdfPattern(object):
    # def __init__(self, file_name, file_path, vendor_name, pdf_page_count):
    def __init__(self, pdf_file_name, pdf_file_path, pdf_text, vendor_name):
        self.pdf_fileName = pdf_file_name
        self.pdf_filePath = pdf_file_path
        self.pdf_text = pdf_text
        self.vendor_name = vendor_name
        self.snippet_line_list = []
        self.snippet_word_list = []
        self.MFSnippetList = []
        self.dimension_name_list = ['a_position', 'b_position', 'prefix1', 'prefix2', 'prefix3', 'topfix1', 'topfix2',
                                    'topfix3']
        self.missing_field_list = ['VendorKvKNumber', 'VendorVATNumber', 'VendorIBANNumber', 'VendorBICNumber',
                                   'VendorBankACNumber', 'CustomerCountry', 'InvoiceDate', 'InvoiceNumber']

    def apply_pattern(self):
        # TODO not saving new PDF info without xml, could be changed later
        # step 1: get snippets of both types from the PDF without calling the dimension matching part
        self.snippet_line_list = self.create_snippets_line_mode()
        self.snippet_word_list = self.create_snippets_word_mode()
        self.apply_pattern_snippets('word')
        self.apply_pattern_snippets('line')
        return self.MFSnippetList

    def apply_pattern_snippets(self, snippet_type):
        # step 2: get the pattern of all MFs for that

        # PatternDimensions.objects.filter(vendor_name=self.vendor_name, snippet_type='line')
        # pattern_instance_list = PatternDimensions.objects.filter(vendor_name=self.vendor_name, snippet_type='word')

        # self.snippet_word_list

        for missing_field in self.missing_field_list:
            pattern_instance_instance_list = PatternDimensions.objects.filter(vendor_name=self.vendor_name, snippet_type=snippet_type,
                                                                              field_name=missing_field).values()
            if pattern_instance_instance_list:
                pattern_instance_instance = pattern_instance_instance_list[0]
            else:
                continue

            # Now based on dimension_name and dimension_value search in current snippet list
            snippet_list = []

            if snippet_type == 'line':
                snippet_list = self.snippet_line_list

            if snippet_type == 'word':
                snippet_list = self.snippet_word_list

            for snippet_instance in snippet_list:
                dimension_name = pattern_instance_instance['dimension_name']
                dimension_value = pattern_instance_instance['dimension_value']

                not_already_exist = not any(d.get('field_name', None) == missing_field for d in self.MFSnippetList)

                if snippet_instance[dimension_name] == dimension_value and not_already_exist:
                    result = {'vendor_name': self.vendor_name, 'field_name': missing_field,
                              'snippet_type': snippet_type}
                    result.update(snippet_instance)
                    self.MFSnippetList.append(result)
                    continue

        return self.MFSnippetList

    # TODO below 2 methods are almost the same copy from class pdfLearning.py without MFs part. Make it DRY later
    def create_snippets_line_mode(self):
        total_lines = sum(1 for line in self.pdf_text.splitlines())

        line_index = 0
        snippet_line_list = []
        topfix1 = ''
        topfix2 = ''
        topfix3 = ''

        for line in self.pdf_text.splitlines():
            # print '##line:', line
            line_index += 1
            b_position = total_lines - line_index   # max - A + 1 TODO: recheck if +1 is required here
            # TODO: dynamic vendor_pdf_id
            result = {'vendor_name': self.vendor_name, 'field_value': line,
                      'a_position': line_index, 'b_position': b_position, 'topfix1': topfix1, 'topfix2': topfix2,
                      'topfix3': topfix3}
            topfix3 = topfix2
            topfix2 = topfix1
            topfix1 = line
            snippet_line_list.append(result)
            # snippet_line_list.append(SnippetsLine(**result))

        # SnippetsLine.objects.bulk_create(snippet_line_list)
        return snippet_line_list

    def create_snippets_word_mode(self):
        total_words = sum(1 for word in self.pdf_text.split())

        line_index = 0
        snippet_word_list = []
        prefix1 = ''
        prefix2 = ''
        prefix3 = ''

        for word in self.pdf_text.split():
            # print '##line:', line
            line_index += 1
            b_position = total_words - line_index   # max - A + 1 TODO: recheck if +1 is required here
            # TODO: dynamic vendor_pdf_id
            result = {'vendor_name': self.vendor_name, 'field_value': word,
                      'a_position': line_index, 'b_position': b_position, 'prefix1': prefix1, 'prefix2': prefix2,
                      'prefix3': prefix3}
            prefix3 = prefix2
            prefix2 = prefix1
            prefix1 = word
            snippet_word_list.append(result)
            # snippet_word_list.append(SnippetsWord(**result))

        # SnippetsWord.objects.bulk_create(snippet_word_list)
        return snippet_word_list


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
            pdfLearner = PdfPattern(fileName, filePath, vendor_name_identified, pdfPageCount)
            pdfLearner.create_xml()
        pdfCount = pdfCount + 1
