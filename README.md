## 🚀 Migration with Claude Code

AI-assisted migration and data visualization project built with Python.

This project combines:

## 🔄 Migration logic
🧠 Claude / LLM integration
📊 Data visualization
🏗 Clean modular structure
📂 Project Structure
Migration-with-Claude-Code/
│
├── main.py
├── pyproject.toml
├── README.md
│
├── visualization/
│   ├── charts/
│   ├── diagrams/
│   ├── dashboards/
│   └── outputs/
│
├── data/
└── .venv/
📊 Visualization Module

All visualization logic and generated outputs are stored inside the visualization/ folder.

📁 Folder Breakdown
📈 visualization/charts/

Contains Python scripts that generate:

Line charts
Bar charts
Trend analysis
KPI comparisons

Run example:

python visualization/charts/your_script.py
🗺 visualization/diagrams/

Contains:

Migration flow diagrams
Architecture diagrams
Mermaid diagrams
AI-generated schema visuals
🖥 visualization/dashboards/

Interactive dashboards using:

Plotly
HTML-based visualizations
📦 visualization/outputs/

Stores generated files:

.png
.svg
.html
🖼 Sample Visualizations

Below are example outputs generated from this project.

(Replace filenames with your real PNG files inside visualization/outputs/)

📈 Migration Trend Analysis
![Migration Trend](visualization/outputs/migration_trend.png)

📊 Data Comparison Chart
![Data Comparison](visualization/outputs/data_comparison.png)

🗺 Migration Architecture Diagram
![Migration Architecture](visualization/outputs/migration_architecture.png)

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/Marwamedha/Migartion-with-Claude-Code.git
cd Migartion-with-Claude-Code
2️⃣ Install Dependencies (Using uv)
uv install

Add visualization libraries if needed:

uv add pandas matplotlib seaborn plotly pyarrow
🚀 Running the Project

Run main script:

python main.py

Run visualization scripts:

python visualization/charts/your_script.py
🧠 AI Integration

Set your API key (Mac):

export ANTHROPIC_API_KEY="your_api_key_here"

Or inside Python:

import os
os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"
📈 Workflow

1️⃣ Load data
2️⃣ Apply migration logic
3️⃣ Save processed dataset
4️⃣ Generate visualizations
5️⃣ Store PNG/HTML in visualization/outputs/
6️⃣ Display results in README

💡 Best Practices
Do not commit API keys
Add large generated files to .gitignore
Keep visualization logic modular
Separate raw data from processed outputs
📜 License

MIT License

If you send me the exact PNG filenames inside visualization/outputs/, I will customize this README precisely to your real files so it looks 100% polished for your GitHub portfolio 🔥
