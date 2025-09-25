"use client";
import { useState } from "react";

type SummaryBoxProps = {
    summary: string;
    formatChoice: string;
};

export default function SummaryBox({ summary, formatChoice }: SummaryBoxProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(summary);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <div className="flex justify-between items-center mb-2">
                <h2 className="text-lg font-semibold text-gray-800">Summary:</h2>
                <button
                    onClick={handleCopy}
                    className="text-sm px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
                >
                    {copied ? "✅ Copied!" : "📋 Copy"}
                </button>
            </div>

            {formatChoice === "bullets" ? (
                <ul className="list-disc pl-5 space-y-2 text-gray-700">
                    {summary
                        .split("\n")
                        .filter((line) => line.trim().length > 0)
                        .map((line, idx) => (
                            <li key={idx}>{line.replace(/^- /, "")}</li>
                        ))}
                </ul>
            ) : (
                <p className="whitespace-pre-wrap text-gray-700">{summary}</p>
            )}
        </div>
    );
}
