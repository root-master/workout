import unittest
from workout.context import Context


class TestContext(unittest.TestCase):
    def test_context(self):
        """Tests context.py."""
        context = Context(env="local")
        assert isinstance(context, Context)


if __name__ == '__main__':
    unittest.main()
