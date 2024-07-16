import gradio as gr
from src.backend.core import transcribe_audio, synthesize_speech, process_image

custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
.primary-btn {
    background-color: #3498db;
    color: white;
}
.secondary-btn {
    background-color: #2ecc71;
    color: white;
}
"""

def transcribe_with_progress(audio):
    progress = gr.Progress()
    for i in range(100):
        progress(i/100, desc="Transcribing")
        # Simulate work
    return transcribe_audio(audio)

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# Artificial Me Intelligence")
    
    with gr.Tab("Audio Processing"):
        audio_input = gr.Audio(type="filepath", label="Upload Audio")
        transcribe_button = gr.Button("Transcribe")
        transcription_output = gr.Textbox(label="Transcription Result")
        transcribe_button.click(transcribe_with_progress, inputs=audio_input, outputs=transcription_output)
        
        synthesize_button = gr.Button("Synthesize Speech")
        synthesized_audio_output = gr.Audio(label="Synthesized Audio")
        synthesize_button.click(synthesize_speech, inputs=transcription_output, outputs=synthesized_audio_output)
        
    with gr.Tab("Image Processing"):
        image_input = gr.Image(type="filepath", label="Upload Image")
        process_button = gr.Button("Process Image")
        image_output = gr.Image(label="Processed Image")
        process_button.click(process_image, inputs=image_input, outputs=image_output)

    with gr.Tab("Chat"):
        chat_input = gr.Textbox(label="Your Message")
        chat_output = gr.Chatbox(label="Chat History")
        chat_button = gr.Button("Send")
        chat_button.click(
            chat_history,
            inputs=[chat_input, chat_output],
            outputs=[chat_output, chat_input],
        )
        chat_input.change(
            chat_history,
            inputs=[chat_input, chat_output],
            outputs=[chat_output, chat_input],
        )

    with gr.Tab("Profile"):
        profile_input = gr.Textbox(label="Name")
        profile_input_email = gr.Textbox(label="Email")
        profile_input_preferences = gr.Textbox(label="Preferences")
        profile_button = gr.Button("Update Profile")
        profile_button.click(
            update_profile,
            inputs=[profile_input, profile_input_email, profile_input_preferences],
            outputs=[],
        )

    with gr.Tab("Chat History"):
        chat_history_input = gr.Textbox(label="Search Query")
        chat_history_button = gr.Button("Search")
        chat_history_output = gr.Textbox(label="Chat History")
        chat_history_button.click(
            search_messages,
            inputs=[chat_history_input],
            outputs=[chat_history_output],
        )
        chat_history_input.change(
            search_messages,
            inputs=[chat_history_input],
            outputs=[chat_history_output],
        )
        export_button = gr.Button("Export Chat History")
        export_button.click(export_chat_history, inputs=[], outputs=[])

    with gr.Tab("Register"):
        register_input_username = gr.Textbox(label="Username")
        register_input_password = gr.Textbox(label="Password", type="password")
        register_button = gr.Button("Register")
        register_button.click(
            register_user,
            inputs=[register_input_username, register_input_password],
            outputs=[],
        )

    with gr.Tab("Login"):
        login_input_username = gr.Textbox(label="Username")
        login_input_password = gr.Textbox(label="Password", type="password")
        login_button = gr.Button("Login")
        login_button.click(
            authenticate_user,
            inputs=[login_input_username, login_input_password],
            outputs=[],
        )

demo.launch()