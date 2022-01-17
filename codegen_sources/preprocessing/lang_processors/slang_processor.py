
from codegen_sources.preprocessing.lang_processors.tree_sitter_processor import (
    TreeSitterLangProcessor,
    NEW_LINE,
)

from codegen_sources.preprocessing.lang_processors.tokenization_utils import (
    ind_iter,
    NEWLINE_TOKEN,
)
import re


class SlangProcessor(TreeSitterLangProcessor):

    def __init__(self, root_folder):
        super().__init__(
            language="slang",
            ast_nodes_type_string=["comment", "string"],
            stokens_to_chars={},
            chars_to_stokens={},
            root_folder=root_folder,
        )

    def extract_functions(self, tokenized_code):
        """Extract functions from tokenized code"""
        if isinstance(tokenized_code, str):
            tokenized_code = tokenized_code.split()
        else:
            assert isinstance(tokenized_code, list)
            tokenized_code = tokenized_code

        tokens = iter(tokenized_code)
        functions_standalone = []
        functions_class = []
        number_indent = 0
        token_index = -1
        try:
            token = next(tokens)
            token_index = token_index + 1
        except StopIteration:
            return [], []
        while True:
            try:
                if token == "Func":
                    # backtrack to extract the function name as well, as we need this later
                    function = [tokenized_code[token_index-2], tokenized_code[token_index-1], token]
                    while not (token == "}" and number_indent == 0):
                        token = next(tokens)
                        token_index = token_index + 1
                        if token == "{":
                            number_indent += 1
                        elif token == "}":
                            number_indent -= 1
                        function.append(token)
                    try:
                        if function[function.index("(") + 1] == "self":
                            function = " ".join(function)
                            if function is not None:
                                functions_class.append(function)
                        else:
                            function = " ".join(function)
                            if function is not None:
                                functions_standalone.append(function)
                    except:
                        print(function)
                        token = next(tokens)
                        token_index = token_index + 1
                else:
                    token = next(tokens)
                    token_index = token_index + 1
            except StopIteration:
                break
        return functions_standalone, functions_standalone #functions_class

    def get_function_name(self, function):
        assert isinstance(function, str) or isinstance(function, list)
        if isinstance(function, str):
            function = function.split()
        return function[0]

    def extract_arguments(self, function):
        return []

    def obfuscate_code(self, code):
        raise NotImplementedError
