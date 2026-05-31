"use client";

import { useState } from "react";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://ragpulse-x7-ai-resume-screening-system.hf.space";

export default function ComparePage() {
  const [resumeA, setResumeA] = useState<File | null>(null);
  const [resumeB, setResumeB] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const compareCandidates = async () => {
    if (!resumeA || !resumeB) {
      alert("Upload 2 resumes");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("files", resumeA);
      formData.append("files", resumeB);
      formData.append("job_description", jobDescription);

      const response = await fetch(
        `${BACKEND_URL}/compare_candidates`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      console.log("COMPARE RESPONSE:", data);

      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Comparison failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#020817] text-white p-10">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-6xl font-black mb-10">
          Candidate Comparison
        </h1>

        <div className="flex gap-6 mb-6">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) =>
              setResumeA(e.target.files?.[0] || null)
            }
          />

          <input
            type="file"
            accept=".pdf"
            onChange={(e) =>
              setResumeB(e.target.files?.[0] || null)
            }
          />
        </div>

        <textarea
          value={jobDescription}
          onChange={(e) =>
            setJobDescription(e.target.value)
          }
          placeholder="Paste Job Description"
          className="w-full h-40 rounded-xl p-4 bg-white text-black border"
        />

        <button
          onClick={compareCandidates}
          disabled={loading}
          className="mt-6 px-6 py-3 bg-cyan-600 hover:bg-cyan-500 rounded-xl font-semibold disabled:opacity-50"
        >
          {loading
            ? "Comparing..."
            : "Compare Candidates"}
        </button>

        {result && (
          <div
            className="
              mt-10
              rounded-3xl
              border
              border-cyan-500/30
              bg-[#071028]
              p-8
              shadow-lg
            "
          >
            <div className="mb-6">
              <h2 className="text-3xl font-bold">
                🏆 Winner
              </h2>

              <div className="mt-3 p-4 rounded-xl bg-[#0B1736] border border-cyan-500">
                <p className="text-cyan-400 font-semibold break-all text-xl">
                  {result.winner}
                </p>
              </div>
            </div>

            <p className="text-xl mb-6">
              Winner Score: {result.winner_score}
            </p>

            <h3 className="text-2xl font-bold mb-4">
              Reasons
            </h3>

            <div className="space-y-2">
              {result.comparison_reasons?.map(
                (reason: string, index: number) => (
                  <p key={index}>
                    ✓ {reason}
                  </p>
                )
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}