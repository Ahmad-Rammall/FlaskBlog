from flaskBlog import createApp #createApp function inside __init__.py

app = createApp()

#when we run this code with 'python'.
if __name__ == '__main__': 
    app.run(debug=True)