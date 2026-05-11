# Schema Folder

This `Schema/` folder contains simple JSON-LD structured data files for a landing page website.

## Files

- `organization.schema.json` — Basic organization/brand schema.
- `website.schema.json` — Website schema with search action placeholder.
- `webpage.schema.json` — Landing page schema.
- `faq.schema.json` — FAQ schema template.
- `breadcrumb.schema.json` — Breadcrumb schema template.
- `index.schema.json` — Combined starter graph using the common schemas.
- `schema-loader.js` — Optional helper to inject `index.schema.json` into a page.

## How to use

1. Copy the `Schema/` folder into the root of your repository.
2. Replace placeholder values such as:
   - `Your Brand Name`
   - `https://example.com/`
   - `contact@example.com`
   - `Your landing page title`
3. Add the JSON-LD to your HTML page:

```html
<script type="application/ld+json">
  <!-- Paste the JSON from one schema file here -->
</script>
```

For a simple landing page, `index.schema.json` is usually enough after editing the placeholders.
