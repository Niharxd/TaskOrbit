from app import create_app

# Create the Flask app using our factory function
app = create_app()

if __name__ == "__main__":
    # debug=True gives helpful error pages during development
    # Turn this OFF in production!
    app.run(debug=True)
