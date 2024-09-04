# Translator
The translator doesn't really do everything yet, but it's a start with eval properly working

## How it works
1. Tokenize the input
2. Parse the tokens
3. Turn tokens into Python code
4. Eval python code

## Try it 
```bash
python3 translator.py debug
```

## Issues
- It doesn't tokenize everything yet. Needs more work
- The mail input is injected as a string, and uses SimpleNamespaces to handle dot notation
- The mail translator doesn't really work
- Functions need to be fixed. It was just a test
