class AIAssistant:
    def show_ai_help(self):
        print("runai <question> — offline assistant (stub)")

    def help_with_file(self, filename: str):
        print(f"AI analysis for '{filename}' is not available in this build.")

    def get_code_assistance(self, query: str):
        return {"topic": "General", "advice": "Assistant is not available."}

    def format_ai_response(self, response: dict):
        print(response.get("advice", ""))