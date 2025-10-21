#!/usr/bin/env python3
"""
Database setup script for AI Chat API
This script initializes the database and creates the necessary tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import create_tables, engine
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Setup the database with all required tables"""
    try:
        logger.info("Setting up database...")
        logger.info(f"Database URL: {settings.database_url}")
        
        # Create all tables
        create_tables()
        
        logger.info("Database setup completed successfully!")
        
        # Test connection
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
