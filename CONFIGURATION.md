# Local configuration

Copy `.env.example` to `.env` and replace its fictional connection with your own
local settings. Never commit `.env` or paste it into logs, issues or screenshots.
An existing `DATABASE_URL` environment variable takes precedence over `.env`.

The application and Alembic use the same configuration. `alembic.ini` must not
contain credentials. A missing or blank `DATABASE_URL` produces a configuration
error without printing the connection string. Configure your database before
running migrations; never test with credentials recovered from repository history.

Run the isolated configuration tests without loading database fixtures:

```sh
python -m unittest discover -s tests -p test_configuration_offline.py
```

These tests do not connect to a database and mock dotenv to avoid reading local
secrets. They do not replace full application or migration integration tests.
Removing a file from tracking does not remove previous commits or revoke a
credential that was previously exposed.
