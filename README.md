# Sentensizer

:raised_hands: Devoted to all Clean Code lovers.

Utility for counting meaningful code lines (sentences) in Python, JavaScript/TypScript, Java, C# files. It helps to detect files that contain too many code lines and need refactoring.

Default critical number of sentences per file - **70**.

Tested on Python 3.11+.

## :computer: Usage

```bash
# initiate environment (ONLY ONCE)
python -m venv env

# activate session
. env/bin/activate

# install dependencies (ONLY ONCE)
pip install -r requirements.txt

# analyse directory and print all results
python main.py DIRECTORY/

# analyse directory and print only critical lines
# exit with error code
python main.py DIRECTORY/ --only-critical

# end session
. env/bin/activate
```

## :camera: Screenshots

![Default run](/i/general.png)

![Only critical run](/i/only-critical.png)