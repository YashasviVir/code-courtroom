from google.adk import AgentResult, InvocationContext, Orchestrator


class CodeCourtroomOrchestrator(Orchestrator):
    async def run(self, ctx: InvocationContext) -> AgentResult:
        prosecutor_output = await ctx.invoke_tool("prosecutor_agent", ctx.user_input)
        defendant_input = {
            "code": ctx.user_input["code"],
            "prosecutor_findings": prosecutor_output,
            "intent": ctx.user_input.get("intent", ""),
        }
        defendant_output = await ctx.invoke_tool("defendant_agent", defendant_input)

        compliance_output, optimization_output = await ctx.invoke_tools_parallel(
            [("compliance_agent", ctx.user_input), ("optimizer_agent", ctx.user_input)]
        )

        judge_input = {
            "code": ctx.user_input["code"],
            "intent": ctx.user_input.get("intent", ""),
            "prosecutor_findings": prosecutor_output,
            "defense_response": defendant_output,
            "compliance_report": compliance_output,
            "optimization_suggestions": optimization_output,
        }

        judge_output = await ctx.invoke_tool("judge_agent", judge_input)
        return judge_output
