#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

import os
from indent_x.test_util import fs_test
from indent_x.tests.base import TestCase
from indent_x.general_formatting.general_formatter import GeneralFormatter

class GeneralFormatterTestCases(TestCase):
    def test_should_identify_and_format_basic_xml(self):
        formatter = GeneralFormatter()
        formattedText = formatter.format('<root><child></child></root>', '\t')
        expect(formattedText).to_equal('<root>\n\t<child></child>\n</root>')

    def test_should_identify_and_format_basic_json(self):
        formatter = GeneralFormatter()
        formattedText = formatter.format('{"hello":"world" ,"value":123}', '\t')
        expect(formattedText).to_equal('{\n\t"hello": "world",\n\t"value": 123\n}')

    def test_should_identify_and_format_basic_json_with_leading_spaces(self):
        formatter = GeneralFormatter()
        formattedText = formatter.format('  {"hello":"world" ,"value":123}', '\t')
        expect(formattedText).to_equal('{\n\t"hello": "world",\n\t"value": 123\n}')

    def test_should_not_format_null_input(self):
        formatter = GeneralFormatter()
        formattedText = formatter.format(None, '\t')
        expect(formattedText).to_equal(None)

    def test_should_not_format_whitespace(self):
        formatter = GeneralFormatter()
        formattedText = formatter.format(' ', '\t')
        expect(formattedText).to_equal(None)

    def test_should_identify_and_unindent_basic_xml(self):
        formatter = GeneralFormatter()
        formattedText = formatter.unindent('<root>\n\t<child\na="123"></child>\n</root>')
        expect(formattedText).to_equal('<root><child a="123"></child></root>')

    def test_should_identify_and_unindent_basic_json(self):
        formatter = GeneralFormatter()
        formattedText = formatter.unindent('{\n\t"hello": "world",\n\t"value": 123\n}')
        expect(formattedText).to_equal('{"hello":"world","value":123}')

def result_resolver(input):
    formatter = GeneralFormatter()
    return formatter.format(input, '\t')

fs_test.load_testcases(
    GeneralFormatterTestCases,
    result_resolver,
    os.path.dirname(__file__),
    'data/indent/*.input.xml',
    'expected.xml')
