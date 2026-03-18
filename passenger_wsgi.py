import os
import sys

# Define the path to your project
# Replace 'YOUR_USERNAME' with your actual Serv00 username
# Replace 'YOUR_DOMAIN' with your actual Serv00 domain or path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'videosummarizer'))

# Import the Django WSGI application
from videosummarizer.wsgi import application
