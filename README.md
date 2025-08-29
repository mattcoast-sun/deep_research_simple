# 🔬 Deep Research Agent

A powerful AI-powered research assistant that takes complex questions and breaks them down into manageable sub-questions to provide comprehensive, well-researched answers.

## ✨ What Does It Do?

This intelligent research agent:
- 🧩 **Breaks down complex questions** into smaller, focused sub-questions
- 🔍 **Researches each sub-question** thoroughly using AI
- 📝 **Synthesizes all findings** into a cohesive, comprehensive answer
- 🎨 **Presents results beautifully** in an easy-to-read format

## 🚀 Quick Start (2 Minutes Setup!)

### For Beginners - Just Want to See It Work?

1. **Download the code**: Click the green "Code" button above → "Download ZIP"
2. **Open the frontend**: Simply double-click `index.html` to open it in your browser
3. **Try the demo**: Click one of the sample questions or type your own!

*Note: The frontend will work immediately, but you'll need to set up the backend (step 4 below) to get actual AI-powered research results.*

### Full Setup (with AI Backend)

#### Prerequisites
- Python 3.8 or higher
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

#### Step 1: Download & Extract
```bash
# Download this repository and extract the ZIP file
# Or clone it:
git clone https://github.com/mattcoast-sun/deep_research_simple.git
cd deep_research_simple
```

#### Step 2: Install Dependencies
```bash
# Install required Python packages
pip install -r requirements.txt
```

#### Step 3: Set Up Your API Key
Create a file called `.env` in the project folder and add your OpenAI API key:
```
# Copy this content into a new file called '.env'
OPENAI_API_KEY=your_openai_api_key_here
```

**Important:** 
- Get your API key from [OpenAI's platform](https://platform.openai.com/api-keys)
- Replace `your_openai_api_key_here` with your actual API key
- Keep your `.env` file private - never share it or commit it to version control

#### Step 4: Start the Backend
```bash
# Run the API server
python3 fastest_api.py
```
You should see: `Application startup complete. Uvicorn running on http://localhost:8008`

#### Step 5: Open the Frontend
Double-click `index.html` or open it in your browser. The research agent is now ready to use!

## 🎯 How to Use

1. **Open `index.html`** in your web browser
2. **Choose a sample question** or write your own research query
3. **Click "Do deep research"** and wait for the magic to happen
4. **Explore the comprehensive results** presented in a beautiful format

### Sample Research Questions
- "How does the universe work from a physics perspective?"
- "How can cognitive psychology inform the way I understand my own mind?"
- "What are the latest developments in renewable energy?"
- "How do neural networks actually learn?"

## 🏗️ Project Structure

```
deep_research_simple/
├── index.html          # 🌐 Main frontend interface (START HERE!)
├── style.css           # 🎨 Beautiful styling
├── agent.py            # 🤖 Core AI research logic
├── fastest_api.py      # ⚡ FastAPI backend server
├── config.py           # ⚙️ Configuration management
├── requirements.txt    # 📦 Python dependencies
└── README.md          # 📖 This guide
```

## 🛠️ Technical Details

### Frontend
- **Pure HTML/CSS/JavaScript** - no frameworks needed
- **Modern, responsive design** with smooth animations
- **Real-time API communication** with the Python backend

### Backend
- **FastAPI** for high-performance API endpoints
- **OpenAI GPT-4** for intelligent question breakdown and research
- **Async processing** for efficient handling of multiple research tasks
- **HTML/Markdown output** for beautifully formatted results

## 🔧 Troubleshooting

### Common Issues

**"Connection refused" or API errors:**
- Make sure the backend is running (`python fastest_api.py`)
- Check that you see "Uvicorn running on http://localhost:8008"

**"Invalid API key" errors:**
- Verify your `.env` file contains the correct OpenAI API key
- Make sure there are no extra spaces in your `.env` file

**Frontend shows but research doesn't work:**
- The frontend (`index.html`) works standalone for demo purposes
- To get actual AI research results, you need the backend running

**Python import errors:**
- Make sure you're in the project directory when running commands
- Try: `pip install -r requirements.txt` again

## 💡 Customization Ideas

- **Modify sample questions** in `index.html` (lines 45-51)
- **Adjust research depth** by changing `max_questions` in the frontend
- **Customize the AI behavior** by editing prompts in `agent.py`
- **Style the interface** by modifying `style.css`

## 🤝 Contributing

This is a simple, educational project perfect for beginners to understand:
- AI agent architecture
- Frontend-backend communication
- API design with FastAPI
- HTML/CSS/JavaScript fundamentals

Feel free to fork, modify, and enhance!

## 📄 License

Open source - feel free to use for learning and experimentation!

---

**🎉 Happy Researching!** This tool demonstrates how modern AI can break down complex problems into manageable pieces - a powerful technique for both artificial and human intelligence.
