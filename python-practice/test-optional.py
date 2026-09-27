def find_user(user_id: int) -> str | None:
    if user_id == 1:
        return "Sowmya"
    return None

print(f"username: {find_user(1)}")