from unittest.mock import patch, Mock
from python_foundations.api_client01 import inspect_http_status
import requests

def test_successful_http_request(capsys):
    # 1. Setup the mock response object
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None

    # 2. Patch the requests.get method
    with patch("python_foundations.api_client01.requests.get") as mock_get:
        mock_get.return_value = mock_response

        # 3. Call function with the expected URL
        test_url = "https://httpbin.org/get"
        inspect_http_status(test_url)

        # 4. Verify the requests.get() parameters
        mock_get.assert_called_once_with("https://httpbin.org/get", timeout=10)

        # 5. Verify raise_for_status() was called on the mock response
        mock_response.raise_for_status.assert_called_once()

    # 6. Use pytest's capsys fixture to capture the printed text
    captured = capsys.readouterr()

    # 7. Verify the expected output strings appear in the terminal text
    assert "HTTP Status: 200" in captured.out
    assert "Request successful" in captured.out

def test_http_404_error(capsys):
    # 1. Setup the mock response object to simulate a 404 error
    mock_response = Mock()
    mock_response.status_code = 404

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("404 Client Error: Not Found")
    )

    # 2. Patch requests.get
    with patch("python_foundations.api_client01.requests.get") as mock_get:
        mock_get.return_value = mock_response

        # 3. Call the function with the requested 404 test URL
        test_url = "https://httpbin.org/status/404"
        inspect_http_status(test_url)

        # 4. Assert requests.get() was called once with expected URL and timeout=10
        mock_get.assert_called_once_with(test_url, timeout=10)

        # 5. Assert raise_for_status() was called once
        mock_response.raise_for_status.assert_called_once()

    # 6. Capture the output using pytest capsys fixture
    captured = capsys.readouterr()

    # 7. Verify the output text requirements
    assert "HTTP Status: 404" in captured.out
    assert "HTTP Error: 404" in captured.out
    assert "Request successful" not in captured.out

def test_http_500_error(capsys):
    # 1. Setup the mock response object to simulate a 500 error
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("500 Server Error: Internal Server Error")
    )

    # 2. Patch requests.get
    with patch("python_foundations.api_client01.requests.get") as mock_get:
        mock_get.return_value = mock_response

        # 3. Call the function with the requested 404 test URL
        test_url = "https://httpbin.org/status/500"
        inspect_http_status(test_url)

        # 4. Verify that requests.get() and raise_for_status() are each called once
        mock_get.assert_called_once_with(test_url, timeout=10)
        mock_response.raise_for_status.assert_called_once()

    # 5. Capture the terminal outputs
    captured = capsys.readouterr()

    # 6. Verify that it prints the 500 status and error message, and lacks "Request successful"
    assert "HTTP Status: 500" in captured.out
    assert "HTTP Error: 500" in captured.out
    assert "Request successful" not in captured.out

def test_http_timeout(capsys):
    # 1. Patch requests.get() directly
    with patch("python_foundations.api_client01.requests.get") as mock_get:
        # Configure the mock get call to raise a Timeout exception immediately
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        # 2. Call function with the expected URL
        test_url = "https://httpbin.org"
        inspect_http_status(test_url)

        # 3. Verify that requests.get() was called once with the expected URL and timeout=10
        mock_get.assert_called_once_with(test_url, timeout=10)

    # 4. Use pytest's capsys fixture to capture console prints
    captured = capsys.readouterr()

    # 5. Verify the required terminal output behaviors
    assert "ERROR: The HTTP request timed out" in captured.out
    assert "Request successful" not in captured.out
    assert "HTTP Status:" not in captured.out

def test_http_connection_error(capsys):
    #1. Patch requests.get() directly
    with patch("python_foundations.api_client01.requests.get") as mock_get:
        # Configure requests.get() to raise a ConnectionError immediately
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        # 2. Call function with the specified local test URL
        test_url = "http://127.0.0.1:1"
        inspect_http_status(test_url)

        # 3. Verify that requests.get() was called once with the expected URL and timeout=10
        mock_get.assert_called_once_with(test_url, timeout=10)

    # 4. Use pytest's capsys fixture to capture console prints
    captured = capsys.readouterr()

    # 5. Verify the required terminal output behaviors
    assert "ERROR: Unable to connect to remote server" in captured.out
    assert "Request successful" not in captured.out
    assert "HTTP Status:" not in captured.out
