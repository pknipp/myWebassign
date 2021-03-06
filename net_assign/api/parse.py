def parse(question_code, inputs):
    keywords = ['min', 'max', 'avg', 'sum', 'abs', 'ceil', 'floor', 'round', 'roundn', 'exp', 'log', 'log10', 'logn', 'pow', 'root', 'sqrt', 'clamp', 'inrange', 'swap', 'sin', 'cos', 'tan', 'acos', 'asin', 'atan', 'atan2', 'cosh', 'cot', 'csc', 'sec', 'sinh', 'tanh', 'd2r', 'r2d', 'd2g', 'g2d', 'hyp', 'and', 'nand', 'nor', 'not', 'or', 'xor', 'xnor', 'mand', 'mor']
    question_vars = set()
    errors = list()
    question_frags = question_code.split("{")
    if question_frags[0].count("}") > 0:
        errors.append("Your question code starts with a closing - rather than opening - brace.")
    del question_frags[0]
    for frag in question_frags:
        frags = frag.split("}")
        if len(frags) == 1:
            errors.append("In your question code you forgot to close a brace.")
        if len(frags) > 2:
            errors.append("In your question code you forgot an opening brace.")
        question_vars.add(frags[0])
    input_vars = set()
    new_inputs = list()
    for input in inputs:
        if isinstance(input[0], str):
            input_vars.add(input[0])
            new_inputs.append(input)
        else:
            new_input = list()
            subinput_length = len(input[0])
            for subinput in input:
                new_subinput = list()
                input_vars.add(subinput[0])
                if not len(subinput) == subinput_length:
                    errors.append("One of your array sizes is mismatched.")
                for i in range(len(subinput)):
                    value = subinput[i]
                    if i == 0:
                        # The variable name needs no parsing.
                        pass
                    elif value == "true" or value == True or value == "T":
                        value = True
                    elif value == "false" or value == False or value == "F":
                        value = False
                    else:
                        try:
                            # Check if it's a number.  If so, don't put a zero unnecessarily in the tenths place.
                            value = int(value) if int(value) == float(value) else float(value)
                        except ValueError:
                            # Leave it as a string if it's neither boolean nor numerical.
                            pass
                    new_subinput.append(value)
                new_input.append(new_subinput)
            new_inputs.append(new_input)
    for var in question_vars:
        if not var in input_vars:
            errors.append("Your question code references an undefined variable.")
    for var in input_vars:
        if var in keywords:
            errors.append("{0} is a reserved keyword, so you must change the name of that variable.".format(var))
    return {"errors": errors, "inputs": new_inputs, "vars": input_vars}
