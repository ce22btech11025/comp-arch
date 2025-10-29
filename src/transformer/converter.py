import os
from pathlib import Path
from .type_promoter import TypePromoter


class Converter:
    """
    Converter that uses TypePromoter for safe, file-level promotions.
    """

    def __init__(self, input_dir="data/input_programs",
                 output_dir="data/transformed_programs",
                 promote_to="float"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.promote_to = promote_to
        self.promoter = TypePromoter(promote_to=promote_to)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def transform_file(self, filename: str):
        input_path = self.input_dir / filename
        output_path = self.output_dir / filename

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        print(f"[Transformer] Processing: {filename}")

        code = input_path.read_text(encoding='utf-8')

        # Prepend math.h if needed
        if "#include <math.h>" not in code:
            code = "#include <math.h>\n" + code

        transformed = self.promoter.promote_code(code)

        # Write out the transformed code
        output_path.write_text(transformed, encoding='utf-8')

        print(f"[Transformer] ✅ Saved transformed file: {output_path}")
        return str(output_path)

    def transform_all(self):
        print(f"[Transformer] Starting transformation in {self.input_dir}")
        for f in os.listdir(self.input_dir):
            if f.endswith(".c"):
                try:
                    self.transform_file(f)
                except Exception as e:
                    print(f"[Transformer] ❌ Failed to transform {f}: {e}")
        print(f"[Transformer] Completed transformations.")
