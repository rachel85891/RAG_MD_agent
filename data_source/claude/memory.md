# ADL: Architectural Decision Log

## Decision: Migrating to TypeScript
**Date:** 2024-05-20
**Status:** Decided / In-Progress
**Context:** The project has grown in complexity, leading to frequent runtime errors and "undefined" bugs during data fetching from the Node.js backend. The existing JavaScript codebase lacks clear interfaces for the Postgres schema.

**Decision:**
I have decided to migrate the entire codebase from JavaScript to **TypeScript**. 

**Rationale:**
* **Type Safety:** Ensure that all database queries and API responses are strictly typed to prevent production crashes.
* **Developer Experience:** Better autocomplete and refactoring support within the IDE.
* **Maintainability:** Clearer definitions of data structures for future AI-driven code generation.

**Action Plan:**
1. Initialize `tsconfig.json`.
2. Install `@types/react` and `@types/node`.
3. Rename files from `.js/.jsx` to `.ts/.tsx` incrementally.