# AI Dialogue Creator

This project transforms complex content into engaging, natural dialogues using AI agents. By converting technical or dense material into conversational exchanges between two speakers, it makes information more accessible and entertaining. The dialogues can be further enhanced with text-to-speech capabilities to create podcast-like audio content, making learning and information sharing more dynamic and enjoyable.

The system leverages advanced language models to break down content into meaningful segments, generate relevant discussion questions, and craft natural-sounding dialogue that maintains accuracy while adding personality and engagement.

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (Python package installer)

### Environment Setup

1. Set up the environment using make:

```bash
make setup-env
```

2. Create a `.env` file and add your API keys:

```bash
cp .env.example .env
```
3. Spin up the TTS server:

```bash
make run-tts-cpu
```

4. Run the application:

```bash
make run
```