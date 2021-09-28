from unittest.mock import Mock

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from hypermodern_python import console


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> None:
    return mocker.patch("hypermodern_python.wikipedia.random_page")


@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


@pytest.mark.e2e
def test_main_suceeds_in_production_environment(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
