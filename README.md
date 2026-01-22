# 🚀 NANDA Hackathon Dashboard App

A beautiful, visual dashboard for tracking your NANDA hackathon project progress with real-time data from Notion.

## ✨ Features

- **📊 Real-time Metrics** - Live task completion, team progress, and project health
- **⏰ Countdown Timers** - Days until key milestones (team meeting, presentation, hackathon)
- **📈 Visual Analytics** - Interactive charts showing task distribution, priorities, and team progress
- **🗓️ Project Timeline** - Gantt chart visualization of your path to launch
- **👥 Team Dashboards** - Dedicated views for Tech, Outreach, and Events teams
- **🏆 MVP Recognition** - Celebrate weekly winners and team contributions
- **🎨 Beautiful UI** - Gradient designs, progress bars, and motivating visuals

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run nanda_dashboard_app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔗 Connecting to Notion (Optional)

To pull live data from your Notion database:

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Copy your integration token
3. Share your database with the integration
4. Create a `.streamlit/secrets.toml` file:

```toml
NOTION_API_KEY = "your_notion_integration_token_here"
```

5. Update the `fetch_notion_tasks()` function to make real API calls

### Sample Notion API Integration

```python
import requests

def fetch_notion_tasks():
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    response = requests.post(url, headers=headers)
    data = response.json()
    
    # Process and return data
    return process_notion_data(data)
```

## 📱 Deployment Options

### Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Add your Notion API key in the Secrets section
5. Deploy!

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku create nanda-dashboard
git push heroku main
heroku config:set NOTION_API_KEY=your_key_here
```

### Deploy Locally with Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "nanda_dashboard_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🎨 Customization

### Change Color Scheme

Edit the CSS in the `st.markdown()` section at the top of the app:

```python
.mission-box {
    background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
}
```

### Add New Metrics

Add custom metrics in the key metrics section:

```python
st.metric(
    label="Your Metric",
    value="Your Value",
    delta="Change from last week"
)
```

### Create Custom Charts

Use Plotly to create any chart type:

```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3])])
st.plotly_chart(fig)
```

## 📊 Data Structure

The app expects data in this format:

```python
{
    'tasks': [
        {
            'name': 'Task name',
            'team': 'Tech Team | Outreach Team | Events Team',
            'status': 'Completed | In Progress | Not Started',
            'priority': '🔥 Critical | ⚡ High | ✨ Medium | 💫 Low',
            'due': 'YYYY-MM-DD'
        }
    ],
    'total_tasks': int,
    'completed_tasks': int,
    'in_progress': int,
    'not_started': int
}
```

## 🛠️ Tech Stack

- **Streamlit** - Interactive web app framework
- **Plotly** - Interactive charts and visualizations
- **Pandas** - Data manipulation
- **Requests** - API calls to Notion

## 📈 Features Breakdown

### Countdown Timers
- Team Meeting countdown
- Presentation countdown  
- Hackathon countdown

### Visual Charts
- Tasks by Team & Status (stacked bar chart)
- Priority Distribution (pie chart)
- Overall Progress (gauge chart)
- Project Timeline (Gantt chart)

### Team Dashboards
- Tech Team progress and tasks
- Outreach Team progress and tasks
- Events Team progress and tasks
- MVP recognition tab

### Sidebar Features
- Quick links to Notion pages
- Latest updates feed
- Quick stats snapshot
- Team branding

## 🎯 Best Practices

1. **Update Data Daily** - Keep task statuses current in Notion
2. **Celebrate Wins** - Update MVP section after each meeting
3. **Share Progress** - Screenshot dashboard for team updates
4. **Mobile Friendly** - Streamlit works great on phones too
5. **Team Access** - Deploy publicly so everyone can see progress

## 🤝 Team Workflow

1. **Start of Week**: Review dashboard at team meeting
2. **Daily**: Team members check progress and update tasks
3. **End of Week**: Update MVPs and celebrate wins
4. **Before Presentations**: Screenshot metrics for slides

## 📸 Screenshots

The dashboard includes:
- Hero section with mission statement
- 3 countdown timers for key dates
- 4 key metrics cards
- 2 interactive charts
- Progress gauge
- Timeline Gantt chart
- 4 team tabs with individual progress

## 🚀 Next Steps

Want to enhance the dashboard? Consider adding:

- [ ] Email notifications for upcoming deadlines
- [ ] Slack integration for status updates
- [ ] Export to PDF for presentations
- [ ] Team member avatars
- [ ] Task assignment notifications
- [ ] Mobile app version
- [ ] Dark mode toggle
- [ ] Custom team colors

## 💡 Tips for Student Teams

- **Keep it simple**: Don't overcomplicate - focus on what motivates
- **Make it visual**: Progress bars feel better than percentages
- **Celebrate small wins**: Every completed task deserves recognition
- **Update regularly**: Stale data kills engagement
- **Make it accessible**: Deploy so everyone can check from anywhere

## 📞 Support

Questions? Reach out to your team lead or check:
- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Docs](https://plotly.com/python/)
- [Notion API Docs](https://developers.notion.com)

---

**Built with ❤️ for the Hult x NANDA team**  
*Making AI infrastructure accessible to everyone*
