# class Validator:
#     def __init__(self, evaluate_function: function):
#         self.evaluate_function = evaluate_function
#         # should return (is_valid, error)

# class Query:
#     def __init__(self, name, validators=[], required=True):
#         self.name = name
#         self.validators = validators
#         self.required = required

#     def validate(self, request):
#         value = request.args[self.name]
#         is_all_valid = True
#         for validator in self.validators:
#             is_valid, error = validator.evaluate(value)
#             if not is_valid: is_all_valid = False

#         return is_valid
