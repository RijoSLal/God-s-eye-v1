from swarm import Swarm, Agent
from openai import OpenAI
import json
from rich.prompt import Prompt
from rich.console import Console
import tools
from collections import deque

console = Console()

class Friday:
    def __init__(self):
        
        """
        Initialize the agent by loading configuration, creating the
        OpenAI and Swarm clients, registering tool functions, instantiating
        the LLM agent, and preparing message history.
        """

        with open("config.json", "r") as f:
            self.file = json.loads(f.read())

        URL = self.file["url"]
        API_KEY = self.file["api_key"]

        self.open = OpenAI(base_url=URL, api_key=API_KEY)
        self.client = Swarm(client=self.open)

        function_collection = tools.TOOLS()
        self.functions = [
                function_collection.NMAP,
                function_collection.W_WEB,
                function_collection.CURL,
                function_collection.WSV_NIKTO,
                function_collection.OPENVS,
                function_collection.SSL_SCAN, 
                function_collection.CCV,
                function_collection.REPORT,
            ]
        
        self.LLM = Agent(
            name="God's Eye",
            instructions= self.file["system_prompt"],
            temperature= self.file["temperature"],
            functions=self.functions,
            model = self.file["model"]
        )

        self.history = 10
        self.messages = deque(maxlen=self.history)
    
    def add_conversation_exchange(self, role, content):

        """
        Add a single conversation entry to the message history.
        
        Args:
            role (str): Message role ("user" or "assistant").
            content (str): Message text.
        
        Returns:
            None
        """
       
        self.messages.append({"role": role, "content": content})
       
    def get_conversation_history(self):

        """
        Retrieve the current conversation history.
        
        Returns:
            list: List of message dictionaries in order.
        """

        return list(self.messages)
    
    def agent(self):

        """
        Start an interactive loop that sends user input to the LLM agent,
        receives responses, updates message history, and displays output.
        
        Returns:
            None
        """

        while True:
            user = Prompt.ask("[bold green]You [/bold green]")

            if user == "/bye":
                break

            self.add_conversation_exchange("user", user)
            response = self.client.run(
                agent=self.LLM,
                messages=self.get_conversation_history(),
                
            )
            llm_response = response.messages[-1]["content"]

            console.print(f"\n[bold blue]God's Eye :[/bold blue] {llm_response}\n")
            self.add_conversation_exchange("assistant", llm_response)


    def ping(self):

        """
        Send a small test request to verify that the model and credentials
        are functional.
        
        Returns:
            bool: True if the ping succeeds, False otherwise.
        """
        try:
            self.open.chat.completions.create(
                model=self.file["model"],
                messages=[
                    {"role": "user", "content": "Hi"}
                ],
                max_tokens=5
            )
            return True
        except Exception:
            return False
    
