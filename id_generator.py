from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/generate', methods = ['POST'])
def generate():
  numbers = request.form['numbers']
  numbers_list = numbers.split()
  formatted_numbers = [f'"{numbers}"' for numbers in numbers_list]
  result = f'( [Alert ID] Is {" | ".join(formatted_numbers)} )'
  return render_template('index.html', result=result)

if __name__ == '__main__':
  app.run(debug=True)