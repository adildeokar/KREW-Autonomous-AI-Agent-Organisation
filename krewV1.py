import streamlit as st
import openai
import time
from typing import List, Dict, Any

# --- Page Configuration ---
st.set_page_config(
    page_title="Krew By Adil and Azhaan  🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Agent Classes (Adapted for Streamlit) ---
# Note: The core logic remains the same, but print statements are removed
# as output will be handled by the Streamlit UI.

class Agent:
    """The base class for all agents in the system."""

    def __init__(self, role: str, goal: str, model: str = "gpt-4o-mini", api_key: str = None):
        self.role = role
        self.goal = goal
        self.model = model
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = openai.OpenAI(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        """Generates a response from the OpenAI API."""
        messages = [
            {"role": "system", "content": f"You are a {self.role}. Your goal is to {self.goal}."},
            {"role": "user", "content": prompt}
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"An error occurred with the OpenAI API: {e}")
            return f"Error: Could not generate response. Details: {e}"


class Employee(Agent):
    """The Employee agent, responsible for executing tasks."""

    def __init__(self, role: str, goal: str, api_key: str):
        super().__init__(role, goal, api_key=api_key)


class Manager(Agent):
    """The Manager agent, orchestrating the work of Employee agents."""

    def __init__(self, employees: List[Employee], api_key: str):
        super().__init__(
            role="Project Manager",
            goal="Break down user requests into actionable tasks for employees and synthesize their work into a final presentable result.",
            api_key=api_key
        )
        self.employees = employees

    def delegate_task(self, task: str):
        """
        Manages the entire workflow from task delegation to final synthesis.
        This function is a generator, yielding messages to be displayed in the UI.
        """
        yield {"sender": "Manager", "message": f"Received new task: \"{task}\". Breaking it down for the team.",
               "type": "info"}

        initial_prompt = self._create_initial_prompt(task)
        yield {"sender": "Manager",
               "message": f"Delegating to the team with the following prompt:\n\n---\n{initial_prompt}\n---",
               "type": "info"}

        # Run employee collaboration
        employee_output = self._run_employee_collaboration(initial_prompt)
        # The collaboration itself will yield messages, so we process them
        for item in employee_output:
            yield item
            # Extract the final answer if present
            if item.get("final_answer"):
                final_employee_output = item["final_answer"]
                break
        else:
            final_employee_output = "The team could not reach a final answer."

        yield {"sender": "Manager", "message": "Reviewing the team's work and preparing the final response.",
               "type": "info"}

        final_result = self._synthesize_result(task, final_employee_output)
        yield {"sender": "Manager", "message": final_result, "type": "final_result"}

    def _create_initial_prompt(self, task: str) -> str:
        """Creates the initial detailed prompt for the employees."""
        return f"""
        Team, we have a new task from the user: '{task}'.

        Here is the plan and your roles:
        - **Overall Goal:** Collaboratively work to address the user's request.
        - **Your Task:** As a team of specialists, you need to discuss, research, and create a comprehensive solution.
        - **Collaboration:** Please discuss the task, share your findings, and critique each other's work to refine the final output.
        - **Process:**
            1. Each of you should state your initial thoughts on the task.
            2. Share information and build on each other's ideas.
            3. When you all agree that the work is complete and of high quality, one of you MUST conclude your message with 'FINAL_ANSWER:' followed by the complete, final output. Only one agent should do this.

        Let's begin. The Lead Researcher should start the discussion.
        """

    def _run_employee_collaboration(self, initial_prompt: str):
        """Manages the conversation loop between employees, yielding messages."""
        shared_history = [{"role": "user", "content": initial_prompt}]

        # Limit turns to prevent infinite loops, adjustable in UI
        for _ in range(st.session_state.max_turns):
            for employee in self.employees:
                with st.spinner(f"{employee.role} is thinking..."):
                    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in shared_history])
                    employee_prompt = f"Here is the conversation so far:\n{history_str}\n\nYour turn, {employee.role}. What is your contribution? Remember the process and the 'FINAL_ANSWER:' format when the task is complete."

                    response = employee.generate_response(employee_prompt)

                    # Yield the employee's response to the UI
                    yield {"sender": employee.role, "message": response, "type": "message"}

                    shared_history.append({"role": employee.role, "content": response})

                    if "FINAL_ANSWER:" in response:
                        final_answer = response.split("FINAL_ANSWER:", 1)[1].strip()
                        yield {"sender": employee.role, "message": "The team has reached a final answer.",
                               "type": "info", "final_answer": final_answer}
                        return

        yield {"sender": "Manager", "message": "The team could not reach a final answer in the allotted time.",
               "type": "info", "final_answer": "The team could not reach a final answer in the allotted time."}

    def _synthesize_result(self, original_task: str, employee_output: str) -> str:
        """Synthesizes the employee output into a final response for the user."""
        synthesis_prompt = f"""
        The original user request was: '{original_task}'.

        My team of employees has produced the following result:
        ---
        {employee_output}
        ---
        Please review this result and format it into a clean, well-structured, and professional response to the user.
        The response should directly address the user's original request. Be comprehensive.
        """
        return self.generate_response(synthesis_prompt)


