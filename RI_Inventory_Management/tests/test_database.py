import unittest
from unittest.mock import patch
from database import get_storage_items, get_disposal_items

class TestDatabase(unittest.TestCase):

    @patch('database.get_db_connection')
    def test_get_storage_items(self, mock_get_db_connection):
        # 모의 데이터베이스 컬렉션 준비
        mock_collection = mock_get_db_connection.return_value.storage
        mock_collection.find.return_value = [{'item_id': 1, 'name': 'Test Item'}]

        # get_storage_items 함수 테스트
        items = get_storage_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'Test Item')

    @patch('database.get_db_connection')
    def test_get_disposal_items(self, mock_get_db_connection):
        # 모의 데이터베이스 컬렉션 준비
        mock_collection = mock_get_db_connection.return_value.disposal
        mock_collection.find.return_value = [{'item_id': 2, 'name': 'Disposed Item'}]

        # get_disposal_items 함수 테스트
        items = get_disposal_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['name'], 'Disposed Item')

if __name__ == '__main__':
    unittest.main()
