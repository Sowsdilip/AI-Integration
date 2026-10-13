class TransientError(Exception):
    pass

def call_api(i: int):
    print(f"i value {i}")
    if i == 1:
        raise TransientError
    elif i == 2:
        raise TransientError
    elif i == 3:
       print("No Excpetion")
    elif i == 4:
        raise ValueError(" I cant be 4 ")
    
       
for i in range(1,5):
    try:
        print(f"i value {i}")
        call_api(i)
    except TransientError as e:
        print("TransientError")
    except ValueError as e:
        print("Value Error "+str(e))
        raise
      


