"use client";

import {useEffect, useState, useCallback} from "react";
import Script from "next/script";

const GOOGLE_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_API_KEY;
const API_URL = process.env.NEXT_PUBLIC_API_URL;

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

export default function DrivePickerPage() {
    const [gapiLoaded, setGapiLoaded] = useState(false);
    const [pickerReady, setPickerReady] = useState(false);
    const [accessToken, setAccessToken] = useState(null);
    const [lastSelection, setLastSelection] = useState(null);

    // const deleteFile = useCallback(() => {
    //     fetch(`${API_URL}/storage/delete/2ea65c65-31cd-4220-a4bf-5240f30a965e`, {
    //         method: "DELETE",
    //         credentials: "include",
    //         headers: {
    //             "Content-Type": "application/json",
    //             "X-CSRFToken": getCSRFToken(),
    //         },
    //     })
    //         .then(res => res.json())
    //         .then(console.log)
    //         .catch(console.error);
    // });

    const openPicker = useCallback(() => {
        if (!pickerReady) {
            console.warn("Picker is not ready yet");
            return;
        }
        if (!accessToken) {
            console.warn("No access token available");
            return;
        }
        if (!window.google || !window.google.picker) {
            console.warn("Google Picker is not available");
            return;
        }

        const view = new window.google.picker.DocsView()
            .setIncludeFolders(true)
            .setSelectFolderEnabled(true);

        const picker = new window.google.picker.PickerBuilder()
            .setDeveloperKey(GOOGLE_API_KEY)
            .setOAuthToken(accessToken)
            .addView(view)
            .setCallback((data) => {
                if (data.action === window.google.picker.Action.PICKED) {
                    const doc = data.docs[0];

                    fetch(`${API_URL}/storage/save/`, {
                        method: "POST",
                        credentials: "include",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCSRFToken(),
                        },
                        body: JSON.stringify({
                            id: doc.id,
                            name: doc.name,
                            mimeType: doc.mimeType,
                        })
                    })
                        .then(r => r.json())
                        .then(console.log)
                        .catch(console.error);

                    console.log("Picked file:", doc);
                    setLastSelection(doc);
                } else if (data.action === window.google.picker.Action.CANCEL) {
                    console.log("Picker cancelled");
                }
            })
            .build();

        picker.setVisible(true);
    }, [pickerReady, accessToken]);


    useEffect(() => {
        fetch(`${API_URL}/auth/retrieve-access-token`, {
            credentials: "include"
        })
            .then(res => res.json())
            .then(accessToken => setAccessToken(accessToken.access_token));
    }, []);

    useEffect(() => {
        if (!gapiLoaded) return;
        if (!window.gapi) return;

        window.gapi.load("client:picker", () => {
            console.log("gapi client & picker loaded");
            setPickerReady(true);
        });
    }, [gapiLoaded]);

    return (
        <>
            <Script
                src="https://apis.google.com/js/api.js"
                strategy="lazyOnload"
                onLoad={() => {
                    console.log("Google API script loaded");
                    setGapiLoaded(true);
                }}
            />

            <main style={{padding: "2rem", fontFamily: "system-ui, sans-serif"}}>
                <h1>Google Drive Picker Demo</h1>

                {/*<button*/}
                {/*    onClick={deleteFile}*/}
                {/*>*/}
                {/*    Delete File*/}
                {/*</button>*/}

                <div style={{marginTop: "1rem"}}>
                    <p>gapi loaded: {gapiLoaded ? "Yes" : "No"}</p>
                    <p>Picker ready: {pickerReady ? "Yes" : "No"}</p>
                    <p>Access token present: {accessToken ? "Yes" : "No"}</p>
                </div>

                <button
                    onClick={openPicker}
                    disabled={!pickerReady || !accessToken}
                    style={{
                        marginTop: "1rem",
                        padding: "0.5rem 1rem",
                        fontSize: "1rem",
                        cursor: !pickerReady || !accessToken ? "not-allowed" : "pointer",
                    }}
                >
                    Open Google Drive Picker
                </button>

                {lastSelection && (
                    <div style={{marginTop: "2rem"}}>
                        <h2>Last selection</h2>
                        <pre>{JSON.stringify(lastSelection, null, 2)}</pre>
                    </div>
                )}
            </main>
        </>
    );
}
