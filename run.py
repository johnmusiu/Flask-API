"""import classes required"""
import os
from app.api import create_app

# our dev class is DevelopmentConfig
config_mode = 'development'
app = create_app(config_mode)
    
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

