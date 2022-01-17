
from codegen_sources.preprocessing.lang_processors.slang_processor import SlangProcessor
from pathlib import Path

from codegen_sources.preprocessing.tests.tokenization.tokenization_tests_utils import (
    compare_funcs,
)

processor = SlangProcessor(root_folder=Path(__file__).parents[4].joinpath("tree-sitter"))

TESTS = []
TESTS.append(("a = [3.14,4]", ["a", "=", "[", "3.14", ",", "4", "]"]))


def test_slang_tokenizer():
    for i, (x, y) in enumerate(TESTS):
        y_ = processor.tokenize_code(x)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


FUNC_EXTRACTION = [
    (
        """
/************************************************
**
** Script Name : Example: Simple
** Script Type : Example
*************************************************/

DoIt = Func(Double( max ))
Returns(Array())
{
    A = [];
    A;
};

Price = Func(Double( V ))
Returns(Double())
{
    V * 100;
};""",
        (["DoIt = Func ( Double ( max ) ) Returns ( Array ( ) ) { A = [ ] ; A ; }",
          "Price = Func ( Double ( V ) ) Returns ( Double ( ) ) { V * 100 ; }"], []),
    ),

]


def test_extract_functions():
    for input_file, expected_funcs in FUNC_EXTRACTION:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            processor.tokenize_code(input_file)
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(actual_funcs_sa, expected_sa)
        compare_funcs(actual_funcs_cl, expected_cl)


test_slang_tokenizer()
test_extract_functions()
