with open('src/agent/core/executive.py', 'r') as f:
    content = f.read()

content = content.replace('from src.agent.llm.gateway import ModelGateway', 'from src.agent.llm.gateway import ModelGateway\nfrom src.agent.core.config import settings')
content = content.replace('f"You are {self.identity.name}.', 'f"You are {self.identity.name if self.identity else \'\'}.')
content = content.replace('Purpose: {self.identity.purpose}', 'Purpose: {self.identity.purpose if self.identity else \'\'}')
content = content.replace("Directives: {', '.join(self.identity.core_directives)}", "Directives: {', '.join(self.identity.core_directives if self.identity else [])}")

with open('src/agent/core/executive.py', 'w') as f:
    f.write(content)
