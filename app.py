import os
import openai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv

env_path = '.env'

load_dotenv(env_path)
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_transcript(youtube_url):
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    try:
        transcript = transcript_list.find_manually_created_transcript()
        language_code = transcript.language_code  
    except:
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
            language_code = transcript.language_code  
        except:
            raise Exception("No suitable transcript found.")

    full_transcript = " ".join([part['text'] for part in transcript.fetch()])
    return full_transcript, language_code  

def summarize_with_langchain_and_openai(transcript, language_code, model_name='gpt-3.5-turbo'):
    # Same as your original code
    pass

def main():
    st.title('YouTube Video Summarizer')
    st.write("Summarize any YouTube video with the power of AI!")

    link = st.text_input('Enter the link of the YouTube video you want to summarize:', help="Paste YouTube video link here")

    if st.button('Summarize', key='summarize_button'):
        if link:
            try:
                with st.spinner('Loading transcript...'):
                    transcript, language_code = get_transcript(link)

                with st.spinner('Creating summary...'):
                    model_name = 'gpt-3.5-turbo'
                    summary = summarize_with_langchain_and_openai(transcript, language_code, model_name)

                st.subheader('Summary:')
                st.write(summary)
            except Exception as e:
                st.error(str(e))
        else:
            st.warning('Please enter a valid YouTube link.')

    st.sidebar.title("About")
    st.sidebar.info(
        "This web app helps you summarize YouTube videos using AI. "
        "It utilizes the OpenAI 3.5 model to generate summaries "
        "based on the transcript of the provided video."
    )
    st.sidebar.title("How to Use")
    st.sidebar.info(
        "1. Enter the link of the YouTube video you want to summarize.\n"
        "2. Click on the 'Summarize' button.\n"
        "3. Wait for the summary to be generated.\n"
        "4. Enjoy your summarized content!"
    )

    st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
