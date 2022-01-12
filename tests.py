import unittest
from unittest import result
from models import SampleSet, Sample

class TestSample(unittest.TestCase):

    def test_init(self):
        """
        Test Sample init
        """
        sample = Sample(3,3)
        self.assertEqual(sample.__str__(), 'CPU: 300.0%, MEM: 3.0')


class TestSampleSet(unittest.TestCase):

    def test_list_init(self):
        """
        Test SampleSet init with list of Samples
        """
        data = [Sample(0,0), Sample(2,2), Sample(4,4)]
        result = SampleSet(data)
        self.assertIsInstance(result.export(), dict)
        self.assertCountEqual(result.export(),['timestamp','cpu','memory'])

    def test_fail_init(self):

        data = [Sample(0,0), 'fail']
        with self.assertRaises(Exception):
            result = SampleSet(data)

    def test_max(self):

        data = [Sample(0,0), Sample(2,2), Sample(4,4)]
        result = SampleSet(data)
        self.assertEqual(result._max([sample.cpu for sample in result.samples]), 4)


if __name__ == '__main__':
    unittest.main()
