# File and document storage strategy

Clinical documents and images should be stored outside the relational database in encrypted object storage. The database stores metadata, ownership, branch, clinical context, retention class, checksum, and object key. Module 01 ships a local adapter for development; production should bind the same service interface to S3, Azure Blob Storage, or GCS with bucket policies, object versioning, malware scanning, and lifecycle retention.
