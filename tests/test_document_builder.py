#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from tests.base import TestCase
from json_formatting import JsonReader
from general_formatting import Collection
from general_formatting import Document
from general_formatting import document_builder
from json_formatting import ensure_quotes

class JsonFormatterTestCase(TestCase):
    def test_should_create_new_collection(self):
        reader = JsonReader('[]')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Collection)

    def test_should_create_new_collection_with_numbers(self):
        reader = JsonReader('[1,2.,-.3]')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Collection)
        expect(len(doc.children)).to_equal(3)

        val = doc.children[0]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('1')
        expect(val.value_type).to_equal('number')

        val = doc.children[1]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('2.')
        expect(val.value_type).to_equal('unknown')

        val = doc.children[2]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('-.3')
        expect(val.value_type).to_equal('number')

    def test_should_create_new_collection_with_objects(self):
        reader = JsonReader('[{}, {a:2}]')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Collection)
        expect(len(doc.children)).to_equal(2)

        val = doc.children[0]
        expect(val).not_to_be_null()
        expect(val.value_type).to_equal('object')

        obj = doc.children[1].value
        expect(obj).not_to_be_null()

        prop = obj.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('2')

    def test_should_create_new_collection_with_comment(self):
        reader = JsonReader('[// new comment here\n0.1,2]')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Collection)
        expect(len(doc.children)).to_equal(3)

        comm = doc.children[0]
        expect(comm).not_to_be_null()
        expect(comm.value).to_equal('new comment here')
        expect(comm.comment_type).to_equal('line')

        val = doc.children[1]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('0.1')
        expect(val.value_type).to_equal('number')

        val = doc.children[2]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('2')

    def test_should_create_new_collection_with_numbers_and_comment(self):
        reader = JsonReader('[1,2//this is number 2\n,3]')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Collection)
        expect(len(doc.children)).to_equal(3)

        val = doc.children[0]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('1')
        expect(val.value_type).to_equal('number')

        val = doc.children[1]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('2')

        comm = val.comments[0]
        expect(comm).not_to_be_null()
        expect(comm.value).to_equal('this is number 2')
        expect(comm.comment_type).to_equal('line')

        val = doc.children[2]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('3')

    def test_should_create_new_document(self):
        reader = JsonReader('{ }')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)

    def test_should_create_document_with_property(self):
        reader = JsonReader('{ab: 123}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('ab')
        expect(prop.value.value).to_equal('123')
        expect(prop.value.value_type).to_equal('number')

    def test_should_create_document_with_string_property(self):
        reader = JsonReader('{"a": "4"}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('4')
        expect(prop.value.value_type).to_equal('string')

    def test_should_create_document_with_multiple_properties(self):
        reader = JsonReader('{"a": "6", b:c}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(2)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('6')
        expect(prop.value.value_type).to_equal('string')

        prop = doc.children[1]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('b')
        expect(prop.value.value).to_equal('c')
        expect(prop.value.value_type).to_equal('unknown')

    def test_should_create_document_with_array_property(self):
        reader = JsonReader('{"arr": [1,2,3]}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('arr')
        expect(prop.value.value_type).to_equal('array')

        val = prop.value.value.children[0]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('1')

        val = prop.value.value.children[1]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('2')

        val = prop.value.value.children[2]
        expect(val).not_to_be_null()
        expect(val.value).to_equal('3')

    def test_should_create_document_with_child_object_property(self):
        reader = JsonReader('{"obj": {a:false}}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('obj')
        expect(prop.value.value_type).to_equal('object')

        obj = prop.value.value
        expect(obj).not_to_be_null()

        prop = obj.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('false')
        expect(prop.value.value_type).to_equal('boolean')

    def test_should_create_document_with_block_comment(self):
        reader = JsonReader('{/* block comment */ a: true}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(2)

        comm = doc.children[0]
        expect(comm).not_to_be_null()
        expect(comm.comment_type).to_equal('block')
        expect(comm.value).to_equal('block comment')

        prop = doc.children[1]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('true')
        expect(prop.value.value_type).to_equal('boolean')

    def test_should_create_document_with_line_comment(self):
        reader = JsonReader('{// line comment\na: true}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(2)

        comm = doc.children[0]
        expect(comm).not_to_be_null()
        expect(comm.comment_type).to_equal('line')
        expect(comm.value).to_equal('line comment')

        prop = doc.children[1]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('true')
        expect(prop.value.value_type).to_equal('boolean')

    def test_should_create_document_with_property_value_block_comment(self):
        reader = JsonReader('{a: true /* block\ncomment */}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('true')
        expect(prop.value.value_type).to_equal('boolean')

        comm = prop.value.comments[0]
        expect(comm).not_to_be_null()
        expect(comm.comment_type).to_equal('block')
        expect(comm.value).to_equal('block\ncomment')

    def test_should_create_document_with_property_value_line_comment(self):
        reader = JsonReader('{a: true // line comment\n}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('true')
        expect(prop.value.value_type).to_equal('boolean')

        comm = prop.value.comments[0]
        expect(comm).not_to_be_null()
        expect(comm.comment_type).to_equal('line')
        expect(comm.value).to_equal('line comment')

    def test_should_create_document_with_property_value_block_comment(self):
        reader = JsonReader('{a:/* block\ncomment */5.5}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('5.5')
        expect(prop.value.value_type).to_equal('number')

        comm = prop.name.comments[0]
        expect(comm).not_to_be_null()
        expect(comm.comment_type).to_equal('block')
        expect(comm.value).to_equal('block\ncomment')

    def test_should_create_document_with_property_value_line_comment(self):
        reader = JsonReader('{a:// line comment\n-74.0}')
        doc = document_builder.build(reader)

        expect(doc).not_to_be_null()
        expect(doc).to_be_instance_of(Document)
        expect(len(doc.children)).to_equal(1)

        prop = doc.children[0]
        expect(prop).not_to_be_null()
        expect(prop.name.value).to_equal('a')
        expect(prop.value.value).to_equal('-74.0')
        expect(prop.value.value_type).to_equal('number')

        comm = prop.name.comments[0]
        expect(comm).not_to_be_null()
        expect(comm.comment_type).to_equal('line')
        expect(comm.value).to_equal('line comment')
