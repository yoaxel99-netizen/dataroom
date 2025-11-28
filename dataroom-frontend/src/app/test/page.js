"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function TestPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/storage/test/`, {
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
