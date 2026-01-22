import React from "react";
import "./App.css";

function App() {
  return (
    <div>
      {/* Navbar */}
      <nav style={styles.navbar}>
        <h1 style={styles.logo}>My React App</h1>
        <ul style={styles.navLinks}>
          <li>Home</li>
          <li>About</li>
          <li>Contact</li>
        </ul>
      </nav>

      {/* Hero Section */}
      <section style={styles.hero}>
        <h2>Welcome to the React Web App</h2>
        <p>This is a minimal hero section example.</p>
        <button style={styles.ctaButton}>Get Started</button>
      </section>
    </div>
  );
}

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "1rem 2rem",
    backgroundColor: "#1e40af",
    color: "#fff",
  },
  logo: {
    margin: 0,
  },
  navLinks: {
    listStyle: "none",
    display: "flex",
    gap: "1rem",
    margin: 0,
    padding: 0,
  },
  hero: {
    textAlign: "center",
    padding: "4rem 2rem",
    backgroundColor: "#f3f4f6",
  },
  ctaButton: {
    padding: "0.75rem 1.5rem",
    fontSize: "1rem",
    backgroundColor: "#1e40af",
    color: "#fff",
    border: "none",
    borderRadius: "0.5rem",
    cursor: "pointer",
    marginTop: "1rem",
  },
};

export default App;
