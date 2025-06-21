from google.adk.agents import ParallelAgent, SequentialAgent

# Import individual agents
from .compliance_agent.agent import compliance_agent
from .defendant_agent.agent import defendant_agent
from .judge_agent.agent import judge_agent
from .optimizer_agent.agent import optimizer_agent
from .prosecutor_agent.agent import prosecutor_agent
from .rewriter_agent.agent import rewriter_agent

# First phase: Parallel analysis by prosecutor, compliance, and optimizer
parallel_analysis = ParallelAgent(
    name="ParallelAnalysis",
    sub_agents=[prosecutor_agent, compliance_agent, optimizer_agent],
    description="Conducts parallel analysis of the code by Prosecutor, Compliance Officer, and Optimization Expert.",
)

# Second phase: Defendant responds to all accusations
defense_phase = defendant_agent

# Third phase: Judge evaluates all evidence and renders verdict
judgment_phase = judge_agent

# Fourth phase: Rewriter implements judge's verdict if needed
implementation_phase = rewriter_agent

# Complete courtroom workflow
code_courtroom_agent = SequentialAgent(
    name="CodeCourtroomAgent",
    sub_agents=[parallel_analysis, defense_phase, judgment_phase, implementation_phase],
    description="Executes the complete code courtroom workflow: parallel analysis, defense, judgment, and implementation.",
)

root_agent = code_courtroom_agent
