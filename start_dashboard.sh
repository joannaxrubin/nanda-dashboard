#!/bin/bash

# NANDA Dashboard Quick Start Script
# This script sets up and runs your dashboard

echo "🚀 NANDA Hackathon Dashboard Setup"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check if running for first time
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "📝 First-time setup detected"
    echo ""
    echo "Do you want to connect to Notion? (y/n)"
    read connect_notion
    
    if [ "$connect_notion" = "y" ]; then
        echo ""
        echo "Enter your Notion API key:"
        read api_key
        
        echo "Enter your Database ID:"
        read database_id
        
        mkdir -p .streamlit
        cat > .streamlit/secrets.toml << EOF
NOTION_API_KEY = "$api_key"
DATABASE_ID = "$database_id"
EOF
        echo "✓ Notion credentials saved"
    else
        echo "✓ Using sample data (you can connect Notion later)"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Starting dashboard..."
echo "Dashboard will open at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Run the dashboard
streamlit run nanda_dashboard_app.py
