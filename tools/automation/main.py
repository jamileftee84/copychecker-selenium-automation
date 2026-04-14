import sys
import importlib

TEST_REGISTRY = {
    "1": ("AI Reverse Image Search", "tools.automation.tests.test_ai_reverse_image_search"),
    "2": ("Small Text Generator", "tools.automation.tests.test_small_text"),
    "3": ("Happy Birthday Fonts", "tools.automation.tests.test_happy_birthday_fonts"),
    "4": ("Reverse Image Search", "tools.automation.tests.test_reverse_image_search"),
    "5": ("Remove PDF Pages", "tools.automation.tests.test_remove_pdf_pages"),
    "6": ("PDF to Image", "tools.automation.tests.test_pdf_to_image"),
    "7": ("PDF to Text", "tools.automation.tests.test_pdf_to_text"),
    "8": ("OCR PDF", "tools.automation.tests.test_OCR_pdf"),
    "9": ("Extract PDF Pages", "tools.automation.tests.test_extract_pdf_pages"),
    "10": ("Split PDF Free", "tools.automation.tests.test_split_pdf_free"),
    "11": ("Merge PDF", "tools.automation.tests.test_merge_pdf"),
    "12": ("Image to PDF", "tools.automation.tests.test_image_to_pdf"),
    "13": ("PDF to Word", "tools.automation.tests.test_pdf_to_word"),
    "14": ("Edit PDF Metadata", "tools.automation.tests.test_edit_pdf_metadata"),
    "15": ("CSV to TXT", "tools.automation.tests.test_csv_to_txt"),
    "16": ("Text to ASCII", "tools.automation.tests.test_text_to_ascii"),
    "17": ("Sign PDF", "tools.automation.tests.test_sign_pdf"),
    "18": ("PDF Editor", "tools.automation.tests.test_pdf_editor"),
    "19": ("Plagiarism Checker", "tools.automation.tests.test_plagiarism_checker"),
}


def run_test(module_path, label):
    importlib.import_module(module_path)
    print(f"{label} test completed.\n")

def display_menu():
    print("\nSelect a test to run:")
    for key, (label, _module_path) in TEST_REGISTRY.items():
        print(f"{key}. {label}")
    print("0. Exit")

def main():
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1–19 or 0 to exit): ").strip()

            if choice == "0":
                print("Exiting. Goodbye!")
                sys.exit(0)
            elif choice in TEST_REGISTRY:
                label, module_path = TEST_REGISTRY[choice]
                run_test(module_path, label)
            else:
                print("Invalid choice. Please enter a number between 0 and 19.\n")
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
