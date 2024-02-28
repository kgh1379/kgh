import unittest
from unittest.mock import patch
from notifications import send_notification, notify_low_stock

class TestNotifications(unittest.TestCase):

    @patch('notifications.send_notification')
    def test_send_notification(self, mock_send_notification):
        # send_notification 함수 테스트
        send_notification('Test Message', 'recipient@example.com')
        mock_send_notification.assert_called_once_with('Test Message', 'recipient@example.com')

    def test_notify_low_stock(self):
        # notify_low_stock 함수 내부에서 send_notification을 호출하는지 테스트
        with patch('notifications.send_notification') as mock_send_notification:
            notify_low_stock('Test Item', 5, 10, 'recipient@example.com')
            mock_send_notification.assert_called_once_with('Warning: Low stock for Test Item. Current quantity is 5.', 'recipient@example.com')

if __name__ == '__main__':
    unittest.main()
