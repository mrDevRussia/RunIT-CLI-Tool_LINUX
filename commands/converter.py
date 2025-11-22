class Converter:
    def get_supported_conversions(self) -> dict:
        return {
            'js_to_python': ('javascript', 'python'),
            'python_to_javascript': ('python', 'javascript'),
            'html_to_markdown': ('html', 'markdown'),
        }

    def convert_code(self, source_file: str, target_language: str) -> str | None:
        return None