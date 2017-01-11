# -*- coding: utf-8 -*-
"""
Tests for the library interface
"""
import unittest

from datetime import datetime
from ads.libraries import LibraryQuery, Library


class TestLibrary(unittest.TestCase):
    """
    Test the Article object
    """

    def setUp(self):
        """
        Create a test Article instance
        """
        self.library = Library(
            name='Lirary name',
            description='Interesting library',
            public=True,
            bibcode=[],
            date_created=datetime.utcnow(),
            date_last_modified=datetime.utcnow(),
            id='ffff'
        )

    def test_equals(self):
        """
        the __eq__ method should compare bibcodes, and raise if bibcode isn't
        defined or is None
        """
        self.assertNotEqual(Library(id='NotSame'), self.library)
        with self.assertRaisesRegexp(TypeError, 'Cannot compare libraries without id'):
            Library() == self.library
        with self.assertRaisesRegexp(TypeError, 'Cannot compare libraries without id'):
            Library(id=None) == self.library

    # def test_init(self):
    #     """
    #     after init ._raw should be a dict containing a subset of all
    #     class attributes
    #     """
    #     for key, value in six.iteritems(self.article._raw):
    #         self.assertEqual(
    #             self.article.__getattribute__(key),
    #             value,
    #             msg="Instance attribute and _raw mismatch on {}".format(key)
    #         )
    #
    # def test_print_methods(self):
    #     """
    #     the class should return a user-friendly formatted identified when the
    #     __str__ or __unicode__ methods are called
    #     """
    #     self.assertEqual(
    #         '<Sudilovsky, V. et al. 2013, 2013A&A...552A.143S>',
    #         self.article.__str__()
    #     )
    #     self.assertEqual(self.article.__unicode__(), self.article.__str__())
    #     self.assertEqual(
    #         Article().__str__(),
    #         "<Unknown author Unknown year, Unknown bibcode>"
    #     )


class TestLibraryQuery(unittest.TestCase):
    """
    Tests for Library query.
    """

    def test_get_library(self):
        """
        test that a user gets all their libraries
        """
        lq = LibraryQuery()
        libs = lq.execute()

        self.assertIsInstance(libs[0], Library)
        self.assertEqual(len(libs), 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
