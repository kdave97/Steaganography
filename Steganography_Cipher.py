"""
Created on Thu Apr 19 07:44:50 2018

@author: karan
"""

from tkinter import * 
from PIL import Image
from tkinter import messagebox
from tkinter.filedialog import askopenfilename 
import binascii
import optparse	

global name

def encrypt_gui():
	global root
	global root1
	global ee1,ee2,name
	root.destroy()
	root1=Tk()
	root1.title("Encrypt")
	root1.geometry("480x360")
	L1=Label(root1,text="File",font=("bold",15))
	L1.place(x=60,y=110)
	ee1=Entry(root1,width=20,font=("bold",15))
	ee1.place(x=160,y=110)
	b1=Button(root1,text="Browse",command=eopen_file)
	b1.place(x=400,y=110)
	
	L2=Label(root1,text="Message",font=("bold",15))
	L2.place(x=60,y=150)
	ee2=Entry(root1,width=20,font=("bold",15))
	ee2.place(x=160,y=150)
	
	b3=Button(root1,text="Encrypt Image",width=25,command=encrypt_data).place(x=140,y=200)
	
	root1.mainloop()

def decrypt_gui():
	global root
	global root2
	global ed1,name
	root.destroy()
	root2=Tk()
	root2.title("Decrypt")
	root2.geometry("480x360")
	L1=Label(root2,text="File",font=("bold",15))
	L1.place(x=60,y=110)
	ed1=Entry(root2,width=20,font=("bold",15))
	ed1.place(x=160,y=110)
	
	b1=Button(root2,text="Browse",command=dopen_file)
	b1.place(x=400,y=110)
	
	b4=Button(root2,text="Decrypt Image",width=25,command=decrypt_data).place(x=140,y=150)
	
	root2.mainloop()



def eopen_file():
	global ee1
	name = askopenfilename(initialdir="/",filetypes =(("PNG File", "*.png"),("All Files","*.*")),title = "Choose a file.") 
	ee1.insert(END,name)
	
def dopen_file():
	global ed1
	name = askopenfilename(initialdir="/",filetypes =(("PNG File", "*.png"),("All Files","*.*")),title = "Choose a file.") 
	ed1.insert(END,name)
	
def encrypt_data():
	global root1
	global ee1,ee2
	
	fname=ee1.get()
	msg=ee2.get()

	var=hide(fname,msg)
	messagebox.showinfo("Status", var)
	root1.destroy()
	
	ste()
	

def decrypt_data():
	global ed1;
	fname=ed1.get()
	
	var=retr(fname)
	messagebox.showinfo("Text", var)
	root2.destroy()
	
	ste()
	

#------------------------------------------------------"""Steganography"""------------------------------

def rgb2hex(r,g,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

	
def hex2rgb(hexcode):
	hexcode=hexcode.lstrip('#')
	rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2 ,4))
	return rgb
	
def str2bin(message):
	binary=bin(int.from_bytes(message.encode(), 'big'))
	return binary[2:]
		
def bin2str(binary):
	message=binascii.unhexlify('%x' %(int('0b'+binary, 2)))
	return message
	
def encode(hexcode,digit):
	if hexcode[-1] in ('0','1','2','3','4','5'):
			hexcode=hexcode[:-1]+digit
			return hexcode
	else:
		return None
		
def decode(hexcode):
	if hexcode[-1] in ('0','1'):
		return hexcode[-1]
	else:
		return None
		
def hide(filename, message):
	img=Image.open(filename)
	binary=str2bin(message)+ '1111111111111110'
	if img.mode in ('RGBA'):
		img=img.convert('RGBA')
		datas=img.getdata()
		
		newData=[]
		digit=0
		temp=''
		for item in datas:
			if (digit<len(binary)):
				newpix=encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
				if newpix==None:
					newData.append(item)
				else:
					r,g,b=hex2rgb(newpix)
					newData.append((r,g,b,255))
					digit+=1
			else:
					newData.append(item)
		img.putdata(newData)
		img.save(filename,"PNG")
		return "Completed!"
	return "Incorrect image mode"	
	

