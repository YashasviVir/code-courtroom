import AgentAvatar from "@/components/AgentAvatar";
import CodeInput from "@/components/CodeInput";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

interface Agent {
  id: string;
  name: string;
  role: string;
  image: string;
  responses: string[];
  isActive: boolean;
}

const Index = () => {
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: "judge_agent",
      name: "Judge AI",
      role: "Presiding Judge",
      image:
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=400&fit=crop&crop=face",
      responses: [],
      isActive: false,
    },
    {
      id: "prosecutor_agent",
      name: "Prosecutor AI",
      role: "Code Prosecutor",
      image:
        "https://images.unsplash.com/photo-1581090464777-f3220bbe1b8b?w=400&h=400&fit=crop&crop=face",
      responses: [],
      isActive: false,
    },
    {
      id: "defendant_agent",
      name: "Defendant AI",
      role: "Code Defender",
      image:
        "https://images.unsplash.com/photo-1501286353178-1ec881214838?w=400&h=400&fit=crop&crop=face",
      responses: [],
      isActive: false,
    },
    {
      id: "compliance_agent",
      name: "Compliance AI",
      role: "Compliance Officer",
      image:
        "https://images.unsplash.com/photo-1487252665478-49b61b47f302?w=400&h=400&fit=crop&crop=face",
      responses: [],
      isActive: false,
    },
    {
      id: "optimizer_agent",
      name: "Optimizer AI",
      role: "Code Optimizer",
      image:
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=400&fit=crop&crop=face",
      responses: [],
      isActive: false,
    },
    {
      id: "rewriter_agent",
      name: "Rewriter AI",
      role: "Code Rewriter",
      image:
        "https://images.unsplash.com/photo-1581090464777-f3220bbe1b8b?w=400&h=400&fit=crop&crop=face",
      responses: [],
      isActive: false,
    },
  ]);

  const judgeAgent = agents.find((agent) => agent.id === "judge_agent");
  const leftSideAgents = agents.filter((agent) =>
    ["prosecutor_agent", "compliance_agent", "optimizer_agent"].includes(
      agent.id
    )
  );
  const defendantAgent = agents.find((agent) => agent.id === "defendant_agent");
  const rewriterAgent = agents.find((agent) => agent.id === "rewriter_agent");

  async function handleCodeSubmit(code: string) {
    setIsProcessing(true);

    // Reset agent responses and set initial isActive for first group
    setAgents((prev) =>
      prev.map((agent) => {
        if (
          ["prosecutor_agent", "compliance_agent", "optimizer_agent"].includes(
            agent.id
          )
        ) {
          return { ...agent, responses: [], isActive: true };
        }
        return { ...agent, responses: [], isActive: false };
      })
    );

    // Track which phase we're in
    let phase = 1; // 1: prosecution, 2: defense, 3: judge/rewriter
    const prosecutionAgents = [
      "prosecutor_agent",
      "compliance_agent",
      "optimizer_agent",
    ];
    let prosecutionDone = new Set<string>();

    try {
      const response = await fetch(
        "https://code-courtroom-90195122572.us-central1.run.app/stream_query",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: "user_123", // Replace with actual user id
            message: code,
          }),
        }
      );

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        let lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const { agent, text } = JSON.parse(line);

            setAgents((prev) => {
              // PHASE 1: prosecution agents
              if (phase === 1 && prosecutionAgents.includes(agent)) {
                prosecutionDone.add(agent);
                // If all prosecution agents have responded, move to phase 2
                if (prosecutionDone.size === prosecutionAgents.length) {
                  phase = 2;
                  // Mark only defendant_agent as active, all others inactive
                  return prev.map((a) =>
                    a.id === "defendant_agent"
                      ? {
                          ...a,
                          responses:
                            a.id === agent
                              ? [...a.responses, text]
                              : a.responses,
                          isActive: true,
                        }
                      : {
                          ...a,
                          responses:
                            a.id === agent
                              ? [...a.responses, text]
                              : a.responses,
                          isActive: false,
                        }
                  );
                }
                // Otherwise, keep prosecution agents active
                return prev.map((a) =>
                  prosecutionAgents.includes(a.id)
                    ? {
                        ...a,
                        responses:
                          a.id === agent ? [...a.responses, text] : a.responses,
                        isActive: true,
                      }
                    : {
                        ...a,
                        responses:
                          a.id === agent ? [...a.responses, text] : a.responses,
                        isActive: false,
                      }
                );
              }
              // PHASE 2: defendant agent
              if (phase === 2 && agent === "defendant_agent") {
                phase = 3;
                return prev.map((a) =>
                  a.id === "defendant_agent"
                    ? {
                        ...a,
                        responses: [...a.responses, text],
                        isActive: false,
                      }
                    : ["judge_agent", "rewriter_agent"].includes(a.id)
                    ? { ...a, responses: a.responses, isActive: true }
                    : { ...a, responses: a.responses, isActive: false }
                );
              }
              // PHASE 3: judge and rewriter
              if (
                phase === 3 &&
                ["judge_agent", "rewriter_agent"].includes(agent)
              ) {
                return prev.map((a) =>
                  a.id === agent
                    ? {
                        ...a,
                        responses: [...a.responses, text],
                        isActive: true,
                      }
                    : { ...a, responses: a.responses, isActive: false }
                );
              }
              // Default: just append response
              return prev.map((a) =>
                a.id === agent ? { ...a, responses: [...a.responses, text] } : a
              );
            });
          } catch (e) {
            // Optionally handle JSON parse errors
          }
        }
      }
    } catch (err) {
      // Optionally handle fetch errors
    } finally {
      setIsProcessing(false);
    }
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-amber-900 via-orange-900 to-red-900 p-2">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-3">
          <h1 className="text-2xl font-bold text-amber-100 mb-1">
            CODE COURTROOM
          </h1>
          <p className="text-amber-200 text-xs">
            Multi-Agent Code Review System
          </p>
        </div>

        {/* Judge Section - Top */}
        <div className="flex justify-center mb-3">
          <div className="bg-amber-950/80 rounded-lg p-3 shadow-xl border border-amber-700/50 backdrop-blur-xs">
            {judgeAgent && (
              <div className="flex items-center space-x-4">
                <AgentAvatar
                  name={judgeAgent.name}
                  role={judgeAgent.role}
                  image={judgeAgent.image}
                  isActive={judgeAgent.isActive}
                />
                {/* Show judge responses here */}
                <div
                  className="ml-4 text-amber-100 text-sm max-w-xl text-left overflow-y-auto"
                  style={{ maxHeight: "12rem" }}
                >
                  {judgeAgent.responses.length > 0 ? (
                    judgeAgent.responses.map((resp, idx) => (
                      <div key={idx} className="mb-1 whitespace-pre-line">
                        <ReactMarkdown>{resp}</ReactMarkdown>
                      </div>
                    ))
                  ) : (
                    <span className="italic text-amber-400">
                      No response yet.
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Main Courtroom Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mb-3">
          {/* Left Side - Prosecution */}
          <div className="space-y-2">
            <h2 className="text-sm font-semibold text-amber-200 text-center">
              Prosecution Side
            </h2>
            {leftSideAgents.map((agent) => (
              <div
                key={agent.id}
                className="bg-amber-950/70 rounded-lg p-2 shadow-lg border border-amber-700/30 backdrop-blur-xs"
              >
                <div className="flex items-center space-x-3">
                  <AgentAvatar
                    name={agent.name}
                    role={agent.role}
                    image={agent.image}
                    isActive={agent.isActive}
                  />
                  {/* Show agent responses here */}
                  <div
                    className="ml-3 text-amber-100 text-sm max-w-md text-left overflow-y-auto"
                    style={{ maxHeight: "12rem" }}
                  >
                    {agent.responses.length > 0 ? (
                      agent.responses.map((resp, idx) => (
                        <div key={idx} className="mb-1 whitespace-pre-line">
                          <ReactMarkdown>{resp}</ReactMarkdown>
                        </div>
                      ))
                    ) : (
                      <span className="italic text-amber-400">
                        No response yet.
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Right Side - Defense */}
          <div className="space-y-2">
            <h2 className="text-sm font-semibold text-amber-200 text-center">
              Defense Side
            </h2>

            {/* Defendant Agent */}
            {defendantAgent && (
              <div className="bg-amber-950/70 rounded-lg p-2 shadow-lg border border-amber-700/30 backdrop-blur-xs">
                <div className="flex items-center space-x-3">
                  <AgentAvatar
                    name={defendantAgent.name}
                    role={defendantAgent.role}
                    image={defendantAgent.image}
                    isActive={defendantAgent.isActive}
                  />
                  {/* Show defendant responses here */}
                  <div
                    className="ml-3 text-amber-100 text-sm max-w-md text-left overflow-y-auto"
                    style={{ maxHeight: "12rem" }}
                  >
                    {defendantAgent.responses.length > 0 ? (
                      defendantAgent.responses.map((resp, idx) => (
                        <div key={idx} className="mb-1 whitespace-pre-line">
                          <ReactMarkdown>{resp}</ReactMarkdown>
                        </div>
                      ))
                    ) : (
                      <span className="italic text-amber-400">
                        No response yet.
                      </span>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Rewriter Agent */}
            {rewriterAgent && (
              <div className="bg-amber-950/70 rounded-lg p-2 shadow-lg border border-amber-700/30 backdrop-blur-xs">
                <div className="flex items-center space-x-3">
                  <AgentAvatar
                    name={rewriterAgent.name}
                    role={rewriterAgent.role}
                    image={rewriterAgent.image}
                    isActive={rewriterAgent.isActive}
                  />
                  {/* Show rewriter responses here */}
                  <div
                    className="ml-3 text-amber-100 text-sm max-w-md text-left overflow-y-auto"
                    style={{ maxHeight: "12rem" }}
                  >
                    {rewriterAgent.responses.length > 0 ? (
                      rewriterAgent.responses.map((resp, idx) => (
                        <div key={idx} className="mb-1 whitespace-pre-line">
                          <ReactMarkdown>{resp}</ReactMarkdown>
                        </div>
                      ))
                    ) : (
                      <span className="italic text-amber-400">
                        No response yet.
                      </span>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Code Input - Full Width at Bottom */}
        <div className="w-full mb-2">
          <CodeInput onSubmit={handleCodeSubmit} isProcessing={isProcessing} />
        </div>

        {/* Footer */}
        <div className="text-center text-amber-300 text-xs">
          <p>
            Submit your code for comprehensive AI-powered review and analysis
          </p>
        </div>
      </div>
    </div>
  );
};

export default Index;
