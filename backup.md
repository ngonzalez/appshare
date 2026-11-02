#### Database backup

Usage, from backend/:
```
bin/rails db:load FILE=db/dumps/appshare-<time>.dump                       # dry run: says what it would replace
bin/rails db:load FILE=db/dumps/appshare-<time>.dump CONFIRM=1             # into the environment's database
bin/rails db:load FILE=... DATABASE=appshare CONFIRM=1                     # into production's (recovery)
```

How it works (lib/database_load.rb):

- CONFIRM=1: without it, the task only prints what it would do, the same convention as storage:purge_orphans.
- After a drop: if the database doesn't exist, it's created first.
- All or nothing: pg_restore --clean --if-exists --single-transaction --exit-on-error restores in one transaction, so a failure leaves the database as it was.
- Ownership: --no-owner --no-acl makes the loading user own the objects, so a production dump loads fine into your local database.
- Shared code: the connection settings and the PGPASSWORD handling moved into lib/pg_client_options.rb, used by both db:dump and db:load.

Tested for real: I dumped appshare_dev and loaded it into a new database, appshare_load_check, which the task created. I then loaded it a second time over the existing copy. Both got all 26 tables, and I dropped the database afterwards. Dev has no users, so this checked the schema rather than row counts.

Limits:

- Stop the apps first when restoring production (the scale to 0 from my previous message), or open connections will block parts of the restore.
- --clean only replaces what the dump contains. A table created by a migration after the dump stays. After a full drop that doesn't matter.
