# UI & Accessibility Rules

## RTL (Right-to-Left) Support
The application must fully support Hebrew and Arabic interfaces. 

* **Directionality:** Use the HTML attribute `dir="rtl"` on the root element when the language is set to Hebrew/Arabic.
* **Tailwind Logical Properties:** Avoid using `ml-` (margin-left) or `pr-` (padding-right). Instead, use logical properties like `ms-` (margin-start) and `pe-` (padding-end) to ensure layout flips correctly between LTR and RTL.
* **Alignment:** Text alignment should default to `text-start`.

## Accessibility (a11y) Standards
* **Contrast:** Ensure all text passes WCAG AA contrast ratios against the primary Dark Blue (#001f3f) background.
* **Keyboard Navigation:** All interactive elements (buttons, links, inputs) must have a visible `:focus` state.
* **ARIA Labels:** Every icon-only button must include an `aria-label` describing its function.
* **Semantic HTML:** Use `<main>`, `<nav>`, and `<section>` tags instead of generic `<div>` wrappers where possible.