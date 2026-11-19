import tkinter as tk
from tkinter import ttk, messagebox
import random

APP_TITLE = "BÚSQUEDA MEDIANTE TABLA HASH"
SUBTITLE = "Consulta una clave mediante una tabla hash (diccionario)."
MODE = "hash"

BG="#0f172a"; PANEL="#172338"; PANEL2="#1e293b"
CYAN="#22d3ee"; PURPLE="#a78bfa"; GREEN="#34d399"; RED="#fb7185"
WHITE="#f8fafc"; MUTED="#94a3b8"
FONT=("Segoe UI", 10)

class SearchApp:
    def __init__(self, root):
        self.root=root
        self.root.title(APP_TITLE)
        self.root.geometry("960x700")
        self.root.minsize(850,640)
        self.root.configure(bg=BG)
        self.data=[]
        self.after_id=None
        self.steps=[]
        self.step_index=0
        self.found=False
        self.build()
        self.refresh()

    def button(self, parent, text, command, fg, bg):
        return tk.Button(parent,text=text,command=command,bg=bg,fg=fg,
            activebackground=bg,activeforeground=WHITE,relief="flat",bd=0,
            padx=13,pady=8,font=("Segoe UI",9,"bold"),cursor="hand2")

    def build(self):
        style=ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background=PANEL2,foreground=WHITE,
                        fieldbackground=PANEL2,rowheight=27)
        header=tk.Frame(self.root,bg=BG); header.pack(fill="x",padx=24,pady=(18,8))
        tk.Label(header,text="⌕  "+APP_TITLE,bg=BG,fg=WHITE,
                 font=("Segoe UI",21,"bold")).pack(anchor="w")
        tk.Label(header,text=SUBTITLE,bg=BG,fg=CYAN,
                 font=("Segoe UI",10)).pack(anchor="w",pady=(3,0))

        data=tk.Frame(self.root,bg=PANEL,padx=16,pady=13)
        data.pack(fill="x",padx=24,pady=8)
        tk.Label(data,text="1. PREPARAR LOS DATOS",bg=PANEL,fg=CYAN,
                 font=("Segoe UI",9,"bold")).grid(row=0,column=0,columnspan=5,sticky="w")
        tk.Label(data,text="Escribe números separados por comas:",bg=PANEL,fg=WHITE).grid(row=1,column=0,sticky="w",pady=(10,4))
        self.entry=tk.Entry(data,bg=PANEL2,fg=WHITE,insertbackground=WHITE,relief="flat",font=FONT,width=55)
        self.entry.grid(row=2,column=0,columnspan=3,sticky="ew",ipady=8,padx=(0,8))
        self.entry.insert(0,"18, 7, 25, 4, 13, 31, 9")
        self.button(data,"CARGAR NÚMEROS",self.load,CYAN,"#083344").grid(row=2,column=3,padx=4)
        self.button(data,"GENERAR ALEATORIOS",self.random_data,PURPLE,"#3b0764").grid(row=2,column=4,padx=4)
        tk.Label(data,text="Cantidad aleatoria:",bg=PANEL,fg=MUTED).grid(row=3,column=0,sticky="w",pady=(10,0))
        self.count=tk.StringVar(value="12")
        tk.Spinbox(data,from_=3,to=30,textvariable=self.count,width=6,bg=PANEL2,fg=WHITE,
                   buttonbackground=PANEL2,relief="flat").grid(row=4,column=0,sticky="w")

        search=tk.Frame(self.root,bg=PANEL,padx=16,pady=13)
        search.pack(fill="x",padx=24,pady=8)
        tk.Label(search,text="2. REALIZAR LA BÚSQUEDA",bg=PANEL,fg=PURPLE,
                 font=("Segoe UI",9,"bold")).grid(row=0,column=0,columnspan=4,sticky="w")
        tk.Label(search,text="Número a buscar:",bg=PANEL,fg=WHITE).grid(row=1,column=0,sticky="w",pady=(9,4))
        self.target=tk.Entry(search,bg=PANEL2,fg=WHITE,insertbackground=WHITE,relief="flat",width=16,font=FONT)
        self.target.grid(row=2,column=0,sticky="w",ipady=7,padx=(0,8))
        self.button(search,"INICIAR",self.start,GREEN,"#064e3b").grid(row=2,column=1,padx=4)
        self.button(search,"DETENER",self.stop,RED,"#881337").grid(row=2,column=2,padx=4)
        self.button(search,"LIMPIAR",self.clear_result,"#cbd5e1","#334155").grid(row=2,column=3,padx=4)

        body=tk.Frame(self.root,bg=BG); body.pack(fill="both",expand=True,padx=24,pady=8)
        left=tk.Frame(body,bg=PANEL,padx=14,pady=12); left.pack(side="left",fill="both",expand=True,padx=(0,8))
        right=tk.Frame(body,bg=PANEL,padx=14,pady=12); right.pack(side="right",fill="both",expand=True,padx=(8,0))
        tk.Label(left,text="LISTA DE ELEMENTOS",bg=PANEL,fg=CYAN,font=("Segoe UI",9,"bold")).pack(anchor="w")
        self.data_view=tk.Label(left,text="",bg=PANEL2,fg=WHITE,font=("Consolas",12,"bold"),
                                justify="left",wraplength=480,padx=12,pady=16)
        self.data_view.pack(fill="x",pady=10)
        tk.Label(left,text="AVANCE",bg=PANEL,fg=PURPLE,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(8,4))
        self.progress=ttk.Progressbar(left,mode="determinate",maximum=100)
        self.progress.pack(fill="x",pady=(0,10))
        self.status=tk.Label(left,text="Carga una lista o genera números aleatorios.",bg=PANEL,fg=MUTED,
                             wraplength=480,justify="left")
        self.status.pack(anchor="w",pady=5)
        tk.Label(right,text="PASOS DEL ALGORITMO",bg=PANEL,fg=CYAN,font=("Segoe UI",9,"bold")).pack(anchor="w")
        self.log=tk.Listbox(right,bg=PANEL2,fg=WHITE,selectbackground="#155e75",relief="flat",
                            font=("Consolas",9),height=14)
        self.log.pack(fill="both",expand=True,pady=10)
        self.result=tk.Label(right,text="RESULTADO: —",bg=PANEL2,fg=GREEN,font=("Segoe UI",11,"bold"),
                             padx=10,pady=12,wraplength=290,justify="left")
        self.result.pack(fill="x")
        tk.Label(self.root,text="ALGORITMOS DE BÚSQUEDA  •  Python + Tkinter",
                 bg=BG,fg=MUTED,font=("Segoe UI",8)).pack(pady=(0,10))

    def refresh(self):
        values=self.visual_values()
        self.data_view.config(text="[  "+"   ".join(map(str,values))+"  ]" if values else "Sin datos.")
        self.progress["value"]=0

    def visual_values(self):
        return sorted(self.data) if MODE=="binaria" else self.data

    def load(self):
        try:
            values=[int(x.strip()) for x in self.entry.get().split(",") if x.strip()]
            if not values: raise ValueError
            if len(values)>100: raise ValueError
            self.stop(); self.data=values; self.clear_result(); self.refresh()
            self.status.config(text=f"Lista cargada: {len(values)} números.")
        except ValueError:
            messagebox.showerror("Entrada incorrecta","Escribe entre 1 y 100 números enteros separados por comas.")

    def random_data(self):
        try:
            n=int(self.count.get())
            if not 3<=n<=30: raise ValueError
            self.stop(); self.data=random.sample(range(1,100),n)
            self.entry.delete(0,"end"); self.entry.insert(0,", ".join(map(str,self.data)))
            self.clear_result(); self.refresh()
            self.status.config(text=f"Se generaron {n} números aleatorios.")
        except ValueError:
            messagebox.showerror("Cantidad incorrecta","Selecciona una cantidad entre 3 y 30.")

    def clear_result(self):
        self.log.delete(0,"end"); self.result.config(text="RESULTADO: —",fg=GREEN)
        self.progress["value"]=0

    def stop(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id); self.after_id=None

    def start(self):
        if not self.data:
            messagebox.showinfo("Faltan datos","Primero carga o genera una lista."); return
        try: target=int(self.target.get().strip())
        except ValueError:
            messagebox.showerror("Dato incorrecto","Escribe un número entero para buscar."); return
        self.stop(); self.clear_result()
        self.steps=self.create_steps(target); self.step_index=0; self.found=False
        self.status.config(text="El algoritmo está trabajando...")
        self.animate()

    def create_steps(self,target):
        steps=[]
        if MODE=="secuencial":
            for i,v in enumerate(self.data):
                ok=v==target
                steps.append((f"Paso {i+1:02d}: revisar índice {i} → {v}"+("  ✓" if ok else ""),
                              int((i+1)/len(self.data)*100),ok,
                              f"Encontrado en índice {i} (posición {i+1})." if ok else ""))
                if ok: break
        elif MODE=="binaria":
            arr=sorted(self.data); lo=0; hi=len(arr)-1; count=0
            while lo<=hi:
                count+=1; mid=(lo+hi)//2; v=arr[mid]; ok=v==target
                if ok:
                    steps.append((f"Paso {count}: centro={v} → ENCONTRADO",100,True,
                                  f"Encontrado en índice {mid} de la lista ordenada (posición {mid+1})."))
                    break
                if v<target:
                    steps.append((f"Paso {count}: centro={v}; buscar a la DERECHA",min(95,count*25),False,""))
                    lo=mid+1
                else:
                    steps.append((f"Paso {count}: centro={v}; buscar a la IZQUIERDA",min(95,count*25),False,""))
                    hi=mid-1
        else:
            table={v:i for i,v in enumerate(self.data)}
            for key,index in table.items():
                steps.append((f"Tabla: clave {key} → índice {index}",0,False,""))
            if target in table:
                i=table[target]
                steps.append((f"Acceso directo a la clave {target}  ✓",100,True,
                              f"Encontrado: clave {target}, índice {i} (posición {i+1})."))
            else:
                steps.append((f"La clave {target} no está en la tabla.",100,False,""))
        return steps

    def animate(self):
        if self.step_index>=len(self.steps):
            if self.found:
                self.result.config(text="RESULTADO: "+self.final_result,fg=GREEN)
                self.status.config(text="Búsqueda terminada. Elemento localizado.")
            else:
                self.result.config(text="RESULTADO: número no encontrado.",fg=RED)
                self.status.config(text="Búsqueda terminada. No se encontró el número.")
            self.after_id=None; return
        line,pct,found,detail=self.steps[self.step_index]
        self.log.insert("end",line); self.log.yview_moveto(1)
        self.progress["value"]=pct
        if found: self.found=True; self.final_result=detail
        self.step_index+=1
        self.after_id=self.root.after(420,self.animate)

if __name__=="__main__":
    root=tk.Tk()
    app=SearchApp(root)
    root.mainloop()
