import asyncio
import json
from .qwen_client import ask_qwen

DISCLAIMER = (
    "These scenarios are AI-generated possibilities based on the information supplied. "
    "They are not guaranteed forecasts or professional advice."
)

def _extract_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("The model did not return a JSON object")
    return json.loads(text[start:end+1])

def demo_result(req):
    decision = req.decision
    context = req.context or "No additional context was supplied."
    return {
        "mode": "demo",
        "disclaimer": DISCLAIMER,
        "decision": decision,
        "agent_insights": [
            {
                "agent": "People Impact Agent",
                "summary": "Examines how the decision may affect the people involved.",
                "benefits": ["May improve satisfaction if the change matches people's needs",
                             "Creates an opportunity to collect feedback and adapt"],
                "concerns": ["Different groups may experience the change differently",
                             "Communication and accessibility need attention"],
                "assumptions": ["People have a way to share feedback", context]
            },
            {
                "agent": "Operations & Cost Agent",
                "summary": "Checks practical delivery, resources, time and cost implications.",
                "benefits": ["A pilot can reveal operational efficiencies",
                             "Clear ownership can make implementation easier"],
                "concerns": ["Transition may require training or schedule changes",
                             "Hidden costs may appear during implementation"],
                "assumptions": ["A limited pilot is possible", "Resources can be measured"]
            },
            {
                "agent": "Risk & Opportunity Agent",
                "summary": "Identifies uncertainties, failure modes and possible upside.",
                "benefits": ["A controlled experiment can reduce uncertainty",
                             "Success may create a repeatable model"],
                "concerns": ["Unexpected side effects may emerge",
                             "Results may differ across departments or groups"],
                "assumptions": ["Baseline performance can be recorded",
                               "The decision can be reviewed at a checkpoint"]
            }
        ],
        "scenarios": [
            {
                "name": "Best case",
                "likelihood_label": "Optimistic possibility",
                "description": "The change is well planned, accepted by key groups and supported with enough resources.",
                "impacts": ["Strong adoption", "Measurable improvement against the baseline"],
                "risks": ["Overconfidence may lead to scaling too quickly"],
                "opportunities": ["Expand the pilot after results are independently reviewed"]
            },
            {
                "name": "Most likely",
                "likelihood_label": "Working baseline",
                "description": "The change produces mixed results: some benefits appear, while teams need time to adjust.",
                "impacts": ["Partial adoption", "Some processes need refinement"],
                "risks": ["Uneven outcomes", "Short-term disruption during transition"],
                "opportunities": ["Use feedback to improve the design before wider rollout"]
            },
            {
                "name": "Worst case",
                "likelihood_label": "Downside possibility",
                "description": "The change is introduced without sufficient preparation, creating friction and failing to meet its goals.",
                "impacts": ["Low adoption", "Service or productivity disruption"],
                "risks": ["Unplanned costs", "Loss of trust if concerns are ignored"],
                "opportunities": ["Pause, learn from the pilot and revert or redesign"]
            }
        ],
        "recommendations": [
            "Run a small, time-limited pilot before making the change permanent.",
            "Record baseline metrics so outcomes can be compared fairly.",
            "Collect feedback from every affected group, not only decision-makers.",
            "Set review checkpoints and define in advance when to continue, change or stop."
        ],
        "key_assumptions": [
            "The information supplied is accurate and sufficiently representative.",
            "External conditions remain broadly stable during the selected time horizon.",
            "The decision can be monitored and adjusted."
        ],
        "confidence": "Low — demo mode uses a generic framework, not live Qwen analysis."
    }

async def run_simulation(req):
    context = req.context or "Not provided"
    prompt_base = (
        f"Decision: {req.decision}\nContext: {context}\n"
        f"Time horizon: {req.time_horizon}\nConstraints: {req.constraints or 'Not provided'}"
    )
    agent_specs = [
        ("People Impact Agent",
         "You are a careful people-impact analyst. Assess stakeholders, accessibility, adoption, "
         "fairness and wellbeing. Return ONLY valid JSON with keys summary (string), benefits (array "
         "of strings), concerns (array), assumptions (array). Avoid unsupported certainty."),
        ("Operations & Cost Agent",
         "You are an operations and cost analyst. Assess resources, implementation, dependencies, "
         "time and cost drivers. Return ONLY valid JSON with keys summary, benefits, concerns, assumptions. "
         "Do not invent numeric costs."),
        ("Risk & Opportunity Agent",
         "You are a risk analyst. Identify uncertainties, failure modes, mitigations and upside. "
         "Return ONLY valid JSON with keys summary, benefits, concerns, assumptions. Do not claim certainty.")
    ]

    async def one_agent(name, system):
        raw = await ask_qwen(system, prompt_base)
        data = _extract_json(raw)
        return {"agent": name, **data}

    insights = await asyncio.gather(*(one_agent(n, s) for n, s in agent_specs))
    synthesis_system = (
        "You are a decision-simulation synthesizer. Use the three agent analyses to produce "
        "three plausible scenarios, not predictions. Return ONLY valid JSON with exactly these keys: "
        "scenarios (array of 3 objects, each with name, likelihood_label, description, impacts (array), "
        "risks (array), opportunities (array)); recommendations (array of strings); "
        "key_assumptions (array of strings); confidence (string). "
        "Scenario names must be Best case, Most likely, Worst case. Do not invent statistics."
    )
    synthesis_user = json.dumps({
        "decision": req.decision,
        "time_horizon": req.time_horizon,
        "constraints": req.constraints,
        "agent_insights": insights
    }, ensure_ascii=False)
    synthesized = _extract_json(await ask_qwen(synthesis_system, synthesis_user))
    return {
        "mode": "qwen",
        "disclaimer": DISCLAIMER,
        "decision": req.decision,
        "agent_insights": insights,
        **synthesized
    }