def retr(filename):
	img=Image.open(filename)
	binary=''
	
	if img.mode in ('RGBA'):
		img=img.convert('RGBA')
		datas=img.getdata()
		
		for item in datas:
			digit=decode(rgb2hex(item[0],item[1],item[2]))
			if digit==None:
				pass
			else:
				binary=binary+digit
				if (binary[-16:]=='1111111111111110'):
					print ("Success")
					return bin2str(binary[:-16])
					
		return bin2str(binary)

	return "Incorrect Image mode"

#--------------------------------------------------------------------------------------------------------------------
	
def destroy():
	global window
	window.destroy()
	ste()
	
def ste():
	global root
	root=Tk()
	root.geometry("480x360")
	b1=Button(root,text="Encrypt",width=30,font=('times',15,'italic'),command=encrypt_gui).place(x=100,y=100)
	b2=Button(root,text="Decrypt",width=30,font=('times',15,'italic'),command=decrypt_gui).place(x=100,y=200)
	B3=Button(root,text="Main Menu",width=30,font=('times',15,'italic'),command=main_menu).place(x=100,y=300)
	
	root.mainloop()			

def main_menu():
	global root
	root.destroy()
	main()	

#------------------------------------------------------------------"""cipher"""-------------------------------	
	
def cipher():
	global window
	window.destroy()
	rootc=Tk()
	rootc.title("Encrypter/Decrypter")
	label_1=Label(rootc,text="Full path of text file")
	label_2=Label(rootc,text="Key")
	entry_1 = Entry(rootc)
	entry_2 = Entry(rootc)

	label_1.grid(row=0, column=0)
	label_2.grid(row=1, column=0)
	entry_1.grid(row=0, column=1)
	entry_2.grid(row=1, column=1)
	
	Button(rootc, text="Decrypt",command=decrypter).grid(row=2,column=1)
	Button(rootc, text="Encrypt",command=encrypter).grid(row=2,column=0)
	rootc.mainloop()
	
def encrypter():

	global entry_1,entry_2
	key=int(entry_2.get())
	path=str(entry_1.get())
	f1=open('Result.txt','w+')
	with open('test.txt')as f:
		for line in f:
			a=line.split(' ')
			for words in a:
				for letter in words:
					if letter.isalpha():
						print(letter,ord(letter))
						if 65<=ord(letter)<=92:
							new_l=chr(65+((ord(letter)-65+key)%26))
						elif 97<=ord(letter)<=124:
							new_l=chr(97+((ord(letter)-97+key)%26))
					else:
						new_l=letter
					f1.write(new_l)
				if letter.isalpha():
					f1.write(' ')
				else: pass
	print('Done Successfully1!')
def decrypter():
	global entry_1,entry_2
	key=int(entry_2.get())
	path=str(entry_1.get())
	f1=open('Result.txt','w+')
	with open(path)as f:
		for line in f:
			a=line.split(' ')
			for words in a:
				for letter in words:
					if letter.isalpha():
						print(letter,ord(letter))
						if 65<=ord(letter)<=92:
							new_l=chr(65+((26+ord(letter)-65-key)%26))
						elif 97<=ord(letter)<=124:
							new_l=chr(97+((26+ord(letter)-97-key)%26))
					else:
						new_l=letter
					f1.write(new_l)
				if letter.isalpha():
					f1.write(' ')
				else: pass
	print('Done Successfully1!')
	
#-------------------------------------------------------------------------------------------------------------------------------------	

def main():
	global window
	window=Tk()
	window.geometry("480x360")
	window.title("Inteface")
	b1=Button(window,text="Cipher",width=30,font=('times',15,'italic'),command=cipher).place(x=100,y=100)
	b2=Button(window,text="Steganography",width=30,font=('times',15,'italic'),command=destroy).place(x=100,y=200)
	b3=Button(window,text="Quit",width=30,font=('times',15,'italic'),command=window.destroy).place(x=100,y=300)
	
	window.mainloop()
	
main()		