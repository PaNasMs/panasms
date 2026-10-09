import importlib.util
import io
import os
from pathlib import Path
import unittest
import urllib.error
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("resolver", Path(__file__).resolve().parents[1] / "scripts/resolve-build.py")
resolver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resolver)


def missing(*_):
    raise urllib.error.HTTPError("url", 404, "Not Found", {}, io.BytesIO())


class PairedRefTest(unittest.TestCase):
    def test_paired_branch_is_used_when_it_exists(self):
        with patch.dict(os.environ, {"FRONTEND_PAIRED_REF": "claude/version"}, clear=False), \
                patch.object(resolver, "resolve", side_effect=lambda name, ref: ref) as resolve:
            os.environ.pop("FRONTEND_REF", None)
            self.assertEqual(resolver.resolve_component("frontend", None), "claude/version")
            resolve.assert_called_once_with("frontend", "claude/version")

    def test_missing_paired_branch_falls_back_to_main(self):
        calls = []

        def fake(name, ref):
            calls.append(ref)
            if ref != "main":
                missing()
            return ref

        with patch.dict(os.environ, {"BACKEND_PAIRED_REF": "only-in-frontend"}, clear=False), \
                patch.object(resolver, "resolve", side_effect=fake):
            os.environ.pop("BACKEND_REF", None)
            self.assertEqual(resolver.resolve_component("backend", None), "main")
        self.assertEqual(calls, ["only-in-frontend", "main"])

    def test_explicit_ref_and_release_lock_ignore_pairing(self):
        with patch.dict(os.environ, {"BACKEND_REF": "abc", "BACKEND_PAIRED_REF": "other"}, clear=False), \
                patch.object(resolver, "resolve", side_effect=lambda name, ref: ref):
            self.assertEqual(resolver.resolve_component("backend", None), "abc")
            self.assertEqual(resolver.resolve_component("backend", {"sources": {"backend": "f" * 40}}), "f" * 40)

    def test_other_errors_are_not_hidden(self):
        def forbidden(*_):
            raise urllib.error.HTTPError("url", 403, "Forbidden", {}, io.BytesIO())

        with patch.dict(os.environ, {"FRONTEND_PAIRED_REF": "x"}, clear=False), \
                patch.object(resolver, "resolve", side_effect=forbidden):
            os.environ.pop("FRONTEND_REF", None)
            with self.assertRaises(urllib.error.HTTPError):
                resolver.resolve_component("frontend", None)


if __name__ == "__main__":
    unittest.main()
