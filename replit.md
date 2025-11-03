# Student Pickup Code Generator

## Overview
A Python CLI application that generates and validates time-based pickup codes for students. The system creates unique 8-character codes using student IDs and time-based hashing, with a 2-hour validity window.

## Project Architecture
- **Language**: Python 3.11
- **Type**: CLI Application
- **Dependencies**: Standard library only (hashlib, time)
- **File Structure**: Single file application (main.py)

## Core Functionality
1. **Generate Pickup Code**: Creates an 8-character hash-based code for a student ID
   - Uses current hour bucket for time-based uniqueness
   - SHA256 hashing for security
   
2. **Validate Pickup Code**: Verifies codes within a 2-hour window
   - Checks current and previous hour buckets
   - Case-insensitive validation

## Recent Changes
- 2025-11-03: Initial project import and Replit environment setup
  - Installed Python 3.11
  - Added .gitignore for Python projects
  - Configured workflow to run the demo script

## Usage
The application runs demonstrations showing:
- Code generation and immediate validation
- Different students get different codes
- Invalid code rejection
- Code consistency within the same hour
- Code expiration after 2+ hours
