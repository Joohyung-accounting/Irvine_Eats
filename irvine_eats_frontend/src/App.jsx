import { useEffect, useMemo, useState } from "react";

const SAMPLE = [
  { id: 1, name: "BCD Tofu House", category: "Korean", address: "Irvine, CA", rating: 4.6 },
  { id: 2, name: "Din Tai Fung", category: "Taiwanese", address: "Irvine, CA", rating: 4.7 },
  { id: 3, name: "Tender Greens", category: "Healthy", address: "Irvine, CA", rating: 4.3 },
];

export default function App() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");
  const [restaurants, setRestaurants] = useState(SAMPLE);

  const categories = useMemo(() => {
    const set = new Set(restaurants.map(r => r.category));
    return ["All", ...Array.from(set)];
  }, [restaurants]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return restaurants.filter(r => {
      const okCategory = category === "All" || r.category === category;
      const okQuery =
        !q ||
        r.name.toLowerCase().includes(q) ||
        r.address.toLowerCase().includes(q);
      return okCategory && okQuery;
    });
  }, [restaurants, query, category]);

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 16, fontFamily: "system-ui" }}>
      <h1 style={{ marginBottom: 6 }}>Irvine Eats</h1>
      <p style={{ marginTop: 0, color: "#555" }}>Search and filter restaurants in Irvine.</p>

      <div style={{ display: "flex", gap: 12, margin: "18px 0" }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name or address..."
          style={{ flex: 1, padding: 10, borderRadius: 10, border: "1px solid #ddd" }}
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{ padding: 10, borderRadius: 10, border: "1px solid #ddd" }}
        >
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 260px))", gap: 12, justifyContent: "center", }}>
        {filtered.map(r => (
          <div key={r.id} style={{ border: "1px solid #eee", borderRadius: 14, padding: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
              <strong>{r.name}</strong>
              <span style={{ color: "#666" }}>⭐ {r.rating}</span>
            </div>
            <div style={{ marginTop: 8, color: "#666" }}>{r.category}</div>
            <div style={{ marginTop: 6, color: "#888", fontSize: 14 }}>{r.address}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 24, color: "#777", fontSize: 13 }}>
        Next: replace SAMPLE with API data from Flask.
      </div>
    </div>
  );
}

