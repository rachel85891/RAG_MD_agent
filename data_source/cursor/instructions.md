# Development Instructions

## General Rules
* Write clean, modular code following DRY (Don't Repeat Yourself) principles.
* Use TypeScript for all new components to ensure type safety.
* Document complex functions with JSDoc comments.

## Styling & UI
* **Framework:** Use **Tailwind CSS** only for all styling. No external CSS files or CSS modules.
* **Color Palette:**
    - Primary Color: Dark Blue (`#001f3f`).
    - Secondary Color: Light Gray (`#f4f4f4`).
* **Components:** Use a mobile-first responsive design approach.
* **Icons:** Use Lucide-React for all iconography.

## Database Constraints
* All table names should be lowercase and plural.
* Always include `created_at` and `updated_at` timestamps for every table.