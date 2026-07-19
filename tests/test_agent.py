import unittest
from unittest.mock import patch

from agent import agent_node


class AgentNodeTest(unittest.TestCase):
    @patch("agent.chat")
    def test_finish_answer_can_be_printed_in_windows_gbk_terminal(self, chat):
        chat.return_value = '{"thought":"done","action":"finish","action_input":"ok"}'

        state = agent_node({"question": "hello"})

        state["answer"].encode("gbk")


if __name__ == "__main__":
    unittest.main()
