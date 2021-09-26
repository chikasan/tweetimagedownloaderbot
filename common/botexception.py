class BotException(Exception):
    """Bot例外クラス."""

    def __init__(self, arg: str = ""):
        """[summary].

        Args:
            arg (str, optional): [description]. Defaults to "".
        """
        self.arg: str = arg

    def __str__(self) -> str:
        """[summary].

        Returns:
            [type]: [description]
        """
        return f"{self.arg}"

    pass
