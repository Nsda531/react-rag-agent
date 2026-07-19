import unittest


class DefaultThreadIdTest(unittest.TestCase):
    def test_default_thread_id_is_medical_project_specific(self):
        from config import DEFAULT_THREAD_ID

        self.assertEqual(DEFAULT_THREAD_ID, "medical_terminal_user_v1")


if __name__ == "__main__":
    unittest.main()
