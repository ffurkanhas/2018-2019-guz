#!/usr/bin/env python3

import tkinter as tki # Tkinter -> tkinter in Python3
from tkinter import Button, ttk
import os

alphabet = '0123456789abcçdefgğhıijklmnoöpqrsştuüvwxyzABCÇDEFGHIİJKLMNOÖPQRSŞTUÜVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ' + os.linesep
substitutionKey = "]kYV}(!7P$n5_0iR:?jOWtF/=-pe'AD&@r6%ZXs\"v*N[#wSl9zq2^+g;LoB`aGh{3.HIu4fbK)mU8|dMET><,Qc\]^_`fgğhı./:;<=>c " + os.linesep

class App(object):

    def __init__(self):
        self.root = tki.Tk()
        self.root.resizable(width=False, height=False)
        self.root.title("Sifreleyici")

    # create a Frame for the plaintext
        encodeFrame = tki.Frame(self.root)
        encodeFrame.pack(fill="both", expand=True)
        encodeFrame.grid_rowconfigure(0, weight=1)
        encodeFrame.grid_columnconfigure(0, weight=1)

    # create a Frame for buttons
        buttonFrame = tki.Frame(self.root)
        buttonFrame.pack(fill="both", padx=(45,0))

    # create a Frame for ciphertext
        decodeFrame = tki.Frame(self.root)
        decodeFrame.pack(fill="both", expand=True)
        decodeFrame.grid_rowconfigure(0, weight=1)
        decodeFrame.grid_columnconfigure(0, weight=1)

    # create a Text widget for encode
        self.plainText = tki.Text(encodeFrame, width=100, height = 15)
        self.plainText.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

    # create a Scrollbar and associate it with txt for encode
        plainTextScrollbar = tki.Scrollbar(encodeFrame, command=self.plainText.yview)
        plainTextScrollbar.place(in_=self.plainText, relx=1.0, relheight=1.0, bordermode="outside")
        self.plainText['yscrollcommand'] = plainTextScrollbar.set

    # create a Text widget for decode
        self.cipherText = tki.Text(decodeFrame, width=100, height = 15)
        self.cipherText.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

    # create a Scrollbar and associate it with txt for decode
        cipherTextScrollBar = tki.Scrollbar(decodeFrame, command=self.cipherText.yview)
        cipherTextScrollBar.place(in_=self.cipherText, relx=1.0, relheight=1.0, bordermode="outside")
        self.cipherText['yscrollcommand'] = cipherTextScrollBar.set

    #create comboBox
        self.encryptionMethods = ['Shift (Caesar)', 'Substitution', 'Affine', 'Vigenere']
        self.encodeMethodComboBox = ttk.Combobox(buttonFrame, width=30)
        self.encodeMethodComboBox.bind("<<ComboboxSelected>>", self.comboUpdateKeys)
        self.encodeMethodComboBox.grid(row=0, column=0, padx=(10,0), sticky='w')
        self.encodeMethodComboBox['values'] = self.encryptionMethods
        self.encodeMethodComboBox.set(self.encryptionMethods[0])


    #create key texts
        self.publicKey = tki.Text(buttonFrame, width=25, height=1)
        self.publicKey.place(x=300, y=0)

        self.privateKey = tki.Text(buttonFrame, width=25, height=1)
        self.privateKey.place(x=520, y=0)

    #disable text areas as default
        self.publicKey.insert(tki.END, "1")
        self.privateKey.configure(state='disabled')

    #create buttons
        self.encode = Button(buttonFrame, text="Sifrele", fg="orange", width=30, command = lambda :ceaserEncode(self, int(self.publicKey.get("1.0", tki.END))))
        self.encode.place(x=0, y=30)

        self.decode = Button(buttonFrame, text="Sifreyi Coz", fg="orange", width=30,  command = lambda :ceaserDecode(self, int(self.publicKey.get("1.0", tki.END))))
        self.decode.grid(row=1, column=1, padx=(20,0), pady=(10,0))

    def comboUpdateKeys(self, event=None):
        self.publicKey.delete('1.0', tki.END)
        self.privateKey.delete('1.0', tki.END)
        if event.widget.get() == self.encryptionMethods[0]:
            self.publicKey.configure(state='normal')
            self.publicKey.insert(tki.END, "1")
            self.privateKey.configure(state='disabled')
            self.encode.configure(command = lambda :ceaserEncode(self, int(self.publicKey.get("1.0", tki.END))))
            self.decode.configure(command=lambda: ceaserDecode(self, int(self.publicKey.get("1.0", tki.END))))
        if event.widget.get() == self.encryptionMethods[1]:
            self.privateKey.configure(state='disabled')
            self.publicKey.configure(state='disabled')
            self.encode.configure(command = lambda :substitutionEncode(self))
            self.decode.configure(command=lambda: substitutionDecode(self))
        if event.widget.get() == self.encryptionMethods[2]:
            self.publicKey.configure(state='normal')
            self.publicKey.insert(tki.END, "1")
            self.privateKey.configure(state='normal')
            self.privateKey.insert(tki.END, "1")
            self.encode.configure(command=lambda: affineEncode(self, int(self.publicKey.get("1.0", tki.END)), int(self.privateKey.get("1.0", tki.END))))
            self.decode.configure(command=lambda: affineDecode(self, int(self.publicKey.get("1.0", tki.END)),int(self.privateKey.get("1.0", tki.END))))
        if event.widget.get() == self.encryptionMethods[3]:
            self.publicKey.insert(tki.END, "key")
            self.privateKey.configure(state='normal')
            self.privateKey.configure(state='disabled')
            self.encode.configure(command = lambda: vigenereEncode(self, self.publicKey.get("1.0", tki.END)))
            self.decode.configure(command=lambda: vigenereDecode(self, self.publicKey.get("1.0", tki.END)))

