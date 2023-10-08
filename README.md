# Sentensizer

Utility for counting meaningful code lines (sentences) in Python, JavaScript/TypScript, Java, C# files. It helps to detect files that contain too many code lines and need refactoring.

Default critical number of sentences per file - **70**.

## Usage

```bash
# analyse directory and print all results
> python main.py DIRECTORY/

# analyse directory and print only critical lines
# exit with error code
> python main.py DIRECTORY/ --only-critical
```

## Screenshots

![Default run](/i/general.png)

![Only critical run](/i/only-critical.png)