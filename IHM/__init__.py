from Tkinter import *
import tkMessageBox, configuration, user, encrypt, ttk, file

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
            self.active[active_view].destroy()
        if view:
            self.active[new_active_view] = None
            view()

    #VIEW

    def root(self):
        root = Tk()
        root.title('Vault - Connexion')

        root.geometry("500x200")

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

        root.geometry("500x200")



        root.mainloop()
