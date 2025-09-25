"use client";

import { useState } from "react";
import FileUpload from "./components/FileUpload";
import FormatSelect from "./components/FormatSelect";
import SummaryBox from "./components/SummaryBox";
import Spinner from "./components/Spinner";

import { API_BASE_URL } from "../config";


export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [formatChoice, setFormatChoice] = useState("narrative");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    setLoading(true);
    setSummary("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE_URL}/api/summarize?format_choice=${formatChoice}`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setSummary(data.summary || "Error: " + JSON.stringify(data));
    } catch (error) {
      console.error(error);
      setSummary("Request failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-br from-blue-950 to-indigo-950">
      <div className="bg-stone-200 shadow-lg rounded-2xl p-8 w-full max-w-lg border border-gray-200 text-blue-950">
        <h1 className="text-3xl font-bold mb-6 text-center">Document Summarizer</h1>

        <FileUpload onFileSelect={setFile} />
        <FormatSelect value={formatChoice} onChange={setFormatChoice} />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-indigo-700 transition flex items-center justify-center"
        >
          {loading ? (
            <span className="flex items-center">
              <Spinner size={5} color="text-white" />
              Summarizing ...
            </span>
          ) : (
            "Upload & Summarize"
          )}
        </button>

        {summary && <SummaryBox summary={summary} formatChoice={formatChoice} />}
      </div>
    </main>
  );
}
