from app import create_app

app = create_app()

if __name__ == "__main__":
    # Enable debug mode for development; switch off in production
    app.run(debug=True)