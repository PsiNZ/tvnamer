#!/usr/bin/env python
#encoding:utf-8
#author:dbr/Ben
#project:tvnamer
#repository:http://github.com/dbr/tvnamer
#license:Creative Commons GNU GPL v2
# http://creativecommons.org/licenses/GPL/2.0/

"""Functional tests for tvnamer tests
"""

from functional_runner import run_tvnamer, verify_out_data


def test_simple_single_file():
    """Test most simple usage
    """

    out_data = run_tvnamer(
        with_files = ['scrubs.s01e01.avi'],
        with_input = "1\ny\n")

    expected_files = ['Scrubs - [01x01] - My First Day.avi']

    verify_out_data(out_data, expected_files)


def test_simple_multiple_files():
    """Tests simple interactive usage with multiple files
    """

    input_files = [
        'scrubs.s01e01.hdtv.fake.avi',
        'my.name.is.earl.s01e01.fake.avi',
        'a.fake.show.s12e24.fake.avi',
        'total.access.s01e01.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'My Name Is Earl - [01x01] - Pilot.avi',
        'a fake show - [12x24].avi',
         'Total Access 24_7 - [01x01] - Episode #1.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_input = "y\n1\ny\n1\ny\n1\ny\ny\n")

    verify_out_data(out_data, expected_files)


def test_simple_batch_functionality():
    """Tests renaming single files at a time, in batch mode
    """

    tests = [
        {'in':'scrubs.s01e01.hdtv.fake.avi',
        'expected':'Scrubs - [01x01] - My First Day.avi'},
        {'in':'my.name.is.earl.s01e01.fake.avi',
        'expected':'My Name Is Earl - [01x01] - Pilot.avi'},
        {'in':'a.fake.show.s12e24.fake.avi',
        'expected':'a.fake.show.s12e24.fake.avi'},
        {'in': 'total.access.s01e01.avi',
        'expected': 'Total Access 24_7 - [01x01] - Episode #1.avi'},
    ]

    for curtest in tests:

        def _the_test():
            out_data = run_tvnamer(
                with_files = [curtest['in'], ],
                with_flags = ['--batch'],
            )
            verify_out_data(out_data, [curtest['expected'], ])

        _the_test.description = "test_simple_functionality_%s" % curtest['in']
        yield _the_test


def test_interactive_always_option():
    """Tests the "a" always rename option in interactive UI
    """

    input_files = [
        'scrubs.s01e01.hdtv.fake.avi',
        'my.name.is.earl.s01e01.fake.avi',
        'a.fake.show.s12e24.fake.avi',
        'total.access.s01e01.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'My Name Is Earl - [01x01] - Pilot.avi',
        'a fake show - [12x24].avi',
         'Total Access 24_7 - [01x01] - Episode #1.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ["--selectfirst"],
        with_input = "a\n")

    verify_out_data(out_data, expected_files)


def test_unicode_in_inputname():
    """Tests parsing a file with unicode in the input filename
    """
    input_files = [
        u'The Big Bang Theory - S02E07 - The Panty Pin\u0303ata Polarization.avi']

    expected_files = [
        u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ["--batch"])

    verify_out_data(out_data, expected_files)


def test_unicode_in_search_results():
    """Show with unicode in search results
    """
    input_files = [
        'psych.s04e11.avi']

    expected_files = [
        'Psych - [04x11] - Thrill Seekers & Hell Raisers.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_input = '1\ny\n')

    verify_out_data(out_data, expected_files)


def test_renaming_always_doesnt_overwrite():
    """If trying to rename a file that exists, should not create new file
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    expected_files = [
        'Scrubs.s01e01.avi',
        'Scrubs - [01x01] - My First Day.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--batch'])

    verify_out_data(out_data, expected_files)


def test_not_overwritting_unicode_filename():
    """Test no error occurs when warning about a unicode filename being overwritten
    """
    input_files = [
        u'The Big Bang Theory - S02E07.avi',
        u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi']

    expected_files = [
        u'The Big Bang Theory - S02E07.avi',
        u'The Big Bang Theory - [02x07] - The Panty Pin\u0303ata Polarization.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--batch'])

    verify_out_data(out_data, expected_files)


def test_not_recursive():
    """Tests the nested files aren't found when not recursive
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--not-recursive', '--batch'],
        run_on_directory = True)

    verify_out_data(out_data, expected_files)


def test_not_recursive():
    """Tests the nested files aren't found when not recursive
    """
    input_files = [
        'Scrubs.s01e01.avi',
        'nested/subdir/Scrubs.s01e02.avi']

    expected_files = [
        'Scrubs - [01x01] - My First Day.avi',
        'nested/subdir/Scrubs - [01x02] - My Mentor.avi']

    out_data = run_tvnamer(
        with_files = input_files,
        with_flags = ['--recursive', '--batch'],
        run_on_directory = True)

    verify_out_data(out_data, expected_files)


if __name__ == '__main__':
    test_not_overwritting_unicode_filename()
