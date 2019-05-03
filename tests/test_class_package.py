# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
#

import unittest

from tern.classes.package import Package
from test_fixtures import TestTemplate1
from test_fixtures import TestTemplate2


class TestClassPackage(unittest.TestCase):

    def setUp(self):
        self.p1 = Package('p1')
        self.p1.version = '1.0'
        self.p1.pkg_license = 'Apache 2.0'
        self.p1.copyright = 'All Rights Reserved'
        self.p1.src_url = 'github.com'

        self.p2 = Package('p2')

    def tearDown(self):
        del self.p1
        del self.p2

    def testInstance(self):
        self.assertEqual(self.p2.name, 'p2')
        self.assertFalse(self.p2.version)
        self.assertFalse(self.p2.src_url)
        self.assertFalse(self.p2.pkg_license)
        self.assertFalse(self.p2.copyright)

    def testSetters(self):
        self.assertRaises(AttributeError, setattr, self.p2, 'name', 'y')
        self.p2.version = '2.0'
        self.assertEqual(self.p2.version, '2.0')
        self.p2.pkg_license = 'Apache 2.0'
        self.assertEqual(self.p2.pkg_license, 'Apache 2.0')
        self.p2.copyright = "All Rights Reserved"
        self.assertEqual(self.p2.copyright, 'All Rights Reserved')
        self.p2.src_url = 'github.com'
        self.assertEqual(self.p2.src_url, 'github.com')

    def testGetters(self):
        self.assertEqual(self.p1.name, 'p1')
        self.assertEqual(self.p1.version, '1.0')
        self.assertEqual(self.p1.pkg_license, 'Apache 2.0')
        self.assertEqual(self.p1.copyright, 'All Rights Reserved')
        self.assertEqual(self.p1.src_url, 'github.com')

    def testToDict(self):
        a_dict = self.p1.to_dict()
        self.assertEqual(a_dict['name'], 'p1')
        self.assertEqual(a_dict['version'], '1.0')
        self.assertEqual(a_dict['pkg_license'], 'Apache 2.0')
        self.assertEqual(a_dict['copyright'], 'All Rights Reserved')
        self.assertEqual(a_dict['src_url'], 'github.com')
        self.assertFalse(a_dict['origins'])

    def testToDictTemplate(self):
        template1 = TestTemplate1()
        template2 = TestTemplate2()
        dict1 = self.p1.to_dict(template1)
        dict2 = self.p1.to_dict(template2)
        self.assertEqual(len(dict1.keys()), 3)
        self.assertEqual(dict1['package.name'], 'p1')
        self.assertEqual(dict1['package.version'], '1.0')
        self.assertEqual(dict1['package.license'], 'Apache 2.0')
        self.assertEqual(len(dict2.keys()), 5)
        self.assertFalse(dict2['notes'])

    def testIsEqual(self):
        p = Package('p2')
        p.pkg_license = 'Testpkg_license'
        p.version = '1.0'
        p.src_url = 'TestUrl'
        self.p2.pkg_license = 'Testpkg_license'
        self.p2.version = '2.0'
        self.p2.src_url = 'TestUrl'
        self.assertFalse(self.p2.is_equal(p))
        p.version = '2.0'
        self.assertTrue(self.p2.is_equal(p))

    def testFill(self):
        p_dict = {'name': 'p1',
                  'version': '1.0',
                  'pkg_license': 'Apache 2.0'}
        p = Package('p1')
        p.fill(p_dict)
        self.assertEqual(p.name, 'p1')
        self.assertEqual(p.version, '1.0')
        self.assertEqual(p.pkg_license, 'Apache 2.0')
        self.assertFalse(p.copyright)
        self.assertFalse(p.src_url)
        self.assertEqual(len(p.origins.origins), 1)
        self.assertEqual(p.origins.origins[0].origin_str, 'p1')
        self.assertEqual(len(p.origins.origins[0].notices), 2)
        self.assertEqual(p.origins.origins[0].notices[0].message,
                         "No metadata for key: copyright")
        self.assertEqual(p.origins.origins[0].notices[0].level, 'warning')
        self.assertEqual(p.origins.origins[0].notices[1].message,
                         "No metadata for key: src_url")


if __name__ == '__main__':
    unittest.main()
