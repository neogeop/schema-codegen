# Sample application using `schema-codegen`

This `example` python application is a FastAPI application that:

- Defines SQL first migrations
- Depends on `schema-codegen` to apply the migrations and generate SQL models from the DB tables
- Showcases an integration test which uses `test-containers` and `schema-codegen` to setup the test environment and wire FastAPI  