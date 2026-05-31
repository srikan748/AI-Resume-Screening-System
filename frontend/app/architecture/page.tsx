export default function ArchitecturePage() {
  return (
    <main className="min-h-screen bg-[#020817] text-white p-10">

      <div className="max-w-6xl mx-auto">

        <h1 className="text-5xl font-black text-center mb-12 bg-gradient-to-r from-cyan-400 to-blue-500 text-transparent bg-clip-text">
          AI Resume Screening System Architecture
        </h1>

        <div className="space-y-6">

          {[
            "📄 Resume PDFs",
            "📑 PyMuPDF Resume Parser",
            "🔍 Text Extraction",
            "🧠 Skill Extraction Engine",
            "📊 Sentence Transformer Embeddings",
            "🎯 Semantic Similarity Engine",
            "⚡ Skill Gap Analysis",
            "🏆 Candidate Ranking Engine",
            "🤖 AI Recruiter Analysis",
            "⚖️ Candidate Comparison",
            "📄 PDF Report Generator",
            "🚀 FastAPI Backend",
            "💻 Next.js Dashboard",
          ].map((step, index) => (
            <div
              key={index}
              className="flex flex-col items-center"
            >
              <div className="w-full max-w-3xl rounded-2xl bg-[#071028] border border-cyan-500/20 p-6 text-center text-xl font-semibold">
                {step}
              </div>

              {index !== 12 && (
                <div className="text-cyan-400 text-4xl my-2">
                  ↓
                </div>
              )}
            </div>
          ))}

        </div>

      </div>

    </main>
  );
}