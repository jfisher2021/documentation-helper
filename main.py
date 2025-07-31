from backend.core import run_llm
import streamlit as st

st.header("LangChain Documentation Helper")

prompt = st.chat_input("Enter your query here:")
if (
    "user_prompt_history" not in st.session_state and
    "chat_answer_history" not in st.session_state and
    "chat_history" not in st.session_state
):
    st.session_state.user_prompt_history = []
    st.session_state.chat_answer_history = []
    st.session_state.chat_history = []



if prompt:

    with st.spinner("Processing your query..."):
        response = run_llm(prompt, chat_history=st.session_state.chat_history)
        sources = set([doc.metadata["source"] for doc in response["context"]])
        formatted_response = (
            f"{response['answer']}\n\nSources: {', '.join(sources)}"
        )
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answer_history.append(formatted_response)
        st.session_state.chat_history.append(("human", prompt))
        st.session_state.chat_history.append(("assistant", response["answer"]))

if st.session_state.user_prompt_history and st.session_state.chat_answer_history:
    st.write("### Conversation History")
    for user_prompt, chat_answer in zip(st.session_state.user_prompt_history, st.session_state.chat_answer_history):
        st.chat_message("user").write(user_prompt)
        st.chat_message("assistant").write(chat_answer)

# def main():
#     print("LangChain Documentation Helper")
#     chat_history = []
#     user_prompt_history = []
#     chat_answer_history = []

#     while True:
#         prompt = input("Enter your query here (or type 'exit' to quit): ")
#         if prompt.lower() == "exit":
#             break

#         response = run_llm(prompt, chat_history=chat_history)
#         sources = set([doc.metadata["source"] for doc in response["context"]])
#         formatted_response = (
#             f"{response['answer']}\n\nSources: {', '.join(sources)}"
#         )
#         user_prompt_history.append(prompt)
#         chat_answer_history.append(formatted_response)
#         chat_history.append(("human", prompt))
#         chat_history.append(("assistant", formatted_response["answer"]))

#         print("\nAssistant:", formatted_response)
#         print("\nConversation History:")
#         for user_prompt, chat_answer in zip(user_prompt_history, chat_answer_history):
#             print(f"User: {user_prompt}")
#             print(f"Assistant: {chat_answer}\n")

# if __name__ == "__main__":
#     main()
