import unittest
import jsAssetBrowser.api.assetBrowser as assetBrowser

class TestAssetBrowser(unittest.TestCase):

    def test_initAssetBrowser(self):
        aB = assetBrowser.AssetBrowser()
        assert aB is not None

if __name__ == '__main__':
    unittest.main()