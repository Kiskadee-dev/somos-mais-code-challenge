def get_mock_file_content() -> str:
    path = "client/tests/mock/input-backend.json"
    with open(path, encoding="utf-8") as file:
        return file.read()
