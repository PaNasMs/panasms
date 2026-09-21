import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("artifacts", Path(__file__).resolve().parents[1] / "scripts/build-artifacts.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BuildArtifactTest(unittest.TestCase):
    def test_unique_prerelease_version(self):
        first = build.ci_version("0.2.5", "2026-09-21T21:34:56Z", "123", "1")
        self.assertEqual(first, "0.2.5~ci.20260921213456.123.1")
        self.assertNotEqual(first, build.ci_version("0.2.5", "2026-09-21T21:34:56Z", "123", "2"))
        import subprocess
        subprocess.run(["dpkg", "--compare-versions", first, "lt", "0.2.5"], check=True)

    def test_invalid_version_inputs_rejected(self):
        for base, date, run, attempt in [("../bad", "2026-09-21T21:34:56Z", "1", "1"),
                                          ("0.2.5", "invalid", "1", "1"),
                                          ("0.2.5", "2026-09-21T21:34:56Z", "1\n2", "1")]:
            with self.assertRaises(ValueError):
                build.ci_version(base, date, run, attempt)

    def test_wrong_elf_and_missing_runtime_library_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "core"
            binary.write_bytes(b"\x7fELF\x02\x01" + bytes(12) + struct.pack("<H", 62))
            with self.assertRaises(ValueError):
                build.verify_elf(binary, "arm64")
            with patch.object(build, "output", return_value="libpam.so.0 => not found"):
                with self.assertRaises(ValueError):
                    build.verify_elf(binary, "amd64")
            with patch.object(build, "output", return_value="libpam.so.0 => /lib/libpam.so.0"):
                build.verify_elf(binary, "amd64")


if __name__ == "__main__":
    unittest.main()
