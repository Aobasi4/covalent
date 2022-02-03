# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the GNU Affero General Public License 3.0 (the "License").
# A copy of the License may be obtained with this software package or at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html
#
# Use of this file is prohibited except in compliance with the License. Any
# modifications or derivative works of this file must retain this copyright
# notice, and modified files must contain a notice indicating that they have
# been altered from the originals.
#
# Covalent is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
#
# Relief from the License may be granted by purchasing a commercial license.

"""Tests for Covalent command line interface (CLI) Tool."""

import tempfile

import mock
from click.testing import CliRunner

from covalent_dispatcher._cli.service import (
    _is_dispatcher_running,
    _is_ui_running,
    _read_pid,
    _rm_pid_file,
    purge,
)


def test_read_pid_nonexistent_pid_file():
    """Test the process id read function when the pid file does not exist."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        assert _read_pid(f"{tmp_dir}/nonexistent.pid") == -1


def test_read_valid_pid_file(mock_open):
    """Test the process id read function when the pid file exists."""

    with mock.patch("__main__.open", mock_open(read_data=1984)):
        res = _read_pid(filename="mock.pid")
    assert res == 1984


def test_rm_pid():
    pass


def test_port_from_pid():
    pass


def test_next_available_port():
    pass


def test_graceful_start():
    pass


def test_graceful_shutdown():
    pass


def test_graceful_restart():
    pass


def test_start():
    pass


def test_stop():
    pass


def test_restart():
    pass


def test_status():
    pass


def test_is_dispatcher_running(mocker):
    """Test the dispatcher server status checking function."""

    mocker.patch("covalent_dispatcher._cli.service._read_pid", return_value=1)
    assert _is_dispatcher_running()

    mocker.patch("covalent_dispatcher._cli.service._read_pid", return_value=-1)
    assert not _is_dispatcher_running()


def test_is_ui_running(mocker):
    """Test the user interface server status checking function."""

    mocker.patch("covalent_dispatcher._cli.service._read_pid", return_value=1)
    assert _is_ui_running()

    mocker.patch("covalent_dispatcher._cli.service._read_pid", return_value=-1)
    assert not _is_ui_running()


def test_purge(mocker):
    """Test the 'covalent purge' CLI command."""

    from covalent_dispatcher._cli.service import DISPATCHER_PIDFILE, UI_PIDFILE, get_config

    runner = CliRunner()
    graceful_shutdown_mock = mocker.patch("covalent_dispatcher._cli.service._graceful_shutdown")
    shutil_rmtree_mock = mocker.patch("covalent_dispatcher._cli.service.shutil.rmtree")
    purge_config_mock = mocker.patch("covalent_dispatcher._cli.service.cm.purge_config")
    result = runner.invoke(purge)
    graceful_shutdown_mock.assert_has_calls(
        [mock.call("dispatcher", DISPATCHER_PIDFILE), mock.call("UI", UI_PIDFILE)]
    )
    shutil_rmtree_mock.assert_has_calls(
        [
            mock.call(get_config("sdk.log_dir"), ignore_errors=True),
            mock.call(get_config("dispatcher.cache_dir"), ignore_errors=True),
            mock.call(get_config("dispatcher.log_dir"), ignore_errors=True),
            mock.call(get_config("user_interface.log_dir"), ignore_errors=True),
        ]
    )
    purge_config_mock.assert_called_once()
    assert result.output == "Covalent server files have been purged.\n"
