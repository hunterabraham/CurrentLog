import os
import datetime
import time
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, TextInput, Select
from bokeh.plotting import figure
import piplates.DAQCplate as DAQC

try:
    from .Supply import Rigol as rg
except Exception: #ImportError
    from Supply import Rigol as rg

def comment_handler(attr, old, new):
    change = comment_box.value + ","
    with open(filename, 'a') as f:
        f.write(change)
        f.close()


def plot_update():
    global voltages
    global currents
    x.append(len(x))
    voltage1 = DAQC.getADC(0, 0)
    voltage2 = DAQC.getADC(0, 1)
    voltage3 = DAQC.getADC(0, 2)
    voltage4 = DAQC.getADC(0, 3)
    voltage5 = DAQC.getADC(0, 4)
    voltage6 = DAQC.getADC(0, 5)
    voltage7 = DAQC.getADC(0, 6)
    voltage8 = DAQC.getADC(0, 7)
    voltages1.append(voltage1)
    voltages2.append(voltage2)
    voltages3.append(voltage3)
    voltages4.append(voltage4)
    voltages5.append(voltage5)
    voltages6.append(voltage6)
    voltages7.append(voltage7)
    voltages8.append(voltage8)
    length = len(x)
    source.data = dict(x=x, voltages1=voltages1, voltages2=voltages2, voltages3=voltages3, voltages4=voltages4, voltages5=voltages5, voltages6=voltages6, voltages7=voltages7, voltages8=voltages8)
    change = str(length).strip() + "," + str(datetime.datetime.now()) + "," + str(time.time() - t0) + "," + str(voltage1).strip() + "," + str(voltage2).strip() + "," + str(voltage3).strip() + "," + str(voltage4).strip() + str(voltage5).strip() + "," + str(voltage6).strip() + "," + str(voltage7).strip() + "," + str(voltage8).strip() + ","
    with open(os.path.join(directory_control.value, file_control.value), 'a') as f:
        # writer = csv.writer(f)
        f.write(change)
        f.write("\n")
        f.close()

def file_handler(attr, old, new):
    filename = os.path.join(directory_control.value, file_control.value)
    if not os.path.exists(directory_control.value):
        os.mkdir(directory_control.value)
    try:
        f = open(filename,"x")
    except Exception:
        f = open(filename, "w+")
        print("File exists.")
    f.write("Index,Date Stamp,Time Stamp,Channel 0,Channel 1,Channel 2,Channel 3,Channel 4,Channel 5,Channel 6,Channel 7\n")
    f.close()

callback_id = None

def start_button_handler():
    global callback_id
    if start_button.label == 'Start recording data':
        callback_id = curdoc().add_periodic_callback(plot_update, 100)
        start_button.label = 'Stop recording data'
    else:
        start_button.label = 'Start recording data'
        curdoc().remove_periodic_callback(callback_id)


filename = "readings " + str(datetime.datetime.now()) + ".csv"
f = open(filename, 'w+')
f.write("Index,Date Stamp,Time Stamp,Channel 0,Channel 1,Channel 2,Channel 3,Channel 4,Channel 5,Channel 6,Channel 7\n")
f.close()
my_supply = rg()

file_control = TextInput(title='Name of save file', value=filename)
comment_box = TextInput(title='Annotation (Will be added when box is unselected)')
start_button = Button(label='Start recording data')
directory_control = TextInput(title='Absolute path to desired directory (Ex: /home/pi/Documents/)')
plot1 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label='Time (100 ms)', y_axis_label='Volts', title='Channel 0', plot_width=500, plot_height=200)
plot2 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 1", plot_width=500, plot_height=200)
plot3 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 2", plot_width=500, plot_height=200)
plot4 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 3", plot_width=500, plot_height=200)
plot5 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 4", plot_width=500, plot_height=200)
plot6 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 5", plot_width=500, plot_height=200)
plot7 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 6", plot_width=500, plot_height=200)
plot8 = figure(x_range=(0,100), y_range=(0, 5), x_axis_label="Time (100 ms)", y_axis_label="Volts", title="Channel 7", plot_width=500, plot_height=200)
x = []
voltages1 = []
voltages2 = []
voltages3 = []
voltages4 = []
voltages5 = []
voltages6 = []
voltages7 = []
voltages8 = []
source = ColumnDataSource({
    'x': x,
    'voltages1': voltages1,
    'voltages2': voltages2,
    'voltages3': voltages3,
    'voltages4': voltages4,
    'voltages5': voltages5,
    'voltages6': voltages6,
    'voltages7': voltages7,
    'voltages8': voltages8
})
plot1.line(x='x', y='voltages1', source=source)
plot2.line(x='x', y='voltages2', source=source)
plot3.line(x='x', y='voltages3', source=source)
plot4.line(x='x', y='voltages4', source=source)
plot5.line(x='x', y='voltages5', source=source)
plot6.line(x='x', y='voltages6', source=source)
plot7.line(x='x', y='voltages7', source=source)
plot8.line(x='x', y='voltages8', source=source)

file_control.on_change('value', file_handler)
directory_control.on_change('value', file_handler)
comment_box.on_change('value', comment_handler)
start_button.on_click(start_button_handler)
t0=time.time()

#curdoc().add_periodic_callback(plot_update, 50)
curdoc().add_root(row(column(directory_control, file_control, comment_box, start_button),
                      column(plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8)))
