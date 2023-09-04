class VaultClientImproperlyConfiguredError(Exception):
    def __init__(
        self, message: str = "Vault client is improperly configured."
    ):
        self.message = message
        super().__init__(self.message)


class InvalidPathError(Exception):
    def __init__(self, vault_path: str):
        self.message = (
            f"Your path ({vault_path}) has not been created yet "
            f"or there are no credentials in it."
        )
        super().__init__(self.message)


class ForbiddenError(Exception):
    def __init__(self, engine_name: str, vault_path: str):
        self.message = (
            f"The client does not have access to the path '{vault_path}' "
            f"or the vault engine ({engine_name}) does not exist."
        )
        super().__init__(self.message)
