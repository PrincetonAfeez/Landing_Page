/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./pages/templates/**/*.html", "./pages/templatetags/**/*.py"],
  theme: {
    extend: {
      colors: {
        brand: {
          ink: "var(--brand-ink)",
          muted: "var(--brand-muted)",
          primary: "var(--brand-primary)",
          primaryDark: "var(--brand-primary-dark)",
          gold: "var(--brand-gold)",
          coral: "var(--brand-coral)",
          paper: "var(--brand-paper)",
          mist: "var(--brand-mist)",
        },
      },
      boxShadow: {
        soft: "0 24px 70px rgba(31, 79, 70, 0.14)",
      },
    },
  },
  plugins: [],
};
