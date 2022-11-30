import requests
import json
import tkinter as tk
from tkinter import ttk
from tkinter import *
import urllib3
from io import BytesIO
import PIL
from PIL import Image, ImageTk

url = 'https://pokeapi.co/api/v2/pokemon/'


class Pokedex:
    def __init__(self, root):
        self.root = root
        self.root = root
        self.root.title("Pokédex")
        self.root.geometry("600x500")
        self.root.configure(padx=10, pady=10)

        self.First_Type = StringVar()
        self.Second_Type = StringVar()

        notebook = ttk.Notebook(self.root)
        self.TabControl1 = ttk.Frame(notebook)
        self.TabControl2 = ttk.Frame(notebook)
        notebook.add(self.TabControl1, text='Pokédex Search')
        notebook.add(self.TabControl2, text='Pokédex Catalog')

        notebook.grid()

        MainFrame = Frame(self.TabControl1)
        MainFrame.grid(padx=10, pady=10)

        TopFrame = Frame(MainFrame)
        TopFrame.grid(padx=10, pady=10)

        Tab2Frame = Frame(self.TabControl2, bd=10, width=1350, height=700, relief=RIDGE)
        Tab2Frame.grid(padx=5, pady=10)

        TopFrame11 = Frame(Tab2Frame, bd=10, width=1340, height=60, relief=RIDGE)
        TopFrame11.grid(row=0, column=0)
        TopFrame12 = Frame(Tab2Frame, bd=10, width=280, height=100, relief=RIDGE)
        TopFrame12.grid(row=1, column=0)

        TopFrame12a = Frame(TopFrame12, bd=10, width=1150, height=100, relief=RIDGE)
        TopFrame12a.grid(row=1, column=0)

        TopFrame12b = Frame(TopFrame12, bd=10, width=190, height=100, relief=RIDGE)
        TopFrame12b.grid(row=1, column=1)

        self.title_label = tk.Label(TopFrame, text="Mario's Pokédex")
        self.title_label.config(font=("Arial", 32))
        self.title_label.pack(padx=10, pady=10)

        self.poke_image = tk.Label(TopFrame)
        self.poke_image.pack(padx=10, pady=10)

        self.poke_information = tk.Label(TopFrame)
        self.poke_information.config(font=("Arial", 20))
        self.poke_information.pack(padx=10, pady=10)

        self.poke_types = tk.Label(TopFrame)
        self.poke_types.config(font=("Arial", 20))
        self.poke_types.pack(padx=10, pady=10)

        def get_pokemon():
            self.poke_image.image = None
            self.poke_information.config(text="")
            self.poke_types.config(text="")
            self.poke_image.config(image="")

            pokemon = self.text_id_name.get(1.0, "end-1c")

            if pokemon == '':
                self.poke_information.config(text="No pokemon was entered", fg='Red')
                return

            poke_request = requests.get(url + str(pokemon))
            if poke_request.status_code == 404:
                self.poke_information.config(text="There is no pokemon\nwith that Name or ID", fg='Red')
                return
            poke_reply = json.loads(poke_request.content)

            img_url = poke_reply['sprites']['front_default']
            if img_url is not None:
                http = urllib3.PoolManager()
                response = http.request('GET', img_url)
                sprite = PIL.Image.open(BytesIO(response.data))
                image = PIL.ImageTk.PhotoImage(sprite)
                self.poke_image.config(image=image)
                self.poke_image.image = image
            else:
                self.poke_image.config(text="There is no image\nfor this pokemon", fg='Red')

            self.poke_information.config(text=f"{poke_reply['id']} - {poke_reply['name']}".title(), fg='Black')
            list_types = []
            for poke_type in poke_reply['types']:
                list_types.append(poke_type['type']['name'])
            self.poke_types.config(text=" - ".join([poke_type for poke_type in list_types]).title())

        self.label_id_name = tk.Label(TopFrame, text="ID or Name")
        self.label_id_name.config(font=("Arial", 20))
        self.label_id_name.pack(padx=10, pady=10)

        self.text_id_name = tk.Text(TopFrame, height=1, width=30)
        self.text_id_name.config(font=("Arial", 20))
        self.text_id_name.pack(padx=10, pady=10)

        self.btn_load = tk.Button(TopFrame, text="Load", command=get_pokemon)
        self.btn_load.config(font=("Arial", 20))
        self.btn_load.pack(padx=10, pady=10)

        # TAB 2
        self.lblTitle = Label(TopFrame11, font=('arial', 40, 'bold'), text='Pokémon Database', bd=5,
                              justify=CENTER)
        self.lblTitle.grid(padx=168)

        self.Pokedex_List = ttk.Treeview(TopFrame12a, height=22,
                                         columns=('Name', 'ID', 'Url', 'Types', 'Abilities', 'LocationAreaEncounter'))

        scroll_x = Scrollbar(TopFrame12a, orient=HORIZONTAL, command=self.Pokedex_List.xview)
        scroll_y = Scrollbar(TopFrame12a, orient=VERTICAL, command=self.Pokedex_List.yview)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        self.Pokedex_List.configure(xscrollcommand=scroll_x.set)
        self.Pokedex_List.configure(yscrollcommand=scroll_y.set)

        self.Pokedex_List.heading('Name', text='Name')
        self.Pokedex_List.heading('ID', text='ID')
        self.Pokedex_List.heading('Url', text='Url')
        self.Pokedex_List.heading('Types', text='Types')
        self.Pokedex_List.heading('Abilities', text='Abilities')
        self.Pokedex_List.heading('LocationAreaEncounter', text='Location Area Encounter')

        self.Pokedex_List['show'] = 'headings'

        self.Pokedex_List.column('Name', width=170)
        self.Pokedex_List.column('ID', width=70)
        self.Pokedex_List.column('Url', width=250)
        self.Pokedex_List.column('Types', width=120)
        self.Pokedex_List.column('Abilities', width=250)
        self.Pokedex_List.column('LocationAreaEncounter', width=290)

        self.Pokedex_List.pack(fill=BOTH, expand=1)
        # --------------------------------------------------------------------------------------
        self.First_Type_Label = Label(TopFrame12b, font=('arial', 12, 'bold'), text='Type of the Pokémon:', bd=7,
                                     anchor='w',
                                     justify=LEFT)
        self.First_Type_Label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.cboFirst_Type = ttk.Combobox(TopFrame12b, textvariable=self.First_Type, width=21,
                                            font=('arial', 12, 'bold'), state='readonly')
        self.cboFirst_Type['value'] = ('any', 'normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug', 'ghost',
                                       'steel', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon',
                                       'dark', 'fairy')
        self.cboFirst_Type.current(0)
        self.cboFirst_Type.grid(row=1, column=0)

        def insert_all_pokemons():
            poke_request = requests.get('https://pokeapi.co/api/v2/pokemon?limit=-1')
            poke_reply = json.loads(poke_request.content)
            poke_list = poke_reply['results']
            for poke in poke_list:
                pokemon_full_request = requests.get(poke['url'])
                pokemon_full_reply = json.loads(pokemon_full_request.content)

                list_types = []
                for poke_type in pokemon_full_reply['types']:
                    list_types.append(poke_type['type']['name'])

                list_abilities = []
                for poke_ability in pokemon_full_reply['abilities']:
                    list_abilities.append(poke_ability['ability']['name'])

                self.Pokedex_List.insert("", 'end', values=(pokemon_full_reply['name'], pokemon_full_reply['id'],
                                                            poke['url'],
                                                            " - ".join([poke_type for poke_type in list_types]).title(),
                                                            " - ".join([poke_ab for poke_ab in list_abilities]).title(),
                                                            pokemon_full_reply['location_area_encounters']))

        def insert_pokemon_by_type():
            self.Pokedex_List.delete(*self.Pokedex_List.get_children())

            poke_type = self.First_Type.get()

            if poke_type == 'any':
                insert_all_pokemons()
                return

            poke_request = requests.get("https://pokeapi.co/api/v2/type/" + str(poke_type))
            poke_reply = json.loads(poke_request.content)
            for poke in poke_reply['pokemon']:
                pokemon_full_request = requests.get(poke['pokemon']['url'])
                pokemon_full_reply = json.loads(pokemon_full_request.content)

                list_types = []
                for poke_type in pokemon_full_reply['types']:
                    list_types.append(poke_type['type']['name'])

                list_abilities = []
                for poke_ability in pokemon_full_reply['abilities']:
                    list_abilities.append(poke_ability['ability']['name'])

                self.Pokedex_List.insert("", 'end', values=(pokemon_full_reply['name'], pokemon_full_reply['id'],
                                                            poke['pokemon']['url'],
                                                            " - ".join([poke_type for poke_type in list_types]).title(),
                                                            " - ".join([poke_ab for poke_ab in list_abilities]).title(),
                                                            pokemon_full_reply['location_area_encounters']))

        self.btn_search_type = tk.Button(TopFrame12b, text="Load", command=insert_pokemon_by_type)
        self.btn_search_type.config(font=("Arial", 20))
        self.btn_search_type.grid(row=2, column=0)


if __name__ == '__main__':
    root = tk.Tk()
    application = Pokedex(root)
    root.mainloop()
