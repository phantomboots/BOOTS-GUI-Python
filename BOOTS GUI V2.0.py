# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:07:12 2020

@author: Acoustics_NDST
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pygame
import socket
import ncd_industrial_relay as ncd
import datetime
import string

#Initialize F310 joystick and display_init() for pygame's event pump function.
pygame.display.init()
pygame.joystick.init()

try:
    F310 = pygame.joystick.Joystick(0)
    F310.init()
except:
    pass

                                                                

#######################################################################################################################################
###                     Main GUI class
#######################################################################################################################################


    
class MainWindow(tk.Frame, socket.socket):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        socket.socket.__init__(self)
        self.parent = parent
        self.parent.title("BOOTS Control V2.0")
        #Overwrite default shutdown behaviour
        self.parent.protocol("WM_DELETE_WINDOW" , self.CloseProgram)
        self.parent.geometry("800x600")
        
        #Create secondary window, for active program status printing
        self.secondary_window = tk.Toplevel()
        self.secondary_window.title("Program Status")
        self.secondary_window.config(width=400, height=200)
        self.status_scroll = tk.Scrollbar(self.secondary_window)
        self.status_scroll.grid(row = 0, column = 1)
        
        #Fill secondary window with an entry widget
        self.program_status = tk.Text(self.secondary_window, height = 60, width = 100)
        self.program_status.grid(row=0, column=0)
        
        #Dictionary to hold socket objects once connected keys are socket names, values are connected socket objects
        self.connected_sockets = {"Desktop Test": {"sck": None, "address": "192.168.3.102", "port": 10000, "err": None},
                               "RPI Test":{"sck": None, "address": "192.168.3.103", "port": 10000, "err": None},
                               "Leia Laptop Depth": {"sck": None, "address": "192.168.3.110", "port": 10000, "err": None}}
        
        #Call Connect sockets function
        self.ConnectSockets()
        
        #Call RelayStatus function
        
        #Call EPOD Status function
        self.EPOD_Status()
        
 
        #set up your socket with the desired settings.
        #self.relay_sock = self.socket(socket.AF_INET, socket.SOCK_STREAM)
        #instantiate the board object and pass it the network socket
        #self.RelayBoard = self.Relay_Controller(sock)
        #connect the socket using desired IP and Port
        #IP_ADDRESS = "192.168.3.52"
        #PORT = 2101 #Default port for the ProXR relays.
        #sock.connect((IP_ADDRESS, PORT))
        #sock.settimeout(.5)
        
        #Call the RelayStatus function, get initial Relays state
        #self.RelayStatus()
        
        #Call the PnTStatus functions, get intial Pan and Tilt Positions
        
        #Initiate left/right side frames
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row = 0, column = 0)
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row = 0, column = 1, sticky = tk.N)
        
        #Instantiate sub frames geometry
        self.relays_frame = tk.Frame(self.left_frame, highlightbackground = "black", highlightthickness = 2)
        self.relays_frame.grid(row = 0, column =0, padx = 10, pady = 10)
        self.alarms_frame = tk.Frame(self.left_frame, highlightbackground = "black", highlightthickness = 2)
        self.alarms_frame.grid(row = 1, column =0)
        self.pnt_frame = tk.Frame(self.right_frame, highlightbackground = "black", highlightthickness = 2)
        self.pnt_frame.grid(row = 0, column =0, padx = 10, pady = 10)    
        self.vals_frame = tk.Frame(self.right_frame, highlightbackground = "black", highlightthickness = 2)
        self.vals_frame.grid(row = 1, column = 0, pady = 10)
        self.grounds_frame = tk.Frame(self.right_frame, highlightbackground = "black", highlightthickness = 2)
        self.grounds_frame.grid(row = 2, column =0, pady = 10) 
        
        #Label for Relay Controls
        tk.Label(self.relays_frame, text = "Relay Controls").grid(row=0, column = 0, pady = 10, padx = 5)
        
        #Relay buttons for Bank 1 (main ProXR relay card)
        tk.Label(self.relays_frame, text = "MiniZeus").grid(row = 1, column =0, pady = 5)
        self.RB1_1_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_1)
        self.RB1_1_toggle.grid(row = 1, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "RayFin Mk2").grid(row = 2, column =0, pady = 5)
        self.RB1_2_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_2)
        self.RB1_2_toggle.grid(row = 2, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "CTD").grid(row = 3, column =0, pady = 5)        
        self.RB1_3_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_3)
        self.RB1_3_toggle.grid(row = 3, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Responder").grid(row = 4, column =0, pady = 5)        
        self.RB1_4_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_4)
        self.RB1_4_toggle.grid(row = 4, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Pan & Tilt/Depth").grid(row = 5, column =0, pady = 5)        
        self.RB1_5_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_5)
        self.RB1_5_toggle.grid(row = 5, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "GoPro Trickle Charge").grid(row = 6, column =0, pady = 5)        
        self.RB1_6_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_6)
        self.RB1_6_toggle.grid(row = 6, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Tritech/SD Cam").grid(row = 7, column =0, pady = 5)        
        self.RB1_7_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_7)
        self.RB1_7_toggle.grid(row = 7, column =1, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Sonar").grid(row = 8, column =0, pady = 5)        
        self.RB1_8_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB1_8)
        self.RB1_8_toggle.grid(row = 8, column =1, padx = 5, pady = 5)
        
        
        #Relay buttons for Bank 4 (ProXR relay expansion card)
        
        tk.Label(self.relays_frame, text = "Altimeter").grid(row = 1, column =2, pady = 5)         
        self.RB4_1_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_1)
        self.RB4_1_toggle.grid(row = 1, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Sphere Lights").grid(row = 2, column =2, pady = 5)         
        self.RB4_2_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_2)
        self.RB4_2_toggle.grid(row = 2, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Lasers").grid(row = 3, column =2, pady = 5)       
        self.RB4_3_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_3)
        self.RB4_3_toggle.grid(row = 3, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "A125 DVL").grid(row = 4, column =2, pady = 5)        
        self.RB4_4_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_4)
        self.RB4_4_toggle.grid(row = 4, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Port ROS LED Light").grid(row = 5, column =2, pady = 5)        
        self.RB4_5_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_5)
        self.RB4_5_toggle.grid(row = 5, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Stbd ROS LED Light").grid(row = 6, column =2, pady = 5)        
        self.RB4_6_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_6)
        self.RB4_6_toggle.grid(row = 6, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Port HID Light").grid(row = 7, column =2, pady = 5)           
        self.RB4_7_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_7)
        self.RB4_7_toggle.grid(row = 7, column =3, padx = 5, pady = 5)
        
        tk.Label(self.relays_frame, text = "Stbd HID Light").grid(row = 8, column =2, pady = 5)          
        self.RB4_8_toggle = tk.Button(self.relays_frame, text = "OFF", bg = 'grey', command=self.RB4_8)
        self.RB4_8_toggle.grid(row = 8, column =3, padx = 5, pady = 5)
        
        #Store all the buttons in a list, for later processing. Set them all to disabled to start
        self.button_list = [self.RB1_1_toggle, self.RB1_2_toggle, self.RB1_3_toggle, self.RB1_4_toggle, self.RB1_5_toggle,
                            self.RB1_6_toggle, self.RB1_7_toggle, self.RB1_8_toggle, self.RB4_1_toggle, self.RB4_2_toggle,
                            self.RB4_3_toggle, self.RB4_4_toggle, self.RB4_5_toggle, self.RB4_6_toggle, self.RB4_7_toggle,
                            self.RB4_8_toggle]
        
        for each in self.button_list:
            each.configure(state = "disabled")

        #Call the RelayStatus function
        #self.RelayStatus()
        
        #List of Relay buttons, to iterate through.
        
        #Alarms Pane
        tk.Label(self.alarms_frame, text = 'Alarms').grid(row = 9, column = 0, pady = 70)    
        
        
        #Pan and Tilt Pane
        tk.Label(self.pnt_frame, text = 'Pan').grid(row = 0, column = 4 )
        self.pan_entry = tk.Entry(self.pnt_frame, width = 2)
        self.pan_entry.grid(row = 0, column = 5, pady = 0)
        tk.Label(self.pnt_frame, text = "Tilt").grid(row = 0, column = 6, pady = 0)
        self.tilt_entry = tk.Entry(self.pnt_frame, width = 2)
        self.tilt_entry.grid(row = 0, column = 7, pady = 0)       
        
        #Values Info Pane
        tk.Label(self.vals_frame, text = "Time").grid(row = 1, column = 4, pady = (20,0))
        self.time_val = tk.Entry(self.vals_frame, width = 10)
        self.time_val.grid(row = 1, column = 5, pady = (20,0))
        tk.Label(self.vals_frame, text = "Depth").grid(row = 2, column = 4)
        self.depth_val = tk.Entry(self.vals_frame, width = 10)
        self.depth_val.grid(row = 2, column = 5)        
        tk.Label(self.vals_frame, text = "EPOD Temp").grid(row = 3, column = 4)
        self.temp_val = tk.Entry(self.vals_frame, width = 10)
        self.temp_val.grid(row = 3, column = 5)
        tk.Label(self.vals_frame, text = "EPOD Humidity %").grid(row = 4, column = 4)
        self.hum_val = tk.Entry(self.vals_frame, width = 10)
        self.hum_val.grid(row = 4, column = 5)        
        tk.Label(self.vals_frame, text = "EPOD Pressure (hPa)").grid(row = 5, column = 4)
        self.press_val = tk.Entry(self.vals_frame, width = 10)
        self.press_val.grid(row = 5, column = 5)
   
        #Ground Faults Monitoring Pane
        
        #Labels and Progress Bars
        tk.Label(self.grounds_frame, text = "Ground Faults Status").grid(row = 0, column = 0, pady = (0, 20))
        tk.Label(self.grounds_frame, text = "Channel 1").grid(row = 1, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 1, column = 1, padx = (0,10))
        tk.Label(self.grounds_frame, text = "Channel 2").grid(row = 2, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 2, column = 1, padx = (0,10))        
        tk.Label(self.grounds_frame, text = "Channel 3").grid(row = 3, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 3, column = 1, padx = (0,10))        
        tk.Label(self.grounds_frame, text = "Channel 4").grid(row = 4, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 4, column = 1, padx = (0,10))    
        tk.Label(self.grounds_frame, text = "Channel 5").grid(row = 5, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 5, column = 1, padx = (0,10))
        tk.Label(self.grounds_frame, text = "Channel 6").grid(row = 6, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 6, column = 1, padx = (0,10))
        tk.Label(self.grounds_frame, text = "Channel 7").grid(row = 7, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 7, column = 1, padx = (0,10))
        tk.Label(self.grounds_frame, text = "Channel 8").grid(row = 8, column = 0)
        ttk.Progressbar(self.grounds_frame, orient = 'horizontal', mode = 'determinate', length = 100).grid(row = 8, column = 1, padx = (0,10))

        #Tk.Entry boxes, to show values in ohms
        self.ch1_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch1_adc.grid(row = 1, column = 2)
        self.ch2_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch2_adc.grid(row = 2, column = 2)
        self.ch3_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch3_adc.grid(row = 3, column = 2)
        self.ch4_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch4_adc.grid(row = 4, column = 2)
        self.ch5_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch5_adc.grid(row = 5, column = 2)
        self.ch6_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch6_adc.grid(row = 6, column = 2)
        self.ch7_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch7_adc.grid(row = 7, column = 2)
        self.ch8_adc = tk.Entry(self.grounds_frame, width = 10)
        self.ch8_adc.grid(row = 8, column = 2)

    #Loop through all the servers in the list, and attempt to connect to them. Store connected sockets in 
    #self.connected_sockets() dictonary. Sockets that are not connected have the value None.
    #If the "sck" value is None, no connection has been attempt yet. First pass. Attempt connection
    #If the "err" value is not None, then a connection was attempted but failed and an error was logged. Attempt connection again.
    def ConnectSockets(self):
        for name, sock in self.connected_sockets.items():
            if sock["sck"] is None: #If the value is None, it is not holding a socket object, and needs to be connected
                try:
                    self.PostStatus(f'Attempting connection to {name} at {sock["address"], sock["port"]}')
                    sock["sck"] = socket.create_connection((sock["address"], sock["port"]), timeout = 1)
                    self.PostStatus(f'Connected to {name} at {sock["address"], sock["port"]}')
                    sock["err"] = None 
                except (socket.error) as err_msg:
                    sock["err"] = err_msg
                    self.PostStatus(f'Failed to connect to {name} at {sock["address"], sock["port"]} error: {sock["err"]}')
            else:
                try:
                    sock["sck"].send(bytes(1)) #Send one byte, to check is server side of socket is open. This will throw and exception if it fails.
                except Exception as error: #If this throws an exception, the connection is probably no longer live. Try to re-establish

