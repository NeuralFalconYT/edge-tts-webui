from microsoft_tts import edge_tts_pipeline
def tts(text,Language='English',Gender='Male',speed=1.0,translate_text_flag=False, no_silence=True, long_sentence=True):
    voice_name=None
    tts_save_path=''         
    edge_save_path = edge_tts_pipeline(text, Language,voice_name, Gender, translate_text_flag=translate_text_flag, 
                                        no_silence=no_silence, speed=speed, tts_save_path=tts_save_path, 
                                        long_sentence=long_sentence)
    return edge_save_path

# text="Machine learning is the study of computer "
# save_path = tts(text, Language='English',Gender="Male")
# print(save_path)
# import simpleaudio as sa
# def play_sound(filename):
#     wave_obj = sa.WaveObject.from_wave_file(filename)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()
# play_sound(save_path)

import gradio as gr
import click
from lang_data import languages
source_lang_list=['English','Hindi','Bengali']
source_lang_list.extend(languages.keys())
@click.command()
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode.")
@click.option("--share", is_flag=True, default=False, help="Enable sharing of the interface.")
def main(debug, share):
    description = """edge-tts GitHub [https://github.com/rany2/edge-tts]"""
    # Define Gradio inputs and outputs
    example=[["This is just beginning of the journey of AI, AI will take over the world soon",
            "English",
            "Female",
            1.0,
            False,
            False,
            True]]
    gradio_inputs = [
        gr.Textbox(label="Enter Text", lines=3,placeholder="Enter your text here..."),
        gr.Dropdown(label="Language", choices=source_lang_list, value="English"),
        gr.Dropdown(label="Gender", choices=['Male','Female'], value="Female"),
        gr.Number(label="Speed", value=1.0),
        gr.Checkbox(label="Translate Text", value=False),
        gr.Checkbox(label="Remove Silence", value=False),
        gr.Checkbox(label="Long Sentence", value=True)
    ]
    
    gradio_outputs = [
        gr.Audio(label="Audio File")
        # gr.File(label="Download Audio F", show_label=True)
    ]

    # Create Gradio interface
    demo = gr.Interface(fn=tts, inputs=gradio_inputs, outputs=gradio_outputs, title="Edge TTS ",examples=example,description=description)

    # Launch Gradio with command-line options
    demo.queue().launch(allowed_paths=[f"./audio"],debug=debug, share=share)
if __name__ == "__main__":
    main()
