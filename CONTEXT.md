# magma_diff_alg Domain Glossary

**Designated migrator (Beads/Dolt schema)** — the `~/gt/magma_diff_alg` working copy is the sole clone authorized to advance schema migrations for this repository's remote-backed bead database. The `~/repos` clone and other machines consume the migrated database from the remote and do not independently migrate it.
