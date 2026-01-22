"""
Notion API Integration Helper
Connects your Streamlit dashboard to Notion database
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime

class NotionClient:
    """Helper class for interacting with Notion API"""
    
    def __init__(self, api_key: str, database_id: str):
        self.api_key = api_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.notion.com/v1"
    
    def query_database(self, filter_params: Optional[Dict] = None) -> Dict:
        """Query the Notion database for tasks"""
        url = f"{self.base_url}/databases/{self.database_id}/query"
        
        payload = {}
        if filter_params:
            payload["filter"] = filter_params
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error querying Notion: {e}")
            return {"results": []}
    
    def parse_tasks(self, response: Dict) -> Dict:
        """Parse Notion database response into task data"""
        results = response.get("results", [])
        
        tasks = []
        status_counts = {
            "Completed": 0,
            "In Progress": 0,
            "Not Started": 0
        }
        
        for page in results:
            props = page.get("properties", {})
            
            # Extract task properties
            task = {
                "id": page.get("id"),
                "url": page.get("url"),
                "name": self._get_title(props.get("Task Name")),
                "team": self._get_select(props.get("Team")),
                "status": self._get_status(props.get("Status")),
                "priority": self._get_select(props.get("Priority")),
                "due": self._get_date(props.get("Due Date")),
                "week": self._get_select(props.get("Week")),
                "impact": self._get_select(props.get("Impact")),
                "assigned_to": self._get_people(props.get("Assigned To"))
            }
            
            tasks.append(task)
            
            # Count statuses
            status = task.get("status", "Not Started")
            if status in status_counts:
                status_counts[status] += 1
        
        return {
            "tasks": tasks,
            "total_tasks": len(tasks),
            "completed_tasks": status_counts["Completed"],
            "in_progress": status_counts["In Progress"],
            "not_started": status_counts["Not Started"],
            "status_counts": status_counts
        }
    
    def get_tasks_by_team(self, team_name: str) -> List[Dict]:
        """Get all tasks for a specific team"""
        filter_params = {
            "property": "Team",
            "select": {
                "equals": team_name
            }
        }
        
        response = self.query_database(filter_params)
        data = self.parse_tasks(response)
        return data["tasks"]
    
    def get_tasks_by_week(self, week: str) -> List[Dict]:
        """Get all tasks for a specific week"""
        filter_params = {
            "property": "Week",
            "select": {
                "equals": week
            }
        }
        
        response = self.query_database(filter_params)
        data = self.parse_tasks(response)
        return data["tasks"]
    
    def get_critical_tasks(self) -> List[Dict]:
        """Get all critical priority tasks"""
        filter_params = {
            "property": "Priority",
            "select": {
                "equals": "🔥 Critical"
            }
        }
        
        response = self.query_database(filter_params)
        data = self.parse_tasks(response)
        return data["tasks"]
    
    # Helper methods to extract data from Notion property formats
    
    def _get_title(self, prop: Optional[Dict]) -> str:
        """Extract title from Notion title property"""
        if not prop or "title" not in prop:
            return ""
        title_array = prop.get("title", [])
        if not title_array:
            return ""
        return title_array[0].get("plain_text", "")
    
    def _get_select(self, prop: Optional[Dict]) -> str:
        """Extract value from Notion select property"""
        if not prop or "select" not in prop:
            return ""
        select = prop.get("select")
        if not select:
            return ""
        return select.get("name", "")
    
    def _get_status(self, prop: Optional[Dict]) -> str:
        """Extract value from Notion status property"""
        if not prop or "status" not in prop:
            return "Not Started"
        status = prop.get("status")
        if not status:
            return "Not Started"
        return status.get("name", "Not Started")
    
    def _get_date(self, prop: Optional[Dict]) -> str:
        """Extract date from Notion date property"""
        if not prop or "date" not in prop:
            return ""
        date = prop.get("date")
        if not date:
            return ""
        return date.get("start", "")
    
    def _get_people(self, prop: Optional[Dict]) -> List[str]:
        """Extract people from Notion people property"""
        if not prop or "people" not in prop:
            return []
        people = prop.get("people", [])
        return [person.get("name", "") for person in people]


def get_sample_data() -> Dict:
    """Return sample data when Notion API is not configured"""
    return {
        'tasks': [
            {
                'name': 'Develop 2-3 framework solution options',
                'team': 'Tech Team',
                'status': 'In Progress',
                'priority': '🔥 Critical',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '🎯 Presentation Ready',
                'assigned_to': ['Chinedu', 'Jude', 'Nicolas']
            },
            {
                'name': 'Define what February hackathon teams will build',
                'team': 'Tech Team',
                'status': 'Not Started',
                'priority': '🔥 Critical',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '🎯 Presentation Ready',
                'assigned_to': ['Chinedu']
            },
            {
                'name': 'Identify specific contacts at MIT',
                'team': 'Outreach Team',
                'status': 'In Progress',
                'priority': '⚡ High',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '🤝 Partnership Building',
                'assigned_to': ['Saranga']
            },
            {
                'name': 'Identify specific contacts at BU',
                'team': 'Outreach Team',
                'status': 'Not Started',
                'priority': '⚡ High',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '🤝 Partnership Building',
                'assigned_to': ['Kevin']
            },
            {
                'name': 'Create outreach template for team-wide use',
                'team': 'Outreach Team',
                'status': 'In Progress',
                'priority': '🔥 Critical',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '🤝 Partnership Building',
                'assigned_to': ['Saranga', 'Kevin']
            },
            {
                'name': 'Create comprehensive sponsor target list',
                'team': 'Events Team',
                'status': 'In Progress',
                'priority': '⚡ High',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '📋 Foundation Work',
                'assigned_to': ['Chris']
            },
            {
                'name': 'Research venue options for 200 people',
                'team': 'Events Team',
                'status': 'In Progress',
                'priority': '⚡ High',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '📋 Foundation Work',
                'assigned_to': ['Lorisca']
            },
            {
                'name': 'Draft hour-by-hour hackathon schedule',
                'team': 'Events Team',
                'status': 'Not Started',
                'priority': '⚡ High',
                'due': '2024-12-18',
                'week': 'Week 1 (Dec 12-18)',
                'impact': '🎯 Presentation Ready',
                'assigned_to': ['Takashi']
            },
        ],
        'total_tasks': 21,
        'completed_tasks': 0,
        'in_progress': 5,
        'not_started': 16,
        'status_counts': {
            'Completed': 0,
            'In Progress': 5,
            'Not Started': 16
        }
    }


# Example usage
if __name__ == "__main__":
    # Test with sample data
    data = get_sample_data()
    print(f"Total tasks: {data['total_tasks']}")
    print(f"In progress: {data['in_progress']}")
    
    # To use with real Notion API:
    # client = NotionClient(api_key="your_key", database_id="your_db_id")
    # response = client.query_database()
    # data = client.parse_tasks(response)
