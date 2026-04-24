def get_agent(message: str):
    message = message.lower()

    if "price" in message or "buy" in message:
        return "sales"
    elif "problem" in message or "issue" in message:
        return "support"
    else:
        return "general"


def generate_reply(agent: str):
    if agent == "sales":
        return "Thanks for your interest. Can you share what you are looking for?"
    elif agent == "support":
        return "Sorry you are facing this issue. Can you describe it a bit more?"
    else:
        return "Happy to help. What would you like to know?"