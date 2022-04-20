from tkinter import messagebox
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3
import pickle
import json
proceed = False
import yadsk


 #  search interface
 #  class of the search interface, appears instead of the description text
#
#  When the search button is clicked the search frame will appear
#  in the place of the notebook_frame.
#  An entry widget will appear where user inputs a string
#  search in table name, in description buttons will be placed lower,
#  when clicked the strip.upper string will be to search
#  after that from each table from tbls-list (description or table name) will be selected,
#  changed to lower case and  checked if the search string is there or no
#  the list of the descriptions (tables) as buttons will be shown in the scrollable frame
#  description should be shortened to +-100 symbols - when clicked:
# select parents table from tbls-list and open_section(parent_table, current_table)
#


class SearchInTableDescription:
    def __init__(self, frame):

        self.layout_frame_raw = ttk.Frame(frame, style="Mainframe.TFrame")
        self.layout_frame_raw.grid(row=2, column=0, columnspan=2)
        self.layout_canvas = Canvas(self.layout_frame_raw, background="WHITE", width=250)
        self.layout_scr_bar = ttk.Scrollbar(self.layout_frame_raw,
                                     orient="vertical",
                                     command=self.layout_canvas.yview)
        self.layout_frame = ttk.Frame(self.layout_frame_raw, style="Mainframe.TFrame")
        self.layout_frame.bind("<Configure>",
                           lambda e: self.layout_canvas.configure(
                               scrollregion=self.layout_canvas.bbox("all")))
        self.layout_canvas.create_window((0, 0), window=self.layout_frame, anchor="nw")
        self.layout_canvas.configure(yscrollcommand=self.layout_scr_bar.set)

        self.layout_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.layout_scr_bar.pack(side=RIGHT, fill=Y)



        self.search_entry = Entry(frame, width=40)
        self.search_table_name = ttk.Button(frame, text="Search name", command=lambda:self.set_search_mode("table"))
        self.search_description = ttk.Button(frame, text="Search note",
                                             command=lambda: self.set_search_mode("description"))
        self.search_string = None
        self.table_description_dict = dict()
        self.found_tables = list()
        self.search_mode = None

        self.search_entry.grid(row=0, column=0, columnspan=2, pady=(5,0))
        self.search_table_name.grid(row=1, column=0)
        self.search_description.grid(row=1, column=1)
        # self.layout_frame.grid(row=2, column=0, columnspan=2)

    def set_search_mode(self, mode):
        self.search_mode = mode
        self.get_search_string()

    def get_search_string(self):
        self.search_string = self.search_entry.get().strip().upper()
        self.search_entry.delete(0, "end")
        self.get_table_name_description_dict()

    def get_table_name_description_dict(self):
        if self.search_mode == "table":
            self.find_table_name()
        else:
            self.find_from_description()


    def find_table_name(self):
        for key in Data_base:
            str(key)
            if self.search_string in key.upper():
                self.found_tables.append(key)
        self.layout_found_table()

    def find_from_description(self):
        for key in Data_base:
            try:
                description = Data_base[key][0]
                if self.search_string.lower() in description.lower():
                    #  make a short substring from description (i[1])
                    if len(description[0])>202:
                        start_index = description[0].find(self.search_string)
                        if start_index>99:
                            short_description = description[0][start_index-100:start_index+100]
                        else:
                            short_description = description[0][0:start_index+200]
                    else:
                        short_description = description
                    self.table_description_dict[key] = short_description
                    self.found_tables.append(key)
            except AttributeError:
                print(AttributeError)

        if self.search_mode == "table":
            self.layout_found_table()
        else:
            self.layout_description()


    def layout_found_table(self):
        for i in self.found_tables:
            FoundResult(self.layout_frame, i, i, self)

    def layout_description(self):
        for i in self.found_tables:
            FoundResult(self.layout_frame, self.table_description_dict[i], i, self)



class FoundResult(ttk.Button):
    def __init__(self, frame, string, table, search_interface):
        super().__init__(frame, text=string, width=40,
                         command=lambda: open_section(Data_base[table][1], table))
        self.pack()


