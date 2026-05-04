from pathlib import Path
# Small utility to convert the csv file to the level file.

def convert_csv_to_txt(csv_file: str) -> Path:
	source = Path(csv_file)
	if not source.is_file():
		raise FileNotFoundError(f"CSV file not found: {source}")

	content = source.read_text(encoding="utf-8")
	output_path = source.with_suffix(".txt")
	output_path.write_text(content.replace(",", ""), encoding="utf-8")
	return output_path


def main() -> None:
    file_path = "assets/level2.csv"

    output_path = convert_csv_to_txt(file_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
	main()