# --- Streamlit UI ---

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = [
        {"role": "Lead Researcher", "goal": "To find and provide the most relevant and up-to-date information."},
        {"role": "Creative Writer", "goal": "To draft compelling and clear text based on the research."},
        {"role": "Technical Analyst", "goal": "To analyze the technical aspects and feasibility of the task."},
        {"role": "Quality Assurance", "goal": "To review the work for accuracy, clarity, and completeness."},
        {"role": "Content Strategist",
         "goal": "To ensure the final output aligns with the overall goal and user's intent."}
    ]

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# --- Sidebar for Configuration ---
with st.sidebar:
    st.title("🛠️ Configuration")
    st.markdown("Configure the agents and settings for your autonomous company.")

    st.subheader("API Key")
    st.session_state.api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)
    if st.session_state.api_key.startswith("sk-"):
        st.success("API Key is set.")
    else:
        st.warning("Please enter your OpenAI API Key.")

    st.subheader("Company Settings")
    st.session_state.max_turns = st.slider("Max Conversation Turns", 5, 20, 10)

    st.subheader("Team Configuration")
    for i, agent in enumerate(st.session_state.agents):
        with st.expander(f"**{i + 1}. {agent['role']}**", expanded=False):
            st.session_state.agents[i]['role'] = st.text_input(f"Role {i + 1}", value=agent['role'], key=f"role_{i}")
            st.session_state.agents[i]['goal'] = st.text_area(f"Goal (Prompt) {i + 1}", value=agent['goal'],
                                                              key=f"goal_{i}", height=150)
            if st.button(f"Remove {agent['role']}", key=f"remove_{i}"):
                st.session_state.agents.pop(i)
                st.rerun()

    if st.button("Add New Agent"):
        st.session_state.agents.append({"role": "New Agent", "goal": "Define my purpose."})
        st.rerun()

# --- Main App Interface ---
st.title("🤖 Krew - The Autonomous AI Agent Organisation")            ###################################################################################
st.markdown("Enter a task and watch your configured team of AI agents collaborate to achieve the goal.")

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["sender"]):
        st.markdown(msg["message"])

# Input form for the user task
with st.form("task_form"):
    user_task = st.text_area("Enter your task for the company:", height=100)
    submitted = st.form_submit_button("🚀 Run Company")

if submitted:
    if not st.session_state.api_key.startswith("sk-"):
        st.error("Please enter a valid OpenAI API Key in the sidebar to begin.")
    elif not user_task:
        st.warning("Please enter a task for the company.")
    else:
        # Clear previous messages and start new run
        st.session_state.messages = []

        try:
            # Instantiate agents based on current config
            employees = [Employee(api_key=st.session_state.api_key, **agent_config) for agent_config in
                         st.session_state.agents]
            manager = Manager(employees, api_key=st.session_state.api_key)

            # Use a container for the chat history
            chat_container = st.container()

            # Run the delegation and display results as they come in
            for result in manager.delegate_task(user_task):
                st.session_state.messages.append(result)
                with chat_container:
                    with st.chat_message(result["sender"]):
                        st.markdown(result["message"])
                time.sleep(0.5)  # Small delay for better visual flow

        except Exception as e:
            st.error(f"A critical error occurred: {e}")

# Add a reset button
if len(st.session_state.messages) > 0:
    if st.button("🔄 Reset and Start New Task"):
        st.session_state.messages = []
        st.rerun()

