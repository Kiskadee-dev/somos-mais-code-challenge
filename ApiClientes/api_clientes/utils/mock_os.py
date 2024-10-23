import os


def mock_os(mocker):
    original_os_environ_get = os.environ.get

    def side_effect(*args, **kwargs):
        match args[0]:
            case "TESTING_INIT_RETURNS_MOCKED_RESPONSES":
                return "False"
            case "INIT":
                return "True"
            case _:
                return original_os_environ_get(*args, **kwargs)

    mocker.patch("os.environ.get", side_effect=side_effect)
