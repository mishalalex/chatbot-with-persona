import uuid
from checkpointer import get_mongo_checkpointer
from langgraph_flow import build_graph
from utils import format_user_input

def main() -> None:
    print("🤖  Chatbot started. Type 'exit' or 'bye' to quit.\n")

    thread_id = input("Enter session ID (or press Enter to start new): ").strip()
    if not thread_id:
        thread_id = str(uuid.uuid4())
        print(f"📌  New session ID: {thread_id}")

    cfg = {"configurable": {"thread_id": thread_id}}   # <- ONE canonical config

    checkpointer = get_mongo_checkpointer()
    chat_graph  = build_graph(checkpointer)

    # ---------- load prior state (if any) ----------
    try:
        snapshot = chat_graph.get_state(cfg)           # <- pass the config dict
        if snapshot is not None and snapshot.values:
            state = snapshot.values                    # last saved state
            print("🔄  Resuming previous session.")
        else:
            raise ValueError("empty snapshot")
    except Exception:
        print("🆕  Starting fresh session.")
        state = {"messages": []}

    # -------------- chat loop -----------------------
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "bye"}:
            print("👋  Goodbye!")
            break

        state["messages"].append(format_user_input(user_input))
        state = chat_graph.invoke(state, config=cfg)   # <- same config each turn

if __name__ == "__main__":
    main()

# test session id - 3e017623-c569-4313-b42c-4a00b8d2853f
