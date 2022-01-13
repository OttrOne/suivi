import unittest
from models import SampleSet, Sample, Config

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


class TestConfig(unittest.TestCase):

    def test_init(self):
        # might not be the best test case with a file dependency...
        config = Config('test.yaml')
        self.assertEqual(config.section('fail'), {})
        self.assertLessEqual({'image' : 'jordi/ab'}.items(), config.section('penetration').items())

if __name__ == '__main__':
    unittest.main()
