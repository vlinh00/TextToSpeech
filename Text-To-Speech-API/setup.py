from setuptools import setup, find_packages

setup(
    name="text_to_speech_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'gTTS',
    ],
    description="A library for converting text to speech and returning audio as base64 encoded strings.",
    author="Le Linh",
    author_email="your.email@example.com",
    url="https//example.com",
)
