import unittest
from unittest.mock import Mock, patch

from llm import chat


class LlmHttpTest(unittest.TestCase):
    @patch("llm.requests.post")
    def test_chat_calls_ollama_http_api_and_returns_content(self, post):
        response = Mock()
        response.json.return_value = {
            "message": {
                "content": "ok",
            }
        }
        response.raise_for_status.return_value = None
        post.return_value = response

        result = chat([{"role": "user", "content": "hello"}])

        self.assertEqual(result, "ok")
        post.assert_called_once_with(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3:4b",
                "messages": [{"role": "user", "content": "hello"}],
                "stream": False,
            },
            timeout=120,
        )


if __name__ == "__main__":
    unittest.main()
