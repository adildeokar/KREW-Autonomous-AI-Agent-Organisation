from typing import List, Dict, Any, Generator
from datetime import datetime
from openai import OpenAI
import uuid
import time

class Agent:
    def __init__(self, role: str, goal: str, model: str = "gpt-4o-mini", api_key: str = None, expertise: str = "", agent_id: str = None):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.role = role
        self.goal = goal
        self.model = model
        self.expertise = expertise
        self.agent_id = agent_id or str(uuid.uuid4())
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, context: str = "", file_content: str = "") -> str:
        sys = f"You are a {self.role} with expertise in {self.expertise}.\nPrimary goal: {self.goal}\n- Stay in character\n- Provide detailed, actionable insights\n- Reference file content when relevant\n- Build on other team members\n- Avoid generic responses\n"
        if file_content:
            sys += f"\nFile content:\n{file_content[:3000]}..."
        if context:
            sys += f"\nContext:\n{context[-2000:]}"
        resp = self.client.chat.completions.create(model=self.model, messages=[{"role": "system", "content": sys}, {"role": "user", "content": prompt}], temperature=0.7, max_tokens=1500)
        return resp.choices[0].message.content.strip()

class Employee(Agent):
    def __init__(self, role: str, goal: str, api_key: str, expertise: str = "", agent_id: str = None):
        super().__init__(role, goal, api_key=api_key, expertise=expertise, agent_id=agent_id)

class Manager(Agent):
    def __init__(self, employees: List[Employee], api_key: str, max_turns: int = 12):
        super().__init__(role="AI Organization Manager", goal="Orchestrate team collaboration and synthesize final results", api_key=api_key, expertise="Management, Planning, QA")
        self.employees = employees
        self.max_turns = max_turns

    def delegate_task(self, task: str, file_content: str = "", user_suggestions: str = "") -> Generator[Dict[str, Any], None, None]:
        yield {"sender": "Manager", "message": f"🎯 **New Mission**\n\nTask: *{task}*", "type": "manager", "timestamp": datetime.now().strftime("%H:%M:%S")}
        initial = self._build_brief(task, file_content, user_suggestions)
        yield {"sender": "Manager", "message": "📋 **Team Brief Issued**", "type": "manager", "timestamp": datetime.now().strftime("%H:%M:%S")}

        shared = initial
        min_rounds = 2
        total_agents = len(self.employees)

        yield {"sender": "Manager", "message": f"🔄 **Round-Robin Collaboration** with {total_agents} agents", "type": "manager", "timestamp": datetime.now().strftime("%H:%M:%S")}

        for r in range(min_rounds):
            yield {"sender": "Manager", "message": f"📋 **Round {r+1}/{min_rounds}**", "type": "manager", "timestamp": datetime.now().strftime("%H:%M:%S")}
            for e in self.employees:
                yield {"sender": "System", "message": f"🤔 {e.role} is preparing response...", "type": "thinking", "timestamp": datetime.now().strftime("%H:%M:%S")}
                if r == 0:
                    p = f"INITIAL ANALYSIS\n{shared[-2500:]}\nYour role: {e.role} ({e.expertise}). Provide first assessment, questions, and initial recommendations. Do not finalize."
                else:
                    p = f"BUILDING PHASE (Round {r+1})\n{shared[-2500:]}\nYour role: {e.role}. Build on others, refine or challenge, add concrete next steps. Do not conclude yet."
                ans = e.generate(p, context=shared, file_content=file_content)
                yield {"sender": e.role, "message": ans, "type": "agent", "timestamp": datetime.now().strftime("%H:%M:%S"), "agent_id": e.agent_id}
                shared += f"\n\n**{e.role} (R{r+1}):** {ans}"
                time.sleep(0.1)

        yield {"sender": "Manager", "message": "🎯 **Consensus Phase**", "type": "manager", "timestamp": datetime.now().strftime("%H:%M:%S")}
        turns_left = max(self.max_turns - min_rounds * total_agents, 1)
        idx = 0
        for _ in range(turns_left):
            e = self.employees[idx % total_agents]
            idx += 1
            yield {"sender": "System", "message": f"🤔 {e.role} working on consensus...", "type": "thinking", "timestamp": datetime.now().strftime("%H:%M:%S")}
            p = f"CONSENSUS BUILDING\n{shared[-3000:]}\nSynthesize all inputs. If ready, conclude with 'FINAL_ANSWER: ...' that addresses the original task comprehensively with actionable steps."
            ans = e.generate(p, context=shared, file_content=file_content)
            yield {"sender": e.role, "message": ans, "type": "agent", "timestamp": datetime.now().strftime("%H:%M:%S"), "agent_id": e.agent_id}
            shared += f"\n\n**{e.role} (Consensus):** {ans}"
            if "FINAL_ANSWER:" in ans:
                final_answer = ans.split("FINAL_ANSWER:", 1)[1].strip()
                yield {"sender": e.role, "message": "✅ **Final solution synthesized**", "type": "completion", "timestamp": datetime.now().strftime("%H:%M:%S"), "final_answer": final_answer}
                break
            time.sleep(0.1)

        final = self._synthesize(task, shared, file_content)
        yield {"sender": "Manager", "message": "🔍 **Final Review & Synthesis**", "type": "manager", "timestamp": datetime.now().strftime("%H:%M:%S")}
        yield {"sender": "Manager", "message": final, "type": "final_result", "timestamp": datetime.now().strftime("%H:%M:%S"), "task_complete": True}

    def _build_brief(self, task: str, file_content: str, usr: str) -> str:
        team = "\n".join([f"- {e.role}: {e.expertise}" for e in self.employees])
        brief = f"TEAM BRIEF\nOBJECTIVE: {task}\nTEAM:\n{team}\n"
        if file_content:
            brief += f"\nFILES PREVIEW:\n{file_content[:500]}...\n"
        if usr:
            brief += f"\nUSER NOTES:\n{usr}\n"
        brief += "\nSTANDARDS: specific, actionable, collaborative, comprehensive.\n"
        return brief

    def _synthesize(self, task: str, team_output: str, file_content: str) -> str:
        p = f"EXECUTIVE SYNTHESIS\nOriginal Task: {task}\nTeam Output:\n{team_output[-3500:]}"
        return self.generate(p, context=team_output, file_content=file_content)
