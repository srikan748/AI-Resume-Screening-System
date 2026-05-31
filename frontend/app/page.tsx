"use client";

import { useState } from "react";
import Link from "next/link";
const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://ragpulse-x7-ai-resume-screening-system.hf.space";

export default function Page() {
  const [files, setFiles] = useState<FileList | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const analyzeCandidates = async () => {
    if (!files || files.length === 0) {
      alert("Upload resumes");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    Array.from(files).forEach((file) => {
      formData.append("files", file);
    });
    formData.append("job_description", jobDescription);
    try {
      const response = await fetch(`${BACKEND_URL}/rank_candidates`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log(data);
      setCandidates(data.rankings || []);
    } catch (error) {
      console.error(error);
      alert("Backend error");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-[#020817] text-white px-6 py-8">
      <div className="max-w-6xl mx-auto">

        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold mb-1 text-cyan-400 tracking-tight">
            Enterprise AI Hiring Copilot
          </h1>
          <p className="text-sm text-gray-500 tracking-widest uppercase mt-2">
            LLM-Powered Resume Screening and Candidate Ranking
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          <div className="rounded-xl bg-[#071028] border border-cyan-500/20 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-widest mb-1">Candidates</p>
            <h3 className="text-2xl font-bold text-cyan-400">{candidates.length}</h3>
          </div>
          <div className="rounded-xl bg-[#071028] border border-green-500/20 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-widest mb-1">Strong Hire</p>
            <h3 className="text-2xl font-bold text-green-400">
              {candidates.filter((c) => c.recommendation === "Strong Hire").length}
            </h3>
          </div>
          <div className="rounded-xl bg-[#071028] border border-blue-500/20 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-widest mb-1">Hire</p>
            <h3 className="text-2xl font-bold text-blue-400">
              {candidates.filter((c) => c.recommendation === "Hire").length}
            </h3>
          </div>
          <div className="rounded-xl bg-[#071028] border border-red-500/20 p-4">
            <p className="text-gray-400 text-xs uppercase tracking-widest mb-1">Reject</p>
            <h3 className="text-2xl font-bold text-red-400">
              {candidates.filter((c) => c.recommendation === "Reject").length}
            </h3>
          </div>
        </div>

        <div className="rounded-2xl border border-cyan-500/20 bg-[#071028]/80 backdrop-blur-xl p-6 mb-8">
          <div className="border-2 border-dashed border-cyan-500/30 rounded-xl p-10 text-center mb-5">
            <input
              type="file"
              multiple
              accept=".pdf"
              onChange={(e) => setFiles(e.target.files)}
              className="mb-3 text-sm text-gray-400"
            />
            <p className="text-sm text-gray-500">Upload Resume PDFs</p>
          </div>

          <textarea
            placeholder="Paste Job Description Here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            className="w-full h-36 rounded-xl bg-[#020817] border border-cyan-500/15 p-4 text-sm text-white outline-none resize-none placeholder:text-gray-600"
          />

          <button
            onClick={analyzeCandidates}
            disabled={loading}
            className="w-full mt-4 py-3 rounded-xl bg-blue-600 text-sm font-semibold transition-all disabled:opacity-60"
          >
            {loading ? "Analyzing Candidates..." : "Analyze Candidates"}
          </button>
        </div>

        <div>
          {candidates.map((candidate: any, index: number) => (
            <div
              key={index}
              className="relative overflow-hidden rounded-2xl border border-cyan-500/20 bg-[#071028]/90 backdrop-blur-xl p-6 mb-5"
            >
              <div className="relative z-10">

                <div className="flex items-start gap-4 mb-5">
                  <div className="h-10 w-10 rounded-xl bg-blue-600 flex items-center justify-center text-sm font-bold flex-shrink-0">
                    #{index + 1}
                  </div>
                  <div>
                    {index === 0 && (
                      <div className="inline-block mb-2 px-3 py-1 rounded-full bg-yellow-500/15 border border-yellow-500/30 text-yellow-300 text-xs font-semibold">
                        Best Candidate
                      </div>
                    )}
                    <h2 className="text-base font-semibold text-gray-100 break-all leading-snug">
                      {candidate.filename}
                    </h2>
                    <p className="text-cyan-400 uppercase tracking-widest text-[10px] mt-0.5">
                      AI Candidate Evaluation
                    </p>
                  </div>
                </div>

                <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4 mb-4">
                  <div className="text-cyan-300 font-bold text-xl mb-2">
                    Final Score: {candidate.match_score}%
                  </div>
                  <div className="flex gap-6 text-xs text-gray-400">
                    <span>Semantic Score: {candidate.semantic_score ?? "N/A"}%</span>
                    <span>Skill Match: {candidate.skill_score ?? "N/A"}%</span>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-gray-500 uppercase tracking-widest text-[10px] mb-1">
                    Recommendation
                  </p>
                  <h3 className="text-xl font-bold">{candidate.recommendation}</h3>
                </div>

                <div className="mb-4">
                  <p className="text-gray-500 uppercase tracking-widest text-[10px] mb-2">
                    AI Recruiter Analysis
                  </p>
                  <div className="rounded-xl border border-cyan-500/15 bg-[#020817] p-4 text-xs text-gray-400 leading-relaxed whitespace-pre-wrap">
                    {candidate.analysis}
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4 mb-5">
                  <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-4">
                    <p className="text-green-400 font-semibold text-xs mb-3 uppercase tracking-wide">
                      Matched Skills
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {candidate.matched_skills?.map((skill: string, i: number) => (
                        <span
                          key={i}
                          className="px-3 py-1 rounded-full bg-green-500/15 text-green-300 border border-green-500/25 text-xs"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4">
                    <p className="text-red-400 font-semibold text-xs mb-3 uppercase tracking-wide">
                      Missing Skills
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {candidate.missing_skills?.map((skill: string, i: number) => (
                        <span
                          key={i}
                          className="px-3 py-1 rounded-full bg-red-500/15 text-red-300 border border-red-500/25 text-xs"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex gap-3 flex-wrap">
                  <button
                    onClick={() => window.open(`${BACKEND_URL}/resumes/${candidate.filename}`, "_blank")}
                    className="px-5 py-2 rounded-xl bg-blue-600 text-white text-xs font-semibold"
                  >
                    View Resume
                  </button>
                  <button
                    onClick={() => window.open(`${BACKEND_URL}/generate_report/${index}`, "_blank")}
                    className="px-5 py-2 rounded-xl border border-cyan-500/30 text-cyan-400 text-xs font-semibold"
                  >
                    Download Report
                  </button>
                </div>

              </div>
            </div>
          ))}
        </div>

      </div>
    </main>
  );
}