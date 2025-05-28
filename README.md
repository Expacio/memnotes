Installation
-----------


Clone this repo:


      git clone https://github.com/your-username/memnotes.git
      cd memnotes

Python Installations
-----------
Install Python 3.12.3 if not already done:


      
      # Linux
      sudo apt update
      sudo apt install python3.12

  For **Windows, macOS**: Just use the online available official installers at the [Python Downloads](https://www.python.org/downloads/) webpage.

Dependencies
-----------
This project uses **Flask**, so make sure you install that:

    # Linux/macOS
    python3 -m pip install -U flask

    # Windows
    py -3 -m pip install -U flask


If not found by **api.py**, the **users.db** file automatically respawns with proper initializations at every script startup.
