// Optional helper for loading Schema/index.schema.json into a landing page.
// Usage:
//   <script src="./Schema/schema-loader.js" defer></script>

async function loadLandingPageSchema() {
  try {
    const response = await fetch("./Schema/index.schema.json");

    if (!response.ok) {
      throw new Error(`Schema file not found: ${response.status}`);
    }

    const schema = await response.json();
    const script = document.createElement("script");

    script.type = "application/ld+json";
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  } catch (error) {
    console.warn("Schema loader error:", error);
  }
}

loadLandingPageSchema();