#TODO - maybe it is easier/better to just set sock["sck"] = None again, if the send call fails?
                    self.PostStatus(f'Could not connect to {name} at {sock["address"], sock["port"]}, attempting to reconnect')
                    sock["sck"] = socket.create_connection((sock["address"], sock["port"]), timeout = 1)
                    self.PostStatus(f'Connected to {name} at {sock["address"], sock["port"]}')
                    sock["err"] = None 
        self.after(4000, self.ConnectSockets)
            
        
    #Function to check all relay status at start up. If the relay socket is connected, remove grey out from the buttons.
    #Add the statuses as key value pairs to a dictionary called 'relay_statuses'
    def RelayStatus(self):
        if self.connected_sockets["NCD_Relays"]["sck"] is None or self.connected_sockets["NCD_Relays"]["err"]:
            pass
        else:
            #self.relay_board = ncd.Relay_Controller(self.connected_sockets["NCD_Relays"]["sck"])
            for each in self.button_list:
                each.configure(state = "enabled")
            for i in range(1,9):
                self.bank1_label = "RB1_" + str(i)
                self.bank1_status = self.relay_board.get_relay_status_by_bank(i, 1)
                self.bank4_label = "RB4_" + str(i)
                self.bank4_status = self.relay_board.get_relay_status_by_bank(i, 4)
                self.relay_statuses[self.bank1_label] = self.bank1_status
                self.relay_statuses[self.bank4_label] = self.bank4_status
        self.after(1000, self.RelayStatus)
                

    #Send tilt and pan value status queries to both the tilt and pan axis, store the received values for a tk.Entry box     
    def TiltStatus(self):
        if self.connected_sockets["PnT"]["sck"] is None or self.connected_sockets["PnT"]["err"]:
            pass
        else:
            self.tilt_status_command = [b'A',b'f']
            self.pan_status_command = [b'B',b'f']
            self.connected_sockets["PnT"]["sck"].send(self.tilt_status_command)
            self.tilt_val = str(self.connected_sockets["PnT"]["sck"].recv(8))
            self.tilt_val = self.tilt_val.decode()
            self.tilt_entry.delete(0, tk.END)  #Delete whatever values was in the box from the previous iteration.
            self.tilt_entry.insert(0, self.tilt_val)
            self.connected_sockets["PnT"]["sck"].send(self.pan_status_command)
            self.pan_val = str(self.connected_sockets["PnT"]["sck"].recv(8))
            self.pan_val = self.pan_val.decode()
            self.pan_entry.delete(0, tk.END)
            self.pan_entry.insert(0, self.pan_val)
        self.after(1000, self.TiltStatus)
        
    #Get the Analog to Digital Conversion values from the Relay Board, insert these into the ground fault status entry 
    #boxes, and update the progress bar extents.
    def ADCStatus(self):
        if self.connected_sockets["PnT"]["sck"] is None or self.connected_sockets["PnT"]["err"]:
            pass
        else:
            self.adc_all = self.relay_board.read_all_ad10()
            for i in range(1, 9):
                self.adc_all[i] 
                
    #Function to report the temp, humidity and pressure values in the EPOD            
    def EPOD_Status(self):
        if self.connected_sockets["RPI Test"]["sck"] is None or self.connected_sockets["PnT"]["err"]:
            pass
        else:
            self.epod_data = str(self.connected_sockets["RPI Test"]["sck"].recv(64))
            self.epod_data = string.split(",", self.epod_data)
            self.temp_val.delete(0, tk.END)
            self.temp_val.insert(0, self.epod_data[1])
            self.hum_val.delete(0, tk.END)
            self.hum_val.insert(0, self.epod_data[2])
            self.press_val.delete(0, tk.END)
            self.press_val.insert(0, self.epod_data[3])
        self.after(1000, self.EPOD_Status)
        
            
            
            
    
    #Custom quit function. Try to close all the sockets, kill the parent window.
    def CloseProgram(self):
        for name, sock in self.connected_sockets.items():
            try:
                sock["sck"].close()
            except:
                pass
        self.parent.destroy() #Kill Tk root instance.
        
        
        
    #Function to post status messages to the second window, line by line
    def PostStatus(self, msg):
        self.msg = msg
        self.msg = str(datetime.datetime.now()) + str(",") + str(self.msg) + str("\n")
        self.program_status.insert(tk.END, self.msg)
        self.program_status.see(tk.END)

        
        
        
