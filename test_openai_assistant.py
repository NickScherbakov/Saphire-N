import unittest
from unittest.mock import patch
from openai_assistant import OpenAIAssistant

class TestOpenAIAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = OpenAIAssistant()

    @patch('openai_assistant.requests.post')
    def test_process_request_success(self, mock_post):
        # Настройка мок-ответа от OpenAI API
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {
            'choices': [{'message': {'content': 'Тестовый ответ'}}]
        }

        response = self.assistant.process_request("Какой сегодня день?")
        self.assertEqual(response, 'Тестовый ответ')

    @patch('openai_assistant.requests.post')
    def test_process_request_failure(self, mock_post):
        # Настройка мок-ответа от OpenAI API с ошибкой
        mock_post.side_effect = Exception("Ошибка при обращении к API")

        with self.assertRaises(Exception) as context:
            self.assistant.process_request("Какой сегодня день?")
        
        self.assertTrue("Ошибка при обращении к API" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
