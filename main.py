import os
from src.analyzer.parser import CParser
from src.analyzer.code_analyzer import CodeAnalyzer
from src.transformer.converter import Converter
from src.executor.compiler_runner import CompilerRunner
from src.executor.benchmark_runner import BenchmarkRunner
from src.visualizer.plot_results import PlotResults
from src.visualizer.summary_report import SummaryReport


def main():
    print("\n=== ALU vs FPU Optimization Workflow ===\n")

    # 1 Analyze sample input programs
    input_dir = "data/input_programs"
    parser = CParser()
    for file in os.listdir(input_dir):
        if file.endswith(".c"):
            cursor = parser.parse(os.path.join(input_dir, file))
            analyzer = CodeAnalyzer(cursor)
            analysis_result = analyzer.analyze()
            print(f"[Analysis] {file}: {len(analysis_result['operations'])} arithmetic ops, "
                  f"{len(analysis_result['loops'])} loops, {len(analysis_result['variables'])} vars")

    # 2 Transform integer → floating-point
    converter = Converter(promote_to="float")
    converter.transform_all()

    # 3 Compile both versions
    compiler = CompilerRunner()
    for file in os.listdir(input_dir):
        if file.endswith(".c"):
            # Compile integer version
            compiler.compile(os.path.join(input_dir, file), output_name=f"{os.path.splitext(file)[0]}_int")
            # Compile floating version
            compiler.compile(os.path.join("data/transformed_programs", file), output_name=f"{os.path.splitext(file)[0]}_fp")

    # 4 Benchmark executions
    benchmarker = BenchmarkRunner()
    bin_dir = "data/results/bin"
    for exe in os.listdir(bin_dir):
        if os.access(os.path.join(bin_dir, exe), os.X_OK):
            benchmarker.run(os.path.join(bin_dir, exe))

    # 5 Visualization and report generation
    plotter = PlotResults()
    plotter.plot_comparison()

    reporter = SummaryReport()
    reporter.generate()

    print("\n Workflow complete! Results stored in data/results/\n")

if __name__ == "__main__":
    main()
# import os
# from src.analyzer.parser import CParser
# from src.analyzer.code_analyzer import CodeAnalyzer
# from src.transformer.converter import Converter
# from src.executor.compiler_runner import CompilerRunner
# from src.executor.benchmark_runner import BenchmarkRunner
# from src.visualizer.plot_results import PlotResults
# from src.visualizer.summary_report import SummaryReport

# # Newly added imports  
# from src.utils.file_ops import read_yaml
# from src.utils.logger import get_logger


# def main():
#     # Load configuration
#     config_path = "config.yaml"
#     config = read_yaml(config_path)

#     # Initialize logger
#     logger = get_logger("main_logger", config_path=config_path)
#     logger.info("=== ALU vs FPU Optimization Workflow ===")

#     # Extract relevant paths from config
#     input_dir = config["paths"]["input_programs"]
#     transformed_dir = config["paths"]["transformed_programs"]
#     bin_dir = os.path.join(config["paths"]["analyzer_output"], "bin")

#     # Ensure necessary directories exist
#     for _, path in config["paths"].items():
#         os.makedirs(path, exist_ok=True)
#     os.makedirs(bin_dir, exist_ok=True)

#     # 1 Analyze sample input programs
#     parser = CParser()
#     for file in os.listdir(input_dir):
#         if file.endswith(".c"):
#             file_path = os.path.join(input_dir, file)
#             cursor = parser.parse(file_path)
#             analyzer = CodeAnalyzer(cursor)
#             analysis_result = analyzer.analyze()
#             logger.info(f"[Analysis] {file}: {len(analysis_result['operations'])} ops, "
#                         f"{len(analysis_result['loops'])} loops, {len(analysis_result['variables'])} vars")

#     # 2 Transform integer → floating-point
#     converter = Converter(promote_to=config["fpu"]["precision"])
#     converter.transform_all()
#     logger.info(" Code transformation complete.")

#     # 3 Compile both versions
#     compiler = CompilerRunner()
#     for file in os.listdir(input_dir):
#         if file.endswith(".c"):
#             src_file = os.path.join(input_dir, file)
#             transformed_file = os.path.join(transformed_dir, file)
#             int_out = f"{os.path.splitext(file)[0]}_int"
#             fp_out = f"{os.path.splitext(file)[0]}_fp"

#             compiler.compile(src_file, output_name=int_out)
#             compiler.compile(transformed_file, output_name=fp_out)

#     logger.info(" Compilation of all programs complete.")

#     # 4 Benchmark executions
#     benchmarker = BenchmarkRunner()
#     if os.path.exists(bin_dir):
#         for exe in os.listdir(bin_dir):
#             exe_path = os.path.join(bin_dir, exe)
#             if os.access(exe_path, os.X_OK):
#                 benchmarker.run(exe_path)
#         logger.info(" Benchmarking complete.")
#     else:
#         logger.warning(f" Binary directory not found: {bin_dir}")

#     # 5 Visualization and report generation
#     plotter = PlotResults()
#     plotter.plot_comparison()

#     reporter = SummaryReport()
#     reporter.generate()

#     logger.info(" Workflow complete! Results stored in data/results/")


# if __name__ == "__main__":
#     main()
