import os

from pytest_mock import MockFixture

from vault import from_env_or_vault, from_vault, from_vault_or_env


def test_from_env_or_vault(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_PASSWORD": "4321"},
    )
    vault_var = from_env_or_vault("DB_PASSWORD")
    assert vault_var == "4321"


def test_from_env_or_vault_with_env(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_PASSWORD": "4321"},
    )
    os.environ["DB_PASSWORD"] = "1234"
    vault_var = from_env_or_vault("DB_PASSWORD")
    assert vault_var == "1234"

    # Cleanup
    os.environ.pop("DB_PASSWORD")


def test_from_env_or_vault_with_none(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_NAME": "default"},
    )
    vault_var = from_env_or_vault("DB_PASSWORD")
    assert vault_var is None


def test_from_vault_or_env(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_PASSWORD": "4321"},
    )
    os.environ["DB_PASSWORD"] = "1234"
    vault_var = from_vault_or_env("DB_PASSWORD")
    assert vault_var == "4321"

    # Cleanup
    os.environ.pop("DB_PASSWORD")


def test_from_vault_or_env_without_vault(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_NAME": "default"},
    )
    os.environ["DB_PASSWORD"] = "1234"
    vault_var = from_vault_or_env("DB_PASSWORD")
    assert vault_var == "1234"

    # Cleanup
    os.environ.pop("DB_PASSWORD")


def test_from_vault(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_PASSWORD": "4321"},
    )
    vault_var = from_vault("DB_PASSWORD")
    assert vault_var == "4321"


def test_from_vault_not_exists(mocker: MockFixture) -> None:
    mocker.patch(
        "vault.vault.Vault._fetch_variables",
        return_value={"DB_NAME": "default"},
    )
    try:
        from_vault("DB_PASSWORD")
    except KeyError:
        assert True
    else:
        assert False
