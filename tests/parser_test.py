import unittest

from grandpybot.parser import Parser


class ParserTest(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: sentence below fails
        # Salut GP, tu connais l'adresse de Openclassrooms, par hasard ?
        self.parser = Parser()
        self.question = "Salut GrandPy ! Est-ce que tu connais, " \
                        "par hasard, l'adresse d'OpenClassrooms ?"

    @staticmethod
    def testParserStopWordsNotFound():
        try:
            spanish_parser = Parser(language='es')

            assert len(spanish_parser._stopwords) == 0
        except IOError as e:
            assert False, f"`Parser instanciation` raised an exception:\n{e}"

    def testParsing(self):
        expected = ['!', ',', 'adresse', 'openclassrooms', '?']

        parsed_data = self.parser.parse(self.question)

        self.assertEqual(expected, parsed_data)
        # Check if the original string haven't been mutated.
        self.assertEqual(self.question, self.parser.original_string)

    def testFirstExtractAddress(self):
        self.parser.parse(self.question)
        place = self.parser.find_address()

        self.assertEqual('openclassrooms', place)

    def testSecondExtractAddress(self):
        self.parser.parse("Tu connais l'adresse de la mairie de Paris")
        place = self.parser.find_address()

        self.assertEqual('mairie paris', place)

    def testThirdExtractAddress(self):
        self.parser.parse("Où se situe la Tour Eiffel ?")
        place = self.parser.find_address()

        self.assertEqual('tour eiffel', place)

    def testFourthExtractAddress(self):
        self.parser.parse("Où est la cathédrale Notre-Dame")
        place = self.parser.find_address()

        self.assertEqual('cathédrale notre-dame', place)


if __name__ == '__main__':
    unittest.main()
