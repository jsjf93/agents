# Project README

## About

This is a simple demo project that uses websockets to allow a client to send a name to an AI agent that in turn returns a funny name based on the input.
The objective was to get a feel for FastAPI, atomic-agents, and to get more familiar with deploying a Python backend to Azure.

## Instructions for Running the UI and API

### Prerequisites

- Python 3.12
- Node.js 22

### Setting Up the Environment

1. **Clone the repository:**

```sh
git clone https://github.com/jsjf93/agents.git
```

Then open up two terminals and cd into

```sh
cd agents.api

cd agent.ui
```

2. **Set up a virtual environment for the API:**

```sh
# in agents.api
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

3. **Install the API requirements:**

```sh
pip install -r requirements.txt
```

4. **Install the UI dependencies:**

```sh
# in agents.ui
npm install
```

### Running the API

1. **Set the required environment variables:**

Create a `.env` file in the root directory and add the following variables:

```env
OPENAI_API_KEY=your_api_key
# alternatively you could configure the application to use a different provider, atomic-agents uses Instructor
```

2. **Run the API server:**

```sh
# in agents.api
python app.py
```

### Running the UI

1. **Set the required environment variables:**

Create a `.env` file in the `agent.ui` directory and add the following variables:

```env
VITE_API_BASE_URL=localhost:8000
```

2. **Run the UI development server:**

```sh
# in agents.ui
npm run dev
```

### Accessing the Application

- The API will be running at `http://localhost:8000`
- The UI will be running at `http://localhost:5173`

### Deployment Notes

- In the API App Service, under `Configuration` -> `Startup Command`, add `./startup.sh`.
- To deploy the UI, `npm run build` and then deploy the `dist` folder that gets generated.
- In the UI App Service, for the `Startup Command`, add `pm2 serve /home/site/wwwroot/dist --no-daemon --spa`.
