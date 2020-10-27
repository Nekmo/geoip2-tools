#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `geoip2_tools` package."""


import unittest
from click.testing import CliRunner

from geoip2_tools import geoip2_tools
from geoip2_tools import cli


class TestGeoip2_tools(unittest.TestCase):
    """Tests for `geoip2_tools` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'geoip2_tools.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
