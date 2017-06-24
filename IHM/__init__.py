from Tkinter import *
import tkMessageBox, tkFileDialog, configuration, user, encrypt, ttk, file, shutil, os

class interface:

    def __init__(self, view ='root', attr = None):
        self.session = attr
        view_func = self.view_exist(view)
        if view_func:
            self.active = dict()
            self.active[view] = None
            print self.active
            view_func()

    def view_exist(self, view_name):
        try:
            view = getattr(self, view_name)
        except Exception:
            raise ValueError('UNKNOWN VIEW')
        return view

    def change(self, new_active_view):
        view = self.view_exist(new_active_view)
        for active_view in self.active.keys():
            print type(self.active[active_view])
            if type(self.active[active_view]) is not NoneType:
                self.active[active_view].destroy()
        if view:
            self.active[new_active_view] = None
            view()

    #VIEW

    def root(self):
        root = Tk()
        root.title('Vault - Connexion')

        root.geometry("300x200")

        username_pane = LabelFrame(root, labelanchor='nw', text='Username')
        username = Entry(username_pane, textvariable = StringVar())
        username.pack()
        username_pane.pack()

        password_pane = LabelFrame(root, labelanchor='nw', text='Password')
        password = Entry(password_pane, textvariable = StringVar(), show='*')
        password.pack()
        password_pane.pack()

        def connection_on_click():
            try:
                self.session['user'].connect(username.get(),password.get())
                self.loading_main()
            except Exception as e:
                tkMessageBox.showerror('Error', e.message)

        def subscribe_on_click():
            try:
                test = self.session['user'].inscription(username.get(),password.get(), verify_password.get())
                if test:
                    self.change('root')
            except Exception as e:
                tkMessageBox.showerror('Error', e.message)


        if (self.session['user']._get_name() == '<USER_NAME>'):
            verify_password_pane = LabelFrame(root, labelanchor='nw', text='Verify Password')
            verify_password = Entry(verify_password_pane, textvariable = StringVar(), show='*')
            verify_password.pack()
            verify_password_pane.pack()
            valid_button = Button(root, text="S'inscrire", command=subscribe_on_click)
        else:
            valid_button = Button(root, text="Se connecter", command=connection_on_click)
        valid_button.pack()


        self.active['root'] = root
        print self.active

        root.mainloop()

    def loading_main(self):
        app_conf = configuration.Configuration('./configuration/conf.json')
        self.session['encryptor'] = encrypt.encryptor(app_conf)

        file_list = configuration.Configuration('./configuration/file.conf.json')
        self.session['files'] = file.FilesList(file_list)

        for file_o in file_list.get('files'):
            self.session['files'].add_file(file.File(file_o['name'], file_o['encrypted_name'], file_o['algo'], file_o['key']))

        self.change('main')


    def main(self):
        root = Tk()
        root.title('Vault')

        root.geometry("300x200")
        root.resizable(False, False)

        print root.grid()

        list_var = StringVar()
        file_listbox = Listbox(root, listvariable = list_var, width=30, exportselection = 0, selectmode = 'single')

        for file_o in self.session['files'].files:
            file_listbox.insert('end', file_o.source_name)

        file_listbox.pack(side=LEFT, anchor=NW, padx= 10)

        ##HANDLER
        def button_suppr_file():
            index_selection = file_listbox.curselection()
            if index_selection:
                file_name = file_listbox.get(index_selection)
                encrypted_file_name = self.session['files'].get_file(file_name)['encrypted_name']
                try:
                    self.session['encryptor'].del_encrypted_file(encrypted_file_name)
                except Exception as e:
                    print e
                    return tkMessageBox.showerror('Error', e.message)
                self.session['files'].del_file(file_name)
                file_listbox.delete(index_selection)

        def button_add_file():
            new_file = tkFileDialog.askopenfile(title="Selectionner un fichier", initialdir='/')
            new_file_name = os.path.basename(new_file.name)
            for file_o in self.session['files'].files:
                if file_o.source_name == new_file_name:
                    return tkMessageBox.showerror('Already exist', 'un fichier portant ce nom existe deja')
            shutil.copyfile(new_file.name, self.session['encryptor'].in_directory + '/' + new_file_name)
            file_key = self.session['encryptor'].file_name_generator(16)
            encrypted_file_name = self.session['encryptor'].file_name_generator()
            self.session['encryptor'].encrypt_file(file_key, new_file_name, encrypted_file_name)
            self.session['files'].add_file(file.File(new_file_name, encrypted_file_name + '.enc', self.session['encryptor'].conf.get('file').get('encrypt'), file_key))
            file_listbox.insert('end', new_file_name)
            os.remove(self.session['encryptor'].in_directory + '/' + new_file_name)

        def button_get_file():
            index_selection = file_listbox.curselection()
            if index_selection:
                file_name = file_listbox.get(index_selection)
                stored_file = self.session['files'].get_file(file_name)
                if stored_file:
                    self.session['encryptor'].decrypt_file(stored_file['key'], stored_file['encrypted_name'], stored_file['name'])
                    out_new_file = tkFileDialog.askdirectory(title="Selectionner un fichier", initialdir='/')
                    shutil.copyfile(self.session['encryptor'].in_directory + '/' + stored_file['name'], out_new_file + '/' + stored_file['name'])
                    os.remove(self.session['encryptor'].in_directory + '/' + stored_file['name'])

        def save():
            for instance in self.session:
                self.session[instance].save()
            root.destroy()

        add_button = Button(root, text='ajouter', command = button_add_file)
        add_button.pack()

        suppr_button = Button(root, text='supprimer', command = button_suppr_file)
        suppr_button.pack()

        get_button = Button(root, text='recuperer', command = button_get_file)
        get_button.pack()

        root.protocol('WM_DELETE_WINDOW', save)

        root.mainloop()
