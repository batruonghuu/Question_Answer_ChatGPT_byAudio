import gradio as gr
import whisper
import speech_recognition as sr


model = whisper.load_model("base")

recog = sr.Recognizer()
def itself(audio):
    with sr.AudioFile(audio) as source:
        audio_data = recog.record(source)
        text = recog.recognize_google(audio_data=audio_data, language='en-US')
    return text
def inference(audio):
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    print(result.text)
    return result.text, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)


block = gr.Blocks()

with block:
    with gr.Group():
        with gr.Box():
            with gr.Row().style(mobile_collapse=False, equal_height=True):
                audio = gr.Audio(
                    label="Input Audio",
                    show_label=False,
                    source="microphone",
                    type="filepath"
                )
                audio.interactive
                btn = gr.Button("Transcribe")
        text = gr.Textbox(show_label=False, elem_id="result-textarea")

        # btn.click(inference, inputs=[audio], outputs=text)
        btn.click(itself, inputs=[audio], outputs=text)

block.launch()