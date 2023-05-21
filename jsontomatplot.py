from flask import Flask, render_template, send_from_directory
import matplotlib.pyplot as plt
import json
from datetime import date, timedelta
from io import BytesIO
app = Flask(__name__)

#Sample json file
# {
#   "id": 1234,
#   "type": "example",
#   "quantity": 10,
#   "student": 1,
#   "date": "2023-05-20",
#   "hr": 9
# }

@app.route('/plot', methods=['GET'])
# def plot():
#     # Load JSON data from a file or request
#     with open('itemtest.json') as file:
#         data = json.load(file)

#     # Extract necessary values from JSON data
#     id_values = [item['id'] for item in data]
#     clothing_type = [item['type'] for item in data]
#     quantity_values = [item['quantity'] for item in data]

#     # Generate the plot using Matplotlib
#     fig, ax = plt.subplots()
#     ax.plot(id_values, quantity_values)
#     ax.set_xlabel('Clothing Type')
#     ax.set_ylabel('Quantity')
#     ax.set_title('Plot from JSON Data')

#     # Save the plot image in memory
#     image_stream = BytesIO()
#     plt.savefig(image_stream, format='png')
#     image_stream.seek(0)

#     # Clear the plot from memory
#     plt.clf()
#     plt.close()

#     # Render the template with the plot image
#     return Response(image_stream, mimetype='image/png')
@app.route('/plot', methods=['GET'])
def plot(time_frame):
    # Load JSON data from a file or request
    if time_frame == 'Day':
        today = str(date.today())
        ###Extract data from MongoDB corresponding to date
    elif time_frame == 'Week':
        today = date.today()
        start = str(today - timedelta(days=today.weekday()))
        end = str(start + timedelta(days=4))
        ###data = MongoDB[start_date : end_date]
    else:
        today = str(date.today())
        month,year = today.split('-')[0:2]
        start = f'{year}-{month}-01'
        end = f'{year}-{month}-31'
        ###data = MongoDB[start_date : end_date]
    with open('itemtest.json') as file:
        data = json.load(file)

    # Extract necessary values from JSON data
    types = [item['type'] for item in data]
    quantities = [item['quantity'] for item in data]

    # Generate the histogram using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(types, quantities)
    ax.set_xlabel('Type')
    ax.set_ylabel('Quantity')
    ax.set_title('Type vs Quantity')

    # Save the plot as an image file
    plot_path = 'static/plot.png'
    plt.savefig(plot_path)
    plt.close()

    # Render the template with the plot image path
    return render_template('plot.html', plot_path=plot_path)

@app.route('/plot/<path:filename>')
def download_plot(filename):
    # Serve the plot image file
    return send_from_directory('static', filename)

plot()

if __name__ == '__main__':
    app.run(debug=True)