class Ticket:
    def __init__(self,name:str,amount:float):
        self.name = name
        self.amount = amount

ticket = Ticket("Sowmya",18000.00)
print(ticket.name)