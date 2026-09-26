from enum import Enum

class Priority(Enum):
    LOW = "low",
    HIGH = "high"

def summarize_tickets(*tickets,priority:Priority = Priority.LOW):
    urgent_only = [t for t in tickets if t.get("urgent")]    
    print(f"Priority: {priority}  urgent_count: {len(urgent_only)}")

summarize_tickets({"name":"akshara","urgent":True},{"name":"pranav","urgent":True},priority = Priority.HIGH)