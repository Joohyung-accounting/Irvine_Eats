import { useEffect, useMemo, useState } from "react";

export default function App() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/restaurants")
      .then((res) => res.json())
      .then((data) => {
        console.log("restaurants from API:", data);
        setRestaurants(data);
      })
      .catch((err) => console.error("Failed to fetch restaurants:", err));
  }, []);

  const categories = useMemo(() => {
    const set = new Set(
      restaurants.map((r) => r.category || "restaurant")
    );
    return ["All", ...Array.from(set)];
  }, [restaurants]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();

    return restaurants.filter((r) => {
      const name = r.name || "";
      const address = r.address || "";
      const cat = r.category || "restaurant";

      const okCategory = category === "All" || cat === category;
      const okQuery =
        !q ||
        name.toLowerCase().includes(q) ||
        address.toLowerCase().includes(q) ||
        cat.toLowerCase().includes(q);

      return okCategory && okQuery;
    });
  }, [restaurants, query, category]);

  return (
    <div
      style={{
        maxWidth: 900,
        margin: "40px auto",
        padding: 16,
        fontFamily: "system-ui",
      }}
    >
      <h1 style={{ marginBottom: 6 }}>Irvine Eats</h1>
      <p style={{ marginTop: 0, color: "#555" }}>
        Search and filter restaurants in Irvine.
      </p>

      <div style={{ display: "flex", gap: 12, margin: "18px 0" }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, address, or category..."
          style={{
            flex: 1,
            padding: 10,
            borderRadius: 10,
            border: "1px solid #ddd",
          }}
        />

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{
            padding: 10,
            borderRadius: 10,
            border: "1px solid #ddd",
          }}
        >
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <p style={{ color: "#777", fontSize: 14 }}>
        Showing {filtered.length} of {restaurants.length} restaurants
      </p>

      {filtered.length === 0 && (
        <p style={{ color: "#777", marginTop: 20 }}>
          No restaurants found.
        </p>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 260px))",
          gap: 12,
          justifyContent: "center",
        }}
      >
        {filtered.map((r) => (
          <div
            key={r.restaurant_id}
            style={{
              border: "1px solid #eee",
              borderRadius: 14,
              padding: 14,
            }}
          >
            <strong>{r.name}</strong>

            <div style={{ marginTop: 8, color: "#666" }}>
              {r.category || "restaurant"}
            </div>

            <div style={{ marginTop: 6, color: "#888", fontSize: 14 }}>
              {r.address || "No address"}
            </div>

            {r.phone && (
              <div style={{ marginTop: 6, color: "#888", fontSize: 14 }}>
                {r.phone}
              </div>
            )}

            {r.url && (
              <a
                href={r.url}
                target="_blank"
                rel="noreferrer"
                style={{
                  display: "inline-block",
                  marginTop: 8,
                  color: "#2563eb",
                  fontSize: 14,
                }}
              >
                Website
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

