import os
import sys
from types import ModuleType

# Add src directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Provide dummy google.generativeai module if not installed
if 'google.generativeai' not in sys.modules:
    google_module = ModuleType('google')
    generativeai_module = ModuleType('google.generativeai')
    cloud_module = ModuleType('google.cloud')
    storage_module = ModuleType('google.cloud.storage')
    sys.modules['google'] = google_module
    sys.modules['google.generativeai'] = generativeai_module
    sys.modules['google.cloud'] = cloud_module
    sys.modules['google.cloud.storage'] = storage_module