def layout_search_interface(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    SearchInTableDescription(frame)


#  replaces the notebook interface with the moving interface
class MoveSectionInterface:

    def __init__(self, section_to_move):
        for widget in main_frame.winfo_children():
            widget.destroy()

        canvas = Canvas(main_frame, background="WHITE")
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scr_bar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scr_bar.pack(side=RIGHT, fill=Y)
        sections_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
        sections_frame.bind('<Configure>',
                            lambda e: canvas.configure(
                                scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sections_frame, anchor='nw')

        canvas.configure(yscrollcommand=scr_bar.set)

        layout_btns(sections_frame, "main", section_to_move)


# кнопки, которые отображаются в move_section_interface
class SectionToSelect(ttk.Button):
    def __init__(self, window, section_name, section_to_move):
        super().__init__(window, text=section_name, width=40,
                         command=lambda: layout_btns(window,
                                                     section_name,
                                                     section_to_move))
        self.pack(side=TOP)


#  the back button of the move interface
class BackBtn(ttk.Button):
    def __init__(self, window, current_table, section_to_move):
        super().__init__(window, text="Назад", command=self.go_back, width=40)
        self.pack()
        self.window = window
        self.section_to_move = section_to_move
        self.current_table = current_table

    def go_back(self):
        layout_btn_secnd_phase(self.window,
                               Data_base[self.current_table][1],
                               self.section_to_move)


# функция, которая привязывается к section_to_select
def layout_btns(frame, current_table, section_to_move):
    layout_btn_secnd_phase(frame, current_table, section_to_move)


def layout_btn_secnd_phase(frame, current_table, section_to_move):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.update()
    to_layout_list = list()
    for i in Data_base:
        if Data_base[i][1] == current_table:
            to_layout_list.append(i)

    for item in reversed(to_layout_list):
        SectionToSelect(frame, item, section_to_move)

    ttk.Button(frame, text="Выбрать текущий раздел", width=40,
               command=lambda: select_to_move(current_table, section_to_move)).pack()

    back_btn = BackBtn(frame, current_table, section_to_move)
    if current_table == "main":
        back_btn.state(["disabled"])

#  funtion that copies the table and deletes it from the previous place
def select_to_move(parent_table, section_to_move):
    # print(elder_table, " elder table, то, откуда все должно быть удалено")
    # print(parent_table, " parent table, то, куда все доллжно быть перемещено")
    # print(section_to_move, " section to move, то что перемещаем")

    #  take the parent table, description of the section to move


    #  change the parent table of the section to move
    table_attr = Data_base[section_to_move]
    Data_base[section_to_move] = [table_attr[0], parent_table, table_attr[2], datetime.now()]

    with open(Data_base_file, "wb") as f:
        pickle.dump(Data_base, f)


    layout_frames()
    open_section(parent_table, section_to_move)


class App(Tk):
    def __init__(self):
        global main_frame, Data_base_file, current_section_var, current_section_indicator, app
        global Data_base
        super().__init__()
        self.title("AI support notebook")
        self.configure(background="#F4F6F7")

        current_section_var = StringVar()

        sf = ttk.Style()
        sf.configure("Mainframe.TFrame", background="WHITE")
        sf.configure("Label.TLabel", background="WHITE")

        Data_base_file = yadsk.download()
        try:
            if Data_base_file:
                with open(Data_base_file, "rb") as f:
                    Data_base = pickle.load(f)
            else:
                Data_base_file = "techsupport_base"
                with open(Data_base_file, "rb") as f:
                    Data_base = pickle.load(f)


        except FileNotFoundError:
            Data_base = dict()
            Data_base["main"] = ["Main folder", "TSH", datetime.now(), datetime.now()]
            Data_base["My notebook"] = ["New note", "main", datetime.now(), datetime.now()]
            with open(Data_base_file, "wb") as f:
                pickle.dump(Data_base_file, f)
        except EOFError:
            Data_base = dict()
            Data_base["main"] = ["Main folder", "TSH", datetime.now(), datetime.now()]
            Data_base["My notebook"] = ["New note", "main", datetime.now(), datetime.now()]
            with open(Data_base_file, "wb") as f:
                pickle.dump(Data_base_file, f)

        main_frame = ttk.Frame(self, style="Mainframe.TFrame")
        main_frame.pack()

        layout_frames()
        open_section("TSH", "main")
        self.mainloop()


# класс используемый при создании кнопки с именем раздела
class SectionBtn(ttk.Button):
    def __init__(self, frame, button_section_name, click_cmnd, current_table):
        self.section_name = StringVar(value=button_section_name)
        super().__init__(frame, textvariable=self.section_name,
                         width=40, command=lambda: click_cmnd(current_table, self.section_name.get()))

        self.pack(fill=X, padx=3, side=TOP)
        self.current_table = current_table
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-3>", self.section_btn_right_clck_menu)
        self.frame = frame
        self.right_clck_menu = Menu(self.frame, tearoff=0)
        self.right_clck_menu.add_command(label="Rename", command=self.rename_section_interface)

    # выводим содержимое таблицы, куда наводится курсор к разделу (2 столбец)
    def on_enter(self, e):
        global section_inner_lvl_frame

        try:
            for widget in section_inner_lvl_frame.winfo_children():
                widget.destroy()
            section_inner_lvl_frame.update()
        except:
            pass

        time.sleep(0.1)
        description = Data_base[self.section_name.get()][0]
        to_layout_sections = list()
        for i in Data_base:
            if Data_base[i][1] == self.section_name.get():
                to_layout_sections.append(i)

        created_edited_time = Data_base[self.section_name.get()][2:]


        SectionInnerLvlLabel(section_inner_lvl_frame, to_layout_sections,
                             description, created_edited_time)

        return

    def on_leave(self, e):
        return

    def rename_section_interface(self):
        self.rename_win = Toplevel(self.frame)
        self.entry_widget = Entry(self.rename_win)
        self.entry_widget.pack()
        self.rename_button = ttk.Button(self.rename_win, text="Rename", command=self.rename_section)
        self.rename_button.pack()
        self.rename_win.mainloop()

    def rename_section(self):
        new_table_name = self.entry_widget.get().strip().upper()
        try:
            Data_base[new_table_name]
            messagebox.showinfo("Error", f"{new_table_name} already exists")
            self.rename_win.destroy()
        except KeyError:
            Data_base[new_table_name] = Data_base.pop(self.section_name.get())
            table_attr = Data_base[new_table_name]
            Data_base[new_table_name] = [table_attr[0], table_attr[1], table_attr[2], datetime.now()]
            for i in Data_base:
                if Data_base[i][1] == self.section_name.get():
                    i_attr = Data_base[i]
                    Data_base[i] = [i_attr[0], new_table_name, i_attr[2], i_attr[3]]

            self.section_name.set(new_table_name)
            with open(Data_base_file, "wb") as f:
                pickle.dump(Data_base_file, "techsupport_base")
            yadsk.upload()
        self.rename_win.destroy()

    def section_btn_right_clck_menu(self, event):
        try:
            self.right_clck_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_clck_menu.grab_release()


#  класс используемый для создания Энтри и кнопки добавения к current_table
class NewSectionEntry(Entry):
    def __init__(self, frame, current_table):
        super().__init__(frame)
        get_entry_btn = ttk.Button(frame, text="Добавить раздел", width=40,
                                   command=lambda: add_section(self, current_table))
        self.pack(side=TOP, pady=(10, 0))
        get_entry_btn.pack(side=TOP, pady=(3, 20))


# класс добавления описания к текущему разделу при помощи Text widget
class DescriptionText(Text):
    def __init__(self, frame, current_table):
        super().__init__(frame, height=25, wrap="word", width=40, font="Font 9")
        get_text_btn = ttk.Button(frame, text="Добавить описание к текущему разделу",
                                  command=lambda: add_description(self,
                                                                  current_table))
        description = (Data_base[current_table])[0]


        self.insert(END, description)
        get_text_btn.grid(row=0, column=0, sticky=EW)
        self.grid(row=1, column=0, sticky=N)
        self.descr_from_base = description
        self.table = current_table

    def update_descr_from_base(self, new_description):
            self.descr_from_base = new_description

        # get_text_btn.grid(row=3,column=0)


# поле для вывода содержимого таблицы при наведении курсора на кнопку
class SectionInnerLvlLabel(ttk.Label):
    def __init__(self, frame, to_layout, description, date):
        to_layout.insert(0, "Содержание")
        if len(to_layout) < 2:
            to_layout.insert(1, "Здесь пока пусто")
        tbl_of_cntns = "\n".join(to_layout)
        super().__init__(frame, wraplength=220, font="Font 9",
                         justify=LEFT, width=40,
                         text=f"{date[0]}\t{date[1]}\n{str(description[:500])}...\n\n{tbl_of_cntns}",
                         padding=(5, 10, 2, 0), style="Label.TLabel")
        self.grid(row=0, column=0, sticky=EW)

        # text_widget = Text(frame, height=10, wrap="word", width=40, font="Font 9")
        # text_widget.grid(row=1, column=0, sticky=W)
        #
        # text_widget.insert(END, f"{description[:500]} ...")
        # text_widget.update()


# добавление описания в таблицу
def add_description(text_widget, current_table):
    description = text_widget.get(1.0, "end").strip()
    Data_base[current_table] = Data_base.pop(current_table)
    Data_base[current_table] = [description, Data_base[current_table][1], Data_base[current_table][2], datetime.now()]
    with open(Data_base_file, "wb") as f:
        pickle.dump(Data_base, f)
    yadsk.upload()

    text_widget.update_descr_from_base(description)


# функция выкладывания кнопок текущего раздела
def layout_section_btns(current_table):
    global Data_base
    to_layout_list = list()

    for i in Data_base:
        if Data_base[i][1] == current_table:
            to_layout_list.append(i)

    #  experimental feature to sort by last edit
    # sections_list = []
    # for i in to_layout_list:
    #     sections_list.append(i[0])
    # cur.execute('''SELECT existing_section,
    #                         last_edit_time
    #             from "tbls_list" where existing_section="{}"
    #             "{}"'''.format(sections_list[0], "AND where existing_section=".join(sections_list[1:])))
    # section_edit_time = cur.fetchall()
    # conn.close()
    # print(section_edit_time, "section edit_time list of tuples")
    # modified_list = []
    # for tup in section_edit_time:
    #     modified_list.append(time_to_sec(tup[1]))
    # sorted(modified_list, key=lambda seconds: seconds[1])

    for item in reversed(to_layout_list):
        SectionBtn(section_frame,
                   item,  # section_name
                   open_section,
                   current_table)


# функция добавления нового раздела к базе данных, а также вывода ее в интрефейс в виде кнопки
def add_section(entry, current_table):
    global root, section_frame
    section_title = entry.get().strip().upper()
    if section_title != "":
        entry.delete(0, 'end')
        # if not section_title in existing_sections:
    try:
        Data_base[section_title]
        messagebox.showinfo("Error", f"{section_title} already exists" )
    except KeyError:
        add_table_to_tbls_list(section_title, current_table)
        new_section_btn = SectionBtn(section_frame, section_title, open_section, current_table)
        # else:
        #     messagebox.showinfo("Ошибка", "Такая запись уже существует")
    else:
        pass


def add_table_to_tbls_list(name, parent_table):
    Data_base[name] = ["Empty", parent_table, datetime.now(), datetime.now()]
    with open(Data_base_file, "wb") as f:
        pickle.dump(Data_base, f)
    yadsk.upload()


def layout_frames():
    global buttons_frame, section_frame, section_inner_lvl_frame, notebook_frame, back_btn, current_section_indicator

    for widget in main_frame.winfo_children():
        widget.destroy()

    buttons_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    buttons_frame.grid(row=0, column=0, columnspan=3, sticky=W)
    current_section_indicator = Label(buttons_frame, textvariable=current_section_var, background="WHITE",
                                      font="BOLD")

    sections_raw_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    sections_raw_frame.grid(row=1, column=0, sticky=NS)
    sections_canvas = Canvas(sections_raw_frame, background="WHITE", width=250)
    sections_scr_bar = ttk.Scrollbar(sections_raw_frame,
                                     orient="vertical",
                                     command=sections_canvas.yview)
    section_frame = ttk.Frame(sections_raw_frame, style="Mainframe.TFrame")
    section_frame.bind("<Configure>",
                       lambda e: sections_canvas.configure(
                           scrollregion=sections_canvas.bbox("all")
                       ))
    sections_canvas.create_window((0, 0), window=section_frame, anchor="nw")
    sections_canvas.configure(yscrollcommand=sections_scr_bar.set)

    sections_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
    sections_scr_bar.pack(side=RIGHT, fill=Y)



    section_inner_lvl_raw_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    section_inner_lvl_raw_frame.grid(row=1, column=1, sticky=NSEW, padx=0)

    inner_lvl_canvas = Canvas(section_inner_lvl_raw_frame, background="WHITE", width=300)
    inner_lvl_scr_bar = ttk.Scrollbar(section_inner_lvl_raw_frame,
                                     orient="vertical",
                                     command=inner_lvl_canvas.yview)
    section_inner_lvl_frame = ttk.Frame(section_inner_lvl_raw_frame, width=300, style="Mainframe.TFrame")
    section_inner_lvl_frame.bind("<Configure>",
                       lambda e: inner_lvl_canvas.configure(
                           scrollregion=inner_lvl_canvas.bbox("all")
                       ))
    inner_lvl_canvas.create_window((0, 0), window=section_inner_lvl_frame, anchor="nw")
    inner_lvl_canvas.configure(yscrollcommand=inner_lvl_scr_bar.set)

    inner_lvl_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
    inner_lvl_scr_bar.pack(side=RIGHT, fill=Y)




    notebook_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    notebook_frame.grid(row=1, column=2)

    back_btn = ttk.Button(buttons_frame, text="Назад", command=None)


# Вернуться к предыдущему разделу, спросить о сохранении, в некоторых случаях text_widget=None
def go_to_previous_section(current_table, text_widget):
    try:
        current_note = text_widget.get(1.0, "end").strip()
        if current_note != text_widget.descr_from_base:
            if messagebox.askokcancel("Сохранение",
                                      f"Сохранить изменения в записи {text_widget.table}?"):
                add_description(text_widget, text_widget.table)

    except AttributeError:
        print(AttributeError)

    try:
        parent_table = Data_base[current_table][1]
        layout_frames()
        open_section(parent_table, current_table)
    except KeyError:
        print(KeyError)



# функция для удаления текущего раздела
def ask_delete_section(parent_table, table_name):
    try:
        if messagebox.askokcancel(f'Delete "{table_name}?"',
                                  f'Are you sure you want to delete "{table_name}"'):
            delete_section(table_name)

    except IndexError:
        pass


# Удаление раздела из базы данных и возврат к предыдущему разделу
def delete_section(table_name):
    previous_content = Data_base[table_name]

    try:
        del Data_base[table_name]
        Data_base_temp = dict()
        for i in Data_base:
            Data_base_temp[i] = Data_base[i]
        for i in Data_base_temp:
            if Data_base_temp[i][1] == table_name:
                del Data_base[i]
        with open(Data_base_file, "wb") as f:
            pickle.dump(Data_base, f)
        yadsk.upload()

    except KeyError:
        messagebox.showinfo("Ошибка", "Нельзя удалить основной раздел")

    open_section(Data_base[previous_content[1]][1], previous_content[1])


# вызов класса move section interface
def call_move_section(table_name):
    MoveSectionInterface(table_name)



# Открытие раздела базы данных в интерфейсе (current table - то, где сейчас
# inner table - то, что открываем


def open_section(current_table, inner_table):
    global Data_base
    #  удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками
    layout_frames()

    #  отправляем команду на создание нового фрейма, нового Энтри  для добавления разделов внутрь открываемого
    NewSectionEntry(section_frame, inner_table)


    layout_section_btns(inner_table)


    description_text_widget = DescriptionText(notebook_frame, inner_table)

    back_btn.configure(command=lambda: go_to_previous_section(current_table, description_text_widget))
    back_btn.update()
    back_btn.pack(side=LEFT)


    move_btn = ttk.Button(buttons_frame, text="Переместить текущий раздел",
                          command=lambda: call_move_section(inner_table))
    move_btn.pack(side=LEFT)

    delete_section_btn = ttk.Button(buttons_frame, text="Удалить текущий раздел",
                                    command=lambda: ask_delete_section(current_table,
                                                                       inner_table))
    delete_section_btn.pack(side=LEFT)

    if inner_table == "main":
        back_btn.state(["disabled"])
        move_btn.state(["disabled"])
        delete_section_btn.state(["disabled"])
    else:
        back_btn.state(["!disabled"])
        move_btn.state(["!disabled"])
        delete_section_btn.state(["!disabled"])

    search_btn = ttk.Button(buttons_frame, text="Поиск",
                            command=lambda: layout_search_interface(notebook_frame))
    search_btn.pack(side=RIGHT, pady=(5,0), padx=(10,0))

    current_section_var.set(f"../{current_table[0:10].lower()} /{inner_table[0:10].lower()}")
    current_section_indicator.pack()



def time_to_sec(str_time):
    date = str_time.split(" ")[0]
    date_split = date.split("-")
    days = int(date_split[0]) * 365 * 0.25 + int(date_split[1]) * 30.45 + int(date_split[2])

    time = str_time.split(" ")[1]
    time_split = time.split(":")
    seconds = int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])
    total_seconds = days * 86400 + seconds
    return total_seconds


if __name__ == "__main__":
    global app
    app = App()