import piplates as pp
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, TextInput, Select
from bokeh.plotting import figure

from .Supply import Rigol as rg


def comment_handler(attr, old, new):
    change = comment_box.value + ","
    with open(file_control.value, 'a') as f:
        f.write(change)
        f.close()


def plot_update():
    global voltages
    global currents
    x.append(len(x))
    voltage = pp.getADC(my_supply.get_channel)
    voltages.append(voltage)
    length = len(x)
    source.data = dict(x=x, voltages=voltages)
    change = str(length).strip() + "," + str(voltage).strip() + ","
    with open(file_control.value, 'a') as f:
        # writer = csv.writer(f)
        f.write(change)
        f.close()


def channel_handler(attr, old, new):
    if channel_dropdown.value == '1':
        my_supply.set_channel('ch1')
    elif channel_dropdown.value == '2':
        my_supply.set_channel('ch2')
    else:
        my_supply.set_channel('ch3')


def file_handler(attr, old, new):
    save_file = file_control.value
    f = open(save_file)


def start_button_handler():
    curdoc().add_periodic_callback(plot_update, 200)


f = open('readings.csv', 'a')
my_supply = rg()
apply_button = Button(label='Apply settings')

channel_dropdown = Select(title='Channel control', options=['1', '2', '3'])
file_control = TextInput(title='Path to save file', value='readings.csv')
comment_box = TextInput(title='Annotation (Will be added when box is unselected)')
start_button = Button(label='Start recording data')
plot1 = figure(x_range=(0, 10000), y_range=(0, 30), x_axis_label='Time (100 ms)', y_axis_label='Volts',
               title='ADC over time', plot_width=500, plot_height=200)

x = []
voltages = []
currents = []
source = ColumnDataSource({
    'x': x,
    'voltages': voltages
})
plot1.line(x='x', y='voltages', source=source)
file_control.on_change('value', file_handler)
file_control.on_change('value', file_handler)
comment_box.on_change('value', comment_handler)
channel_dropdown.on_change('value', channel_handler)
start_button.on_click(start_button_handler)
curdoc().add_periodic_callback(plot_update, 100)
curdoc().add_root(row(column(file_control, comment_box, channel_dropdown, start_button),
                      column(plot1)))
