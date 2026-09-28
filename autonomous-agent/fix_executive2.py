with open('src/agent/core/executive.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "logger.info(f\"LLM Response:" in line:
        new_lines.append(line)
    else:
        new_lines.append(line.replace("self.identity.name", "self.identity.name if self.identity else 'Unknown'"))

with open('src/agent/core/executive.py', 'w') as f:
    f.writelines(new_lines)
