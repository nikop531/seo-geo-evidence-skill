import importlib.util,shutil,tempfile,unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('validator',Path(__file__).with_name('validate.py'))
validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)

class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'repo'
        shutil.copytree(validator.ROOT,self.root,ignore=shutil.ignore_patterns('.git','__pycache__'))
    def test_current_package(self):validator.validate(self.root)
    def test_private_path_rejected(self):
        (self.root/'private.md').write_text('/'+'Users'+'/'+'private-person'+'/'+'internal')
        with self.assertRaises(AssertionError):validator.validate(self.root)
    def test_unregistered_source_rejected(self):
        with (self.root/'skills/seo-geo-evidence/references/seo.md').open('a') as f:f.write('\n來源G99\n')
        with self.assertRaises(AssertionError):validator.validate(self.root)
    def test_missing_reference_rejected(self):
        (self.root/'skills/seo-geo-evidence/references/geo.md').unlink()
        with self.assertRaises(AssertionError):validator.validate(self.root)

if __name__=='__main__':unittest.main()
