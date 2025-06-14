from google.adk import AgentResult, ConditionalAgent, InvocationContext, Orchestrator

from agents.rewriter_agent import rewriter_agent


def should_rewrite(ctx: InvocationContext) -> bool:
    verdict = ctx.session.state.get("verdict")
    return verdict in ["Needs Refactor", "Reject"]


conditional_rewriter_agent = ConditionalAgent(
    name="conditional_rewriter_agent",
    agent=rewriter_agent,
    condition=should_rewrite,
)


class CodeCourtroomOrchestrator(Orchestrator):
    async def run(self, ctx: InvocationContext) -> AgentResult:
        (
            compliance_output,
            optimization_output,
            prosecutor_output,
        ) = await ctx.invoke_tools_parallel(
            [
                ("compliance_agent", ctx.user_input),
                ("optimizer_agent", ctx.user_input),
                ("prosecutor_agent", ctx.user_input),
            ]
        )

        defendant_input = {
            "code": ctx.user_input["code"],
            "prosecutor_findings": prosecutor_output,
            "intent": ctx.user_input.get("intent", ""),
        }

        defendant_output = await ctx.invoke_tool("defendant_agent", defendant_input)

        judge_input = {
            "code": ctx.user_input["code"],
            "intent": ctx.user_input.get("intent", ""),
            "prosecutor_findings": prosecutor_output,
            "defense_response": defendant_output,
            "compliance_report": compliance_output,
            "optimization_suggestions": optimization_output,
        }

        judge_output = await ctx.invoke_tool("judge_agent", judge_input)

        ctx.session.state["verdict"] = judge_output.get("verdict")

        rewriter_result = await conditional_rewriter_agent.run_async(ctx)

        return judge_output and rewriter_result if rewriter_result else judge_output
