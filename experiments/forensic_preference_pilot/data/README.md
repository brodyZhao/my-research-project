# Data contract

Place local data in the subdirectories here and populate `metadata.csv`.
Image and mask files are intentionally not included in this scaffold.

The preparation script validates paths without copying or modifying the
source images. It creates split CSVs by source image group to avoid leakage.
