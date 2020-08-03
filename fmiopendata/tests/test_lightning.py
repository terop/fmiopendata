#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Panu Lahtinen
#
# Author(s):
#
#   Panu Lahtinen <pnuu+git@iki.fi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Test lightning parsers."""

import pytest
import mock

import numpy as np

# Define a time period that has data
ARGS = ["starttime=2010-08-01T12:00:00Z", "endtime=2010-08-01T12:01:00Z"]


def test_lightning():
    """Test parsing lightning data."""
    from fmiopendata.lightning import download_and_parse

    # The "simple" format
    res = download_and_parse("fmi::observations::lightning::simple", args=ARGS)
    num = len(res.latitudes)
    assert num > 0
    assert num == len(res.longitudes) == len(res.times) == len(res.cloud_indicator)
    assert num == len(res.ellipse_major) == len(res.multiplicity) == len(res.peak_current)

    # The multipoint coverage format
    res2 = download_and_parse("fmi::observations::lightning::multipointcoverage", args=ARGS)

    # The results should be indentical
    assert np.all(res.latitudes == res2.latitudes)
    assert np.all(res.longitudes == res2.longitudes)
    assert np.all(res.times == res.times)
    assert np.all(res.cloud_indicator == res2.cloud_indicator)
    assert np.all(res.ellipse_major == res2.ellipse_major)
    assert np.all(res.multiplicity == res2.multiplicity)
    assert np.all(res.peak_current == res2.peak_current)


@mock.patch("fmiopendata.lightning.ET")
@mock.patch("fmiopendata.lightning.read_url")
def test_unimplemented(read_url, ET):
    """Test lightning format that has not been implemented."""
    from fmiopendata.lightning import download_and_parse

    with pytest.raises(NotImplementedError):
        _ = download_and_parse("fmi::observations::lightning::nonexistent", args=ARGS)
