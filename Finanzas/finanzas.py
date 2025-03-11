import customtkinter as ctk
import sqlite3
import tkinter as tk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

class FinanzaSeccion:    
    def __init__(self,parent):
        self.parent = parent
        self.tree = None
        
    def render(self):
        pass