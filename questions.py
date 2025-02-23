# questions.py
questions_data = {
    "variables": [
        {"question": "What is used to store data?", "options": ["Variable", "Function", "Loop", "Condition"], "correct": "Variable", "difficulty": 0},
        {"question": "What symbol assigns a value?", "options": ["+", "=", "-", "*"], "correct": "=", "difficulty": 1},
        {"question": "Which is a valid variable name?", "options": ["1var", "var_1", "var-1", "var 1"], "correct": "var_1", "difficulty": 2},
        {"question": "What type is 'Hello'?", "options": ["int", "float", "string", "bool"], "correct": "string", "difficulty": 3},
        {"question": "Can variable names start with numbers?", "options": ["Yes", "No", "Sometimes", "Only in loops"], "correct": "No", "difficulty": 4},
        {"question": "What keyword declares a constant in some languages?", "options": ["var", "let", "const", "static"], "correct": "const", "difficulty": 5},
        {"question": "Which is NOT a valid variable type?", "options": ["integer", "boolean", "character", "loop"], "correct": "loop", "difficulty": 6},
        {"question": "What does x = x + 1 do?", "options": ["Error", "Increments x", "Decrements x", "Nothing"], "correct": "Increments x", "difficulty": 7},
        {"question": "What's the scope of a local variable?", "options": ["Global", "Function only", "File", "Program"], "correct": "Function only", "difficulty": 8},
        {"question": "What does += do?", "options": ["Add and assign", "Subtract", "Multiply", "Divide"], "correct": "Add and assign", "difficulty": 9}
    ],
    "loops": [
        {"question": "What repeats code?", "options": ["Loop", "If", "Print", "Input"], "correct": "Loop", "difficulty": 0},
        {"question": "Which is a loop type?", "options": ["if", "while", "switch", "case"], "correct": "while", "difficulty": 1},
        {"question": "What does 'for' do?", "options": ["Count", "Check", "Print", "Input"], "correct": "Count", "difficulty": 2},
        {"question": "What's an infinite loop?", "options": ["Runs once", "Never ends", "Ends quick", "Skips"], "correct": "Never ends", "difficulty": 3},
        {"question": "What stops a loop?", "options": ["break", "continue", "return", "exit"], "correct": "break", "difficulty": 4},
        {"question": "What skips one iteration?", "options": ["break", "continue", "stop", "skip"], "correct": "continue", "difficulty": 5},
        {"question": "How many times does range(3) loop?", "options": ["2", "3", "4", "5"], "correct": "3", "difficulty": 6},
        {"question": "What's a nested loop?", "options": ["Loop in loop", "Fast loop", "Slow loop", "Error"], "correct": "Loop in loop", "difficulty": 7},
        {"question": "What's loop unrolling?", "options": ["Expanding loops", "Ending loops", "Starting loops", "Breaking loops"], "correct": "Expanding loops", "difficulty": 8},
        {"question": "What's a common loop optimization?", "options": ["More loops", "Fewer iterations", "More variables", "Less code"], "correct": "Fewer iterations", "difficulty": 9}
    ],
    "conditions": [
        {"question": "What makes decisions?", "options": ["If", "Loop", "Function", "Variable"], "correct": "If", "difficulty": 0},
        {"question": "What checks equality?", "options": ["=", "==", "!=", "<"], "correct": "==", "difficulty": 1},
        {"question": "What does else do?", "options": ["True case", "False case", "Loop", "Error"], "correct": "False case", "difficulty": 2},
        {"question": "What's elif short for?", "options": ["Else if", "End if", "Early if", "Extra if"], "correct": "Else if", "difficulty": 3},
        {"question": "What does > mean?", "options": ["Less", "Greater", "Equal", "Not equal"], "correct": "Greater", "difficulty": 4},
        {"question": "What's && in Python?", "options": ["and", "or", "not", "&"], "correct": "and", "difficulty": 5},
        {"question": "How many conditions in if-elif-else?", "options": ["1", "2", "3", "Unlimited"], "correct": "Unlimited", "difficulty": 6},
        {"question": "What's a ternary operator?", "options": ["3 conditions", "Short if-else", "Loop", "Function"], "correct": "Short if-else", "difficulty": 7},
        {"question": "What evaluates to True/False?", "options": ["String", "Boolean", "Integer", "Float"], "correct": "Boolean", "difficulty": 8},
        {"question": "What's short-circuit evaluation?", "options": ["Skip conditions", "All conditions", "Loop", "Error"], "correct": "Skip conditions", "difficulty": 9}
    ]
}