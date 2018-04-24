from tkinter import *
from tkinter.filedialog import askdirectory
from topic_modeling import set_params
import os

direc = os.path.dirname(os.path.realpath(__file__))+'\..'
record = []

def browse():
    global direc
    direc = askdirectory(initialdir=direc)
    set_text(direc)
    return

def set_text(text):
    dir_entry.delete(0,END)
    dir_entry.insert(0,text)
    print(direc)
    return

def call_lda():
    max_iter = int(max_iter_entry.get())
    burn_in = int(burn_in_entry.get())
    lag = int(lagstride_entry.get())
    alpha = int(alpha_entry.get())
    eta = float(eta_entry.get())
    num_of_topics = int(num_of_topics_entry.get())
    num_of_freq_words = int(num_of_frew_words_entry.get())
    global record
    print(direc)
    record = set_params(direc, max_iter, burn_in, lag, alpha, eta, num_of_topics, num_of_freq_words)
    for r in range(len(record)):
        print(r)
        out_textarea.insert(END, 'topic %d:\t'%(r))
        out_textarea.insert(END, record[r])
        out_textarea.insert(END, '\n')
    return

window = Tk()
window.title('LDA Topic Modeling')
window.resizable(False, False)

lda_params = LabelFrame(window, text='LDA Parameters')
lda_params.grid(row=0)
alpha_label = Label(lda_params, text='alpha = ')
alpha_label.grid(row=0, column=0)
alpha_entry = Entry(lda_params, width=25)
alpha_entry.grid(row=0, column=1)
alpha_entry.insert(END, '50')
alpha_label_rest = Label(lda_params, text=' / number of topics')
alpha_label_rest.grid(row=0, column=2)
eta_label = Label(lda_params, text='eta = ')
eta_label.grid(row=0, column=3)
eta_entry = Entry(lda_params, width=30)
eta_entry.insert(END, '0.1')
eta_entry.grid(row=0, column=4)

specs = LabelFrame(window, text='Specifications')
specs.grid(row=1)
num_of_topics_label = Label(specs, text='Number of topics: ')
num_of_topics_label.grid(row=0, column=0)
num_of_topics_entry = Entry(specs)
num_of_topics_entry.insert(END, '20')
num_of_topics_entry.grid(row=0, column=1)
num_of_freq_words_label = Label(specs, text='Number of most frequent words: ')
num_of_freq_words_label.grid(row=0, column=2)
num_of_frew_words_entry = Entry(specs)
num_of_frew_words_entry.insert(END, '5')
num_of_frew_words_entry.grid(row=0, column=3)

docs = LabelFrame(window, text='Documents')
docs.grid(row=2)
dir_entry = Entry(docs, width = 80)
dir_entry.insert(END, '')
dir_entry.grid(row=0, column=0)
browse_button = Button(docs, text='Browse', command=browse)
browse_button.grid(row=0, column=1)

final = LabelFrame(window, text='Finalize')
final.grid(row=3)
max_iter_label = Label(final, text='Maximum number of iterations: ')
max_iter_label.grid(row=0, column=1)
max_iter_entry = Entry(final, width=30)
max_iter_entry.insert(END, '1000')
max_iter_entry.grid(row=0, column=2)
burn_in_label = Label(final, text='Burn-in: ')
burn_in_label.grid(row=1, column=0)
burn_in_entry = Entry(final)
burn_in_entry.insert(END, '100')
burn_in_entry.grid(row=1, column=1)
lagstride_label = Label(final, text='Lag: ')
lagstride_label.grid(row=1, column=2)
lagstride_entry = Entry(final)
lagstride_entry.insert(END, '1')
lagstride_entry.grid(row=1, column=3)
# thread_check = Checkbutton(final, text='Use Threading')
# thread_check.grid(row=2, column=1)
file_check = Checkbutton(final)
start_button = Button(final, text='Start', width=25, command=call_lda)
start_button.grid(row=2, column=2)

status = LabelFrame(window, text='Status')
status.grid(row=4)
status_textarea = Text(status, height=5, width=65)
status_scroll = Scrollbar(status, command=status_textarea.yview)
status_textarea.configure(yscrollcommand=status_scroll.set)
status_textarea.tag_configure('bold_italics', font=('Verdana', 12, 'bold', 'italic'))
status_textarea.tag_configure('big', font=('Verdana', 24, 'bold'))
status_textarea.tag_configure('color', foreground='blue', font=('Tempus Sans ITC', 14))
status_textarea.tag_configure('groove', relief=GROOVE, borderwidth=2)
status_textarea.tag_bind('bite', '<1>', lambda e, t=status_textarea: t.insert(END, "Text"))
status_textarea.pack(side=LEFT)
status_scroll.pack(side=RIGHT, fill=Y)

out = LabelFrame(window, text='Output')
out.grid(row=5)
out_textarea = Text(out, height=20, width=65)
out_scroll = Scrollbar(out, command=out_textarea.yview)
out_textarea.configure(yscrollcommand=out_scroll.set)
out_textarea.tag_configure('bold_italics', font=('Verdana', 12, 'bold', 'italic'))
out_textarea.tag_configure('big', font=('Verdana', 24, 'bold'))
out_textarea.tag_configure('color', foreground='blue', font=('Tempus Sans ITC', 14))
out_textarea.tag_configure('groove', relief=GROOVE, borderwidth=2)
out_textarea.tag_bind('bite', '<1>', lambda e, t=out_textarea: t.insert(END, "Text"))
out_textarea.pack(side=LEFT)
out_scroll.pack(side=RIGHT, fill=Y)


window.mainloop()
