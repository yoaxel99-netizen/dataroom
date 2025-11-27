"use client";

import {useEffect, useState, useCallback} from "react";
import Script from "next/script";
import {useRouter} from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

export default function Home() {
    const [files, setFiles] = useState([]);
    const [isLoadingFiles, setIsLoadingFiles] = useState(false);
    const [error, setError] = useState(null);
    const router = useRouter();

    const connectGoogleDrive = useCallback(() => {
        window.location.href = `${API_URL}/auth/google/consent/`;
    }, []);

    const deleteFile = useCallback((uid) => {
        if (!window.confirm("Are you sure you want to delete this file?")) return;

        const csrf = getCSRFToken();

        fetch(`${API_URL}/storage/delete/${uid}`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf,
            },
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`Failed to delete: ${res.status}`);
                }
                return res.json();
            })
            .then(() => {
                setFiles((prev) => prev.filter((f) => f.uid !== uid));
            })
            .catch((err) => {
                console.error("Delete error:", err);
                alert("Could not delete file.");
            });
    }, []);


    useEffect(() => {
        async function fetchFiles() {
            try {
                setIsLoadingFiles(true);
                setError(null);

                const res = await fetch(`${API_URL}/storage/list/`, {
                    credentials: "include",
                });

                if (!res.ok) {
                    throw new Error(`Failed to load files: ${res.status}`);
                }

                const data = await res.json();
                setFiles(data);
            } catch (err) {
                console.error("Error loading files:", err);
                setError(err.message);
            } finally {
                setIsLoadingFiles(false);
            }
        }

        fetchFiles();
    }, []);

    return (
        <section style={{marginTop: "2rem"}}>
            <button
                onClick={connectGoogleDrive}
                style={{marginBottom: "1rem", padding: "0.5rem 1rem"}}
            >
                Connect Google Drive
            </button>

            <button onClick={() => router.push("/file-picker")}>
                Import from Google Drive
            </button>

            <h2>Imported files</h2>

            {isLoadingFiles && <p>Loading files…</p>}
            {error && <p style={{color: "red"}}>{error}</p>}

            {!isLoadingFiles && files.length === 0 && !error && (
                <p>No files imported yet.</p>
            )}

            {files.length > 0 && (
                <table
                    style={{
                        borderCollapse: "collapse",
                        width: "100%",
                        marginTop: "1rem",
                        fontSize: "0.9rem",
                    }}
                >
                    <thead>
                    <tr>
                        <th style={{borderBottom: "1px solid #ccc", textAlign: "left"}}>
                            Name
                        </th>
                        <th style={{borderBottom: "1px solid #ccc", textAlign: "left"}}>
                            MIME type
                        </th>
                        <th style={{borderBottom: "1px solid #ccc", textAlign: "left"}}>
                            Uploaded at
                        </th>
                        <th style={{borderBottom: "1px solid #ccc"}}>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {files.map((file) => (
                        <tr key={file.uid}>
                            <td style={{padding: "0.3rem 0"}}>{file.name}</td>
                            <td>{file.mimeType}</td>
                            <td>{new Date(file.uploaded_at).toLocaleString()}</td>
                            <td>
                                <button
                                    onClick={() => deleteFile(file.uid.toString())}
                                    style={{marginRight: "0.5rem"}}
                                >
                                    Delete
                                </button>
                                {/* Placeholder for future "View" button */}
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}
        </section>

    );
}