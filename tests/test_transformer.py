import unittest
import os
from pathlib import Path
from src.transformer.type_promoter import TypePromoter
from src.transformer.converter import Converter
from src.executor.compiler_runner import CompilerRunner

class TestTypePromoter(unittest.TestCase):

    def setUp(self):
        self.promoter = TypePromoter(promote_to="float")

    def test_declaration_promotion(self):
        line = "int a = 5;"
        expected = "float a = 5;"
        self.assertEqual(self.promoter.promote_declaration(line), expected)

    def test_literal_promotion(self):
        line = "a = 5 + b;"
        result = self.promoter.promote_literal(line)
        self.assertIn("5.0", result)

    def test_no_change_for_printf(self):
        line = 'printf("%d", a);'
        result = self.promoter.promote_literal(line)
        self.assertEqual(result, line)


class TestConverter(unittest.TestCase):

    def setUp(self):
        self.input_dir = Path("data/input_programs")
        self.output_dir = Path("data/transformed_programs")
        self.converter = Converter(input_dir=self.input_dir, output_dir=self.output_dir)

        # Create dummy C file for testing
        self.test_file = self.input_dir / "temp_test.c"
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        with open(self.test_file, "w") as f:
            f.write("int main() { int a = 5; int b = 10; int c = a + b; return 0; }")

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()
        transformed_file = self.output_dir / self.test_file.name
        if transformed_file.exists():
            transformed_file.unlink()

    def test_transform_file_creates_output(self):
        out = self.converter.transform_file("temp_test.c")
        self.assertTrue(Path(out).exists())

    def test_compile_transformed(self):
        self.converter.transform_file("temp_test.c")
        compiler = CompilerRunner()
        exe_path = compiler.compile(str(self.output_dir / "temp_test.c"), output_name="temp_test_fp")
        self.assertTrue(Path(exe_path).exists())


if __name__ == "__main__":
    unittest.main()
