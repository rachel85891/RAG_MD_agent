# Kiro Agent: Internal System Logic & Constraints

## System Overview
This document outlines the critical technical boundaries and architectural decisions for the Kiro Agent's environment. Adhering to these constraints is mandatory for maintaining system stability.

## Technical Constraints

### 1. API Server Memory Limits
* **Threshold:** The API server is capped at **2GB RAM** per instance.
* **Optimization:** Avoid large in-memory data processing. Use Node.js `streams` for handling large JSON payloads or file exports.
* **Garbage Collection:** Ensure no global variables are used to store temporary request data to prevent memory leaks.

### 2. Session Management (Redis)
* **Storage:** All user sessions and distributed locks are managed via **Redis**.
* **TTL Policy:** Sessions are set to expire after 24 hours of inactivity.
* **Consistency:** Always use the `redis-client` wrapper to ensure atomic operations during session updates. Do not fall back to local memory for session storage.

### 3. Database Connection Pooling
* **PostgreSQL:** Maximum concurrent connections are limited to **20**. 
* **Protocol:** Use the `pg-pool` library to manage recycling of idle connections. Always release connections in a `finally` block.

---

## ⚠️ Critical Security Warning

> [!CAUTION]
> **Unauthorized Modification Prohibited:** > Do NOT modify the `Auth Middleware` (`src/middleware/auth.ts`) under any circumstances without explicit, documented approval from the **Lead Developer**. 
> Any changes to the JWT verification logic or role-based access control (RBAC) could create severe security vulnerabilities.

---

## Performance Targets
* **P99 Latency:** All internal API routes must respond within **< 200ms**.
* **Rate Limiting:** Maximum **100 requests per minute** per IP address, enforced at the Nginx layer.