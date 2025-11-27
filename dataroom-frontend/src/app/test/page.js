"use client";

import { useEffect, useState } from "react";

export default function TestPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/storage/test/", {
        credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => setData(data.message))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1>Test Page</h1>
      <p>{data ? data : "Loading..."}</p>
    </div>
  );
}