###############################################################################################################
##                              BUTTONS SPECIFIC FUNCTIONS                                                  ##
###############################################################################################################

    #Relay Bank 1
    def RB1_1(self):
        if self.RB1_1_toggle["bg"] == 'grey':
            self.RB1_1_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_1 on")
        else:
            self.RB1_1_toggle.configure(bg = "grey", text = "OFF") 
            self.PostStatus("RB1_1 off")               
    def RB1_2(self):
        if self.RB1_2_toggle["bg"] == 'grey':
            self.RB1_2_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_2 on")
        else:
            self.RB1_2_toggle.configure(bg = "grey", text = "OFF")   
            self.PostStatus("RB1_2 off")
    def RB1_3(self):
        if self.RB1_3_toggle["bg"] == 'grey':
            self.RB1_3_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_3 on")
        else:
            self.RB1_3_toggle.configure(bg = "grey", text = "OFF")     
            self.PostStatus("RB1_3 off")
    def RB1_4(self):
        if self.RB1_4_toggle["bg"] == 'grey':
            self.RB1_4_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_4 on")
        else:
            self.RB1_4_toggle.configure(bg = "grey", text = "OFF")  
            self.PostStatus("RB1_4 off")
    def RB1_5(self):
        if self.RB1_5_toggle["bg"] == 'grey':
            self.RB1_5_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_5 on")
        else:
            self.RB1_5_toggle.configure(bg = "grey", text = "OFF") 
            self.PostStatus("RB1_1 off")
            
    def RB1_6(self):
        if self.RB1_6_toggle["bg"] == 'grey':
            self.RB1_6_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_6 on")
        else:
            self.RB1_6_toggle.configure(bg = "grey", text = "OFF")  
            self.PostStatus("RB1_6 off")
    def RB1_7(self):
        if self.RB1_7_toggle["bg"] == 'grey':
            self.RB1_7_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_7 on")
        else:
            self.RB1_7_toggle.configure(bg = "grey", text = "OFF")   
            self.PostStatus("RB1_7 on")
    def RB1_8(self):
        if self.RB1_8_toggle["bg"] == 'grey':
            self.RB1_8_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB1_8 on")
        else:
            self.RB1_8_toggle.configure(bg = "grey", text = "OFF")  
            self.PostStatus("RB1_8 off")            
    
    #Relay bank 4 switch functions.
    def RB4_1(self):
        if self.RB4_1_toggle["bg"] == 'grey':
            self.RB4_1_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_1 on")
        else:
            self.RB4_1_toggle.configure(bg = "grey", text = "OFF")  
            self.PostStatus("RB4_1 off")            
    def RB4_2(self):
        if self.RB4_2_toggle["bg"] == 'grey':
            self.RB4_2_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_2 on")
        else:
            self.RB4_2_toggle.configure(bg = "grey", text = "OFF") 
            self.PostStatus("RB4_2 off")
    def RB4_3(self):
        if self.RB4_3_toggle["bg"] == 'grey':
            self.RB4_3_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_3 on")
        else:
            self.RB4_3_toggle.configure(bg = "grey", text = "OFF") 
            self.PostStatus("RB4_3 off")
    def RB4_4(self):
        if self.RB4_4_toggle["bg"] == 'grey':
            self.RB4_4_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_4 on")
        else:
            self.RB4_4_toggle.configure(bg = "grey", text = "OFF")
            self.PostStatus("RB4_4 off")
    def RB4_5(self):
        if self.RB4_5_toggle["bg"] == 'grey':
            self.RB4_5_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_5 on")
        else:
            self.RB4_5_toggle.configure(bg = "grey", text = "OFF") 
            self.PostStatus("RB4_5 off")              
    def RB4_6(self):
        if self.RB4_6_toggle["bg"] == 'grey':
            self.RB4_6_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_6 on")
        else:
            self.RB4_6_toggle.configure(bg = "grey", text = "OFF")
            self.PostStatus("RB4_6 off")
    def RB4_7(self):
        if self.RB4_7_toggle["bg"] == 'grey':
            self.RB4_7_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_7 on")
        else:
            self.RB4_7_toggle.configure(bg = "grey", text = "OFF") 
            self.PostStatus("RB4_7 off")
    def RB4_8(self):
        if self.RB4_8_toggle["bg"] == 'grey':
            self.RB4_8_toggle.configure(bg = "green", text = "ON")
            self.PostStatus("RB4_8 on")
        else:
            self.RB4_8_toggle.configure(bg = "grey", text = "OFF")  
            self.PostStatus("RB4_8 off")

            
            
            
            

##############################################CALL THE MAINLOOP##################################################
        
if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).grid(row = 0, column =0)
    root.mainloop()
        
