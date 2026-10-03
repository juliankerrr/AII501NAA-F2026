import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from activity1_solution import breadth_first_search, classify_and_route


class SpamFilterTests(unittest.TestCase):
    def make_email(self, directory, domain, body):
        path = Path(directory) / "message.eml"
        path.write_text(
            f"From: sender@{domain}\nSubject: Test\nContent-Type: text/plain\n\n{body}\n",
            encoding="utf-8",
        )
        return path

    def test_allow_list_overrides_bad_words(self):
        with TemporaryDirectory() as tmp:
            source = self.make_email(tmp, "safe.example", "free " * 10)
            regular, spam = Path(tmp) / "email", Path(tmp) / "spam"
            result = classify_and_route(source, regular, spam, ["safe.example"], [], ["free"])
            self.assertEqual(result, "non-spam")
            self.assertTrue((regular / source.name).exists())

    def test_restrict_list_forces_spam(self):
        with TemporaryDirectory() as tmp:
            source = self.make_email(tmp, "blocked.example", "hello")
            regular, spam = Path(tmp) / "email", Path(tmp) / "spam"
            result = classify_and_route(source, regular, spam, [], ["blocked.example"], [])
            self.assertEqual(result, "spam")
            self.assertTrue((spam / source.name).exists())

    def test_more_than_five_bad_words_is_spam(self):
        with TemporaryDirectory() as tmp:
            source = self.make_email(tmp, "unknown.example", "free " * 6)
            result = classify_and_route(source, Path(tmp) / "email", Path(tmp) / "spam", [], [], ["free"])
            self.assertEqual(result, "spam")


class JugSearchTests(unittest.TestCase):
    def test_bfs_reaches_one_gallon(self):
        for start in ((0, 0, 0), (12, 0, 0), (0, 8, 0)):
            path = breadth_first_search(start)
            self.assertIsNotNone(path)
            self.assertEqual(1 in path[-1][1], True)

    def test_empty_state_is_already_a_valid_start(self):
        path = breadth_first_search((0, 0, 0))
        self.assertEqual(path[-1][1], (1, 8, 3))


if __name__ == "__main__":
    unittest.main()