def encode(App):
    App.cipherText.delete('1.0', tki.END)
    App.cipherText.insert(tki.END, App.plainText.get("1.0", tki.END))

def decode(App):
    App.plainText.delete('1.0', tki.END)
    App.plainText.insert(tki.END, App.cipherText.get("1.0", tki.END))

def ceaserEncode(App, key):
    plaintext = App.plainText.get("1.0", tki.END)
    cipherText = ""
    for i in range(0, len(plaintext) - 1):
        char = plaintext[i]
        if (char in alphabet):
            index = alphabet.index(char)
            cipherText += alphabet[(index + int(key)) % len(alphabet)]
        else:
            cipherText += char
    App.cipherText.delete('1.0', tki.END)
    App.cipherText.insert(tki.END, cipherText)

def ceaserDecode(App, key):
    cipherText = App.cipherText.get("1.0", tki.END)
    plainText = ""
    for i in range(0, len(cipherText) - 1):
        char = cipherText[i]
        if (char in alphabet):
            index = alphabet.index(char)
            plainText += alphabet[(index - int(key)) % len(alphabet)]
        else:
            plainText += char
    App.plainText.delete('1.0', tki.END)
    App.plainText.insert(tki.END, plainText)

def substitutionEncode(App):
    plaintext = App.plainText.get("1.0", tki.END)
    cipherText = ""
    for i in range(0, len(plaintext) - 1):
        char = plaintext[i]
        index = alphabet.index(char)
        cipherText += substitutionKey[index]
    App.cipherText.delete('1.0', tki.END)
    App.cipherText.insert(tki.END, cipherText)

def substitutionDecode(App):
    cipherText = App.cipherText.get("1.0", tki.END)
    plainText = ""
    for i in range(0, len(cipherText) - 1):
        char = cipherText[i]
        index = substitutionKey.index(char)
        plainText += alphabet[index]
    App.plainText.delete('1.0', tki.END)
    App.plainText.insert(tki.END, plainText)

def affineEncode(App, key1, key2):
    plaintext = App.plainText.get("1.0", tki.END)
    cipherText = ""
    for i in range(0, len(plaintext) - 1):
        char = plaintext[i]
        if (char in alphabet):
            index = alphabet.index(char)
            cipherText += alphabet[((int(key1) * index) + int(key2)) % len(alphabet)]
        else:
            cipherText += char
    App.cipherText.delete('1.0', tki.END)
    App.cipherText.insert(tki.END, cipherText)

def affineDecode(App, key1, key2):
    cipherText = App.cipherText.get("1.0", tki.END)
    plainText = ""
    for i in range(0, len(cipherText) - 1):
        char = cipherText[i]
        modInverse = findModInverse(int(key1), len(alphabet))
        if (char in alphabet):
            index = alphabet.index(char)
            plainText += alphabet[((((index - int(key2)) * modInverse)) % len(alphabet))]
        else:
            plainText += char
    App.plainText.delete('1.0', tki.END)
    App.plainText.insert(tki.END, plainText)

def vigenereEncode(App, key):
    plaintext = App.plainText.get("1.0", tki.END)
    key = key[:len(key)-1]
    cipherText = ""
    tempKey = ""
    for i in range(0, len(plaintext) - 1):
        if (key[i % len(key)] == os.linesep):
            tempKey += ""
        else:
            tempKey += key[i % len(key)]
    for i in range(0, len(plaintext) - 1):
        char = plaintext[i]
        index = alphabet.index(char)
        cipherIndex = alphabet.index(tempKey[i])
        if (index + cipherIndex >= len(alphabet)):
            cipherText += alphabet[(index + cipherIndex) % len(alphabet)]
        else:
            cipherText += alphabet[index + cipherIndex]
    App.cipherText.delete('1.0', tki.END)
    App.cipherText.insert(tki.END, cipherText)

def vigenereDecode(App, key):
    cipherText = App.cipherText.get("1.0", tki.END)
    key = key[:len(key)-1]
    plainText = ""
    tempKey = ""
    for i in range(0, len(cipherText) - 1):
        if (key[i % len(key)] == os.linesep):
            tempKey += ""
        else:
            tempKey += key[i % len(key)]
    for i in range(0, len(cipherText) - 1):
        char = cipherText[i]
        index = alphabet.index(char)
        cipherIndex = alphabet.index(tempKey[i])
        if (index - cipherIndex <= len(alphabet)):
            plainText += alphabet[(index - cipherIndex) % len(alphabet)]
        else:
            plainText += alphabet[index - cipherIndex]
    App.plainText.delete('1.0', tki.END)
    App.plainText.insert(tki.END, plainText)

#ters mod islemini https://inventwithpython.com/cryptomath.py adresinden aldim
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

if(__name__ == '__main__'):
    app = App()
    app.root.mainloop()
