from lexer import *




infix = "[a-b]"


classes_handled = ClassesPreprocessor(infix)
preprocessed = preprocessor(classes_handled)
print(f"preprocessed:       {preprocessed}")

final = shunt(preprocessed)

print(f"\n\nfinal:          {final}")

