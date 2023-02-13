import unittest
from PIL import Image
import QueueWatcher
import unittest

class TestQueueWatcher(unittest.TestCase):
    def setUp(self):
        self.queueWatcher = QueueWatcher.QueueWatcher()
        # self.queueWatcher.show_window()

    def test_set_position(self):
        self.queueWatcher.set_position()
    
    def test_check_queue(self):
        self.queueWatcher.check_queue()
    
    def test_get_queueing_image(self):
        self.queueWatcher = QueueWatcher.QueueWatcher()
        self.queueWatcher.get_queueing_image()
    

if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(TestQueueWatcher("test_set_position"))
    # suite.addTest(TestQueueWatcher("test_check_queue"))
    suite.addTest(TestQueueWatcher("test_get_queueing_image"))
    unittest.TextTestRunner().run(suite)