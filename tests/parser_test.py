import unittest
from grandpybot.parser import Parser


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()
        self.question = "Salut GrandPy ! Est-ce que tu connais, " \
                        "par hasard, l'adresse d'OpenClassrooms ?"

    def testSimpleParsing(self):
        expected = [
            'salut', 'grandpy', '!', 'connais', ',',
            'hasard', "adresse", "openclassrooms", '?'
        ]

        parsed_data = self.parser.parse(self.question)

        self.assertEqual(expected, parsed_data)
        # Check if the original string haven't been mutated.
        self.assertEqual(self.question, self.parser.original_string)

    def testParseAddressSubject(self):
        self.parser.parse(self.question)
        address_subject = self.parser.find_address()

        self.assertEqual('openclassrooms', address_subject)


if __name__ == '__main__':
    unittest.main()
