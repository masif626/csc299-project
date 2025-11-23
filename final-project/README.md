# MindQuest: AI-Powered Journal and RPG

MindQuest is a command line application developed in Python. It functions as a Personal Task Manager and a Journaling tool, utilizing the OpenAI API for its sentiment analysis and gamification.

## Technical Stack

**Language**: Python
**Database**: SQLite
**AI Integration**: OpenAI API (gpt-3.5-turbo)
**Key Libraries:**: openai, python-dotenv, pytest
**Process**: Specification Driven Developement

## Setup and Installation

1. Activate Virtual Environment: 
    ''' bash
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    '''
2. Install Project: 
    '''bash
    py -m pip install -e .
    py -m pip install python-dotenv
    '''
3. Set API Key: 
    '''bash
    $env:OPENAI_API_KEY = "sk-Enter-Key"
    '''

## Command Reference

mindquest status : Display current XP, Level and Adventure Name.
mindquest mood-board : Shows the average sentiment score over the last seven days.
mindquest quest add <text> : Adds a new quest(task).
mindquest quest done <id> : Marks quest as complete and awards XP.
mindquest journal add <text> : Writes a new journal entry and runs AI sentiment analysis.
mindquest journal list : Shows at least five entries with sentiment scores.
mindquest journal remove <id> : Permanently removes journal entry. 