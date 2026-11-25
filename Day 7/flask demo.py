from flask import Flask , render_template, request

app=Flask(__name__)
@app.route("/aa") #url creation
def hello():
    return render_template("f.html")

@app.route("/bb", methods=["GET","POST"]) #url creation
def hi():
    if request.method=="POST":
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        return f"<h2> Hello {name} Your age is {age} and your from {city}</h2>" 
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True, port=5000)


f.html :
<h1>hello nithish</h1>


index.html :

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h2>Enter your details</h2>
    <form action="/bb" method="POST">
        <input type="text" name="name" required><br>
        <input type="text" name="age" required><br>
        <input type="text" name="city" required><br>
        <button type="submit">SUBMIT</button>
    </form>
</body>
</html>
