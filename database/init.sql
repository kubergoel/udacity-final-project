SELECT 'CREATE DATABASE casting_agency'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'casting_agency')\gexec

SELECT 'CREATE DATABASE test_casting_agency'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_casting_agency')\gexec

