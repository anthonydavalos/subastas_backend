"""Configuration tests that need no database, driver, or real .env values."""

import ast
import configparser
import os
from pathlib import Path
import runpy
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock, patch


class ConfigurationTests(unittest.TestCase):
    def load_config(self):
        dotenv = ModuleType("dotenv")
        dotenv.load_dotenv = Mock()
        source = Path(__file__).resolve().parents[1] / "db" / "config.py"
        with patch.dict(sys.modules, {"dotenv": dotenv}):
            config = runpy.run_path(str(source))
        return config, dotenv.load_dotenv

    def test_missing_or_blank_url_fails_without_sensitive_value(self):
        config, _ = self.load_config()
        for values in ({}, {"DATABASE_URL": "   "}):
            with patch.dict(os.environ, values, clear=True):
                with self.assertRaisesRegex(RuntimeError, "DATABASE_URL must be configured"):
                    config["get_database_url"]()

    def test_environment_url_is_returned_without_interpolation(self):
        config, _ = self.load_config()
        synthetic = "postgresql://example:fake%25value@localhost/example"
        with patch.dict(os.environ, {"DATABASE_URL": synthetic}, clear=True):
            self.assertEqual(config["get_database_url"](), synthetic)

    def test_dotenv_location_is_explicit_and_does_not_override_environment(self):
        _, loader = self.load_config()
        loader.assert_called_once()
        self.assertEqual(loader.call_args.kwargs["dotenv_path"], Path(__file__).resolve().parents[1] / ".env")
        self.assertNotIn("override", loader.call_args.kwargs)

    def test_ini_has_no_connection_and_preserves_logging(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read(Path(__file__).resolve().parents[1] / "alembic.ini")
        self.assertFalse(config.has_option("alembic", "sqlalchemy.url"))
        self.assertEqual(config["alembic"]["script_location"], "alembic")
        self.assertEqual(config["loggers"]["keys"], "root,sqlalchemy,alembic")

    def test_both_migration_modes_use_runtime_url_without_connecting(self):
        source = Path(__file__).resolve().parents[1] / "alembic" / "env.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        functions = [item for item in tree.body if isinstance(item, ast.FunctionDef)]
        synthetic = "postgresql://example:fake%25value@localhost/example"
        context = MagicMock()
        engine_factory = MagicMock()
        config = Mock()
        config.config_ini_section = "alembic"
        config.get_section.return_value = {}
        scope = {"context": context, "config": config,
                 "get_database_url": lambda: synthetic,
                 "engine_from_config": engine_factory,
                 "pool": SimpleNamespace(NullPool=object()), "target_metadata": object()}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), "exec"), scope)
        scope["run_migrations_offline"]()
        self.assertEqual(context.configure.call_args.kwargs["url"], synthetic)
        engine_factory.assert_not_called()
        scope["run_migrations_online"]()
        self.assertEqual(engine_factory.call_args.args[0]["sqlalchemy.url"], synthetic)
        self.assertEqual(context.run_migrations.call_count, 2)


if __name__ == "__main__":
    unittest.main()
