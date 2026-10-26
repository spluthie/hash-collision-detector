# hash-collision-detector

Simple program that scans a directory, computes file
hashes (MD5, SHA-1, SHA-256) and classifies each
file as **unique**, **copy** or **collision**.

## How files are classified

**Unique** - no other file in the folder shares any hash with it.
**Copy** - all hashes match another file.
**Collision** - some hashes match another file, but others differ.

