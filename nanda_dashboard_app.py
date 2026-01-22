"""
NANDA Hackathon Project Dashboard
A visual, motivating dashboard for student-led teams
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from typing import Dict, List

# Page configuration
st.set_page_config(
    page_title="NANDA Hackathon Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .mission-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .team-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .tech-team { border-left-color: #3b82f6; }
    .outreach-team { border-left-color: #8b5cf6; }
    .events-team { border-left-color: #10b981; }
    
    .mvp-badge {
        background: linear-gradient(90deg, #ffd700 0%, #ffed4e 100%);
        color: #000;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .countdown-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Notion API Configuration
NOTION_API_KEY = st.secrets.get("NOTION_API_KEY", "")  # You'll add this in Streamlit secrets
DATABASE_ID = "dc9611d2-af6d-4aa5-9a19-eb5f47aab9b9"

def fetch_notion_tasks():
    """Fetch tasks from Notion database"""
    try:
        from notion_integration import NotionClient, get_sample_data
        
        api_key = st.secrets.get("NOTION_API_KEY", "")
        database_id = st.secrets.get("DATABASE_ID", "")
        
        if not api_key or not database_id:
            return get_sample_data()
        
        client = NotionClient(api_key, database_id)
        response = client.query_database()
        return client.parse_tasks(response)
    except Exception as e:
        st.error(f"Error fetching from Notion: {e}")
        from notion_integration import get_sample_data
        return get_sample_data()

def calculate_countdown(target_date):
    """Calculate days until target date"""
    target = datetime.strptime(target_date, "%Y-%m-%d")
    today = datetime.now()
    delta = target - today
    return delta.days

def create_progress_bar(percentage, color="#667eea"):
    """Create a visual progress bar using Plotly"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Progress"},
        delta = {'reference': 100, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_team_task_chart(data):
    """Create a stacked bar chart of tasks by team and status"""
    # Sample data for visualization
    teams_df = pd.DataFrame({
        'Team': ['Tech Team', 'Outreach Team', 'Events Team'],
        'Completed': [0, 0, 0],
        'In Progress': [2, 1, 2],
        'Not Started': [4, 6, 4]
    })
    
    fig = go.Figure(data=[
        go.Bar(name='Completed', x=teams_df['Team'], y=teams_df['Completed'], marker_color='#10b981'),
        go.Bar(name='In Progress', x=teams_df['Team'], y=teams_df['In Progress'], marker_color='#f59e0b'),
        go.Bar(name='Not Started', x=teams_df['Team'], y=teams_df['Not Started'], marker_color='#ef4444')
    ])
    
    fig.update_layout(
        barmode='stack',
        title="Tasks by Team & Status",
        xaxis_title="Team",
        yaxis_title="Number of Tasks",
        height=400,
        showlegend=True
    )
    return fig

def create_priority_distribution():
    """Create pie chart of tasks by priority"""
    priorities = pd.DataFrame({
        'Priority': ['🔥 Critical', '⚡ High', '✨ Medium', '💫 Low'],
        'Count': [6, 10, 4, 1]
    })
    
    fig = px.pie(
        priorities, 
        values='Count', 
        names='Priority',
        title='Task Priority Distribution',
        color_discrete_sequence=['#ef4444', '#f59e0b', '#eab308', '#3b82f6']
    )
    fig.update_layout(height=400)
    return fig

def create_timeline_gantt():
    """Create a Gantt chart showing project timeline"""
    tasks_timeline = pd.DataFrame([
        dict(Task="Week 1: Foundation", Start='2024-12-12', Finish='2024-12-18', Team="All Teams"),
        dict(Task="Week 2: Build & Refine", Start='2024-12-18', Finish='2024-12-28', Team="All Teams"),
        dict(Task="Winter Break", Start='2024-12-28', Finish='2025-01-06', Team="Break"),
        dict(Task="Post-Break: Final Polish", Start='2025-01-06', Finish='2025-01-12', Team="All Teams"),
        dict(Task="PRESENTATION DAY!", Start='2025-01-12', Finish='2025-01-13', Team="Milestone"),
        dict(Task="January Execution", Start='2025-01-13', Finish='2025-02-01', Team="All Teams"),
        dict(Task="February HACKATHON", Start='2025-02-22', Finish='2025-02-23', Team="Milestone"),
    ])
    
    fig = px.timeline(
        tasks_timeline,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Team",
        title="Project Timeline - Path to Launch"
    )
    fig.update_layout(height=400)
    return fig

# Main Dashboard
def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 NANDA Hackathon Mission Control</h1>', unsafe_allow_html=True)
    
    # Mission Statement
    st.markdown("""
    <div class="mission-box">
        <h2>🎯 Our Mission</h2>
        <p style="font-size: 1.2rem;">Launch Boston's first AI agent hackathon that makes NANDA accessible to non-technical students. 
        We're not just organizing an event—we're pioneering how to democratize AI infrastructure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Countdown Timers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        days_to_meeting = calculate_countdown("2024-12-18")
        st.markdown(f"""
        <div class="countdown-box">
            <div>⏰ Team Meeting</div>
            <div style="font-size: 3rem;">{days_to_meeting}</div>
            <div>days away</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        days_to_presentation = calculate_countdown("2025-01-12")
        st.markdown(f"""
        <div class="countdown-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div>🎤 NANDA Presentation</div>
            <div style="font-size: 3rem;">{days_to_presentation}</div>
            <div>days away</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        days_to_hackathon = calculate_countdown("2025-02-22")
        st.markdown(f"""
        <div class="countdown-box" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div>🎪 Hackathon Day</div>
            <div style="font-size: 3rem;">{days_to_hackathon}</div>
            <div>days away</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Fetch data
    data = fetch_notion_tasks()
    
    # Key Metrics
    st.subheader("📊 Project Health Dashboard")
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            label="Total Tasks",
            value=data['total_tasks'],
            delta="21 active"
        )
    
    with metric_col2:
        completion_rate = (data['completed_tasks'] / data['total_tasks'] * 100) if data['total_tasks'] > 0 else 0
        st.metric(
            label="Completion Rate",
            value=f"{completion_rate:.0f}%",
            delta=f"{data['completed_tasks']} completed"
        )
    
    with metric_col3:
        st.metric(
            label="In Progress",
            value=data['in_progress'],
            delta="5 active now",
            delta_color="normal"
        )
    
    with metric_col4:
        st.metric(
            label="Team Members",
            value="8",
            delta="3 teams"
        )
    
    st.markdown("---")
    
    # Visual Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.plotly_chart(create_team_task_chart(data), use_container_width=True)
    
    with chart_col2:
        st.plotly_chart(create_priority_distribution(), use_container_width=True)
    
    # Progress Gauge
    st.subheader("🎯 Overall Progress to Presentation")
    progress_col1, progress_col2, progress_col3 = st.columns([1, 2, 1])
    
    with progress_col2:
        st.plotly_chart(create_progress_bar(15), use_container_width=True)
    
    st.markdown("---")
    
    # Timeline
    st.subheader("🗓️ Project Timeline")
    st.plotly_chart(create_timeline_gantt(), use_container_width=True)
    
    st.markdown("---")
    
    # Team Sections
    st.subheader("👥 Team Progress")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💾 Tech Team", "📩 Outreach Team", "📅 Events Team", "🏆 MVPs & Recognition"])
    
    with tab1:
        st.markdown('<div class="team-card tech-team">', unsafe_allow_html=True)
        st.markdown("### Tech Team - Building the Future")
        st.markdown("**Team Members:** Chinedu, Jude, Nicolas")
        
        st.markdown("**This Week's Focus:** Develop framework solution options")
        
        tech_progress = st.progress(0.3)
        st.caption("30% complete - In active development")
        
        st.markdown("**Current Tasks:**")
        tech_tasks = [t for t in data['tasks'] if t['team'] == 'Tech Team']
        for task in tech_tasks:
            status_color = "🟢" if task['status'] == 'Completed' else "🟡" if task['status'] == 'In Progress' else "⚪"
            st.markdown(f"{status_color} {task['name']} - {task['priority']} - Due: {task['due']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="team-card outreach-team">', unsafe_allow_html=True)
        st.markdown("### Outreach Team - Building Bridges")
        st.markdown("**Team Members:** Saranga, Kevin")
        
        st.markdown("**This Week's Focus:** Build contact list and launch outreach")
        
        outreach_progress = st.progress(0.2)
        st.caption("20% complete - Gathering contacts")
        
        st.markdown("**Current Tasks:**")
        outreach_tasks = [t for t in data['tasks'] if t['team'] == 'Outreach Team']
        for task in outreach_tasks:
            status_color = "🟢" if task['status'] == 'Completed' else "🟡" if task['status'] == 'In Progress' else "⚪"
            st.markdown(f"{status_color} {task['name']} - {task['priority']} - Due: {task['due']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="team-card events-team">', unsafe_allow_html=True)
        st.markdown("### Events Team - Making It Happen")
        st.markdown("**Team Members:** Chris, Lorisca, Takashi")
        
        st.markdown("**This Week's Focus:** Sponsor targets and venue research")
        
        events_progress = st.progress(0.35)
        st.caption("35% complete - Venue research underway")
        
        st.markdown("**Current Tasks:**")
        events_tasks = [t for t in data['tasks'] if t['team'] == 'Events Team']
        for task in events_tasks:
            status_color = "🟢" if task['status'] == 'Completed' else "🟡" if task['status'] == 'In Progress' else "⚪"
            st.markdown(f"{task['priority']} {task['name']} - Due: {task['due']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🏆 This Week's MVPs")
        st.info("MVPs will be announced after Thursday's team meeting!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 💾 Tech Team MVP")
            st.markdown('<div class="mvp-badge">🏆 TBD - Dec 18</div>', unsafe_allow_html=True)
            st.caption("Awaiting team meeting results")
        
        with col2:
            st.markdown("#### 📩 Outreach MVP")
            st.markdown('<div class="mvp-badge">🏆 TBD - Dec 18</div>', unsafe_allow_html=True)
            st.caption("Awaiting team meeting results")
        
        with col3:
            st.markdown("#### 📅 Events MVP")
            st.markdown('<div class="mvp-badge">🏆 TBD - Dec 18</div>', unsafe_allow_html=True)
            st.caption("Awaiting team meeting results")
        
        st.markdown("---")
        st.markdown("### 🎉 Recent Wins")
        st.success("✅ Dec 3: Successfully launched team with clear roles")
        st.success("✅ Dec 12: Second team meeting - momentum building!")
        st.info("🎯 Coming: Dec 18 - Presentation draft complete")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x150/667eea/ffffff?text=NANDA+Boston", use_container_width=True)
        
        st.markdown("### 🔗 Quick Links")
        st.markdown("- [Notion Dashboard](https://notion.so)")
        st.markdown("- [Task Tracker](https://notion.so)")
        st.markdown("- [Team Recognition](https://notion.so)")
        st.markdown("- [NotebookLM Guide](https://notebooklm.google.com)")
        
        st.markdown("---")
        st.markdown("### 📢 Latest Updates")
        st.info("Dec 12: Dashboard launched! 🚀")
        st.info("Next meeting: Dec 18, 4:30pm")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Stats")
        st.metric("Days to Presentation", days_to_presentation)
        st.metric("Active Tasks", data['in_progress'])
        st.metric("Team Morale", "🔥🔥🔥")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
            <small>Built with ❤️ by the NANDA team<br>
            Making AI infrastructure accessible to all</small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
